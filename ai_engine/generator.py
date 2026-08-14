import os
import re
from typing import Optional
from logger import logger
from ai_engine.ast_verifier import verify_python_syntax, verify_ast
from ai_engine.prompts import SYSTEM_PROMPT_SERVICE_LOGIC, SYSTEM_PROMPT_RETRY

def get_groq_client():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return None
    from groq import Groq
    return Groq(api_key=api_key)

def get_async_groq_client():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return None
    from groq import AsyncGroq
    return AsyncGroq(api_key=api_key)

def route_model(task_type: str) -> str:
    """
    Dual-Tier Model Router: Routes to smaller/faster models for scaffolding 
    and larger/slower models for complex reasoning.
    """
    if task_type == "scaffolding":
        return "llama-3.1-8b-instant"
    elif task_type == "reasoning":
        return "llama-3.3-70b-versatile"
    return "llama-3.3-70b-versatile"

def strip_code_fences(code: str) -> str:
    """Removes ```python and ``` wrappers if present."""
    code = code.strip()
    if code.startswith("```"):
        lines = code.splitlines()
        if lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip().startswith("```"):
            lines = lines[:-1]
        code = "\n".join(lines).strip()
    return code

async def generate_ai_service_logic(
    route_summary: str,
    method: str,
    path: str,
    model,
    operation_id: str,
    max_retries: int = 3
) -> str:
    client = get_async_groq_client()
    
    # Semantic Chunking Context Injection
    fields_info = "\n".join([f"- {f.name} ({f.python_type})" for f in model.fields])
    rel_info = "\n".join([f"- {r.name} -> {r.target_model}" for r in model.relationships])
    
    prompt = f"""Write ONLY the Python statements for the inside of a method body in a Service class.

Method: {method}
Path: {path}
Summary: {route_summary}
Target Model: models.{model.name}
Operation ID: {operation_id}

Schema Context (Use this to write accurate database insertions):
Fields:
{fields_info}
Relationships:
{rel_info}

Rules:
- Do NOT write 'def function_name(...):' or nested function definitions.
- Use `self.db` for database session queries.
- Use `models.{model.name}` for SQLAlchemy model class.
- Use `data` for Pydantic schema input.
- Wrap creation in try/except with `self.db.rollback()` and `raise HTTPException(status_code=400, detail=str(e))` if error.
- Return the created/retrieved model instance.

Example output:
try:
    db_item = models.{model.name}(**data.model_dump())
    self.db.add(db_item)
    self.db.commit()
    self.db.refresh(db_item)
    return db_item
except Exception as e:
    self.db.rollback()
    raise HTTPException(status_code=400, detail=str(e))
"""

    if not client:
        logger.warning(f"GROQ_API_KEY not set. Using deterministic fallback for {method} {path}.")
        return generate_deterministic_fallback(method, model.name, operation_id)

    current_prompt = prompt
    system_prompt = SYSTEM_PROMPT_SERVICE_LOGIC

    attempt = 0
    while attempt < max_retries:
        attempt += 1
        try:
            response = await client.chat.completions.create(
                model=route_model("scaffolding"),
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": current_prompt}
                ],
                temperature=0.2,
                max_tokens=2048
            )
            raw_code = response.choices[0].message.content or ""
            clean_code = strip_code_fences(raw_code)

            # Test full function wrapping for AST verification
            test_wrapped_code = f"def dummy_func(db, data=None, item_id=None):\n" + "\n".join(
                f"    {line}" for line in clean_code.splitlines()
            )

            is_valid, err_msg = verify_python_syntax(test_wrapped_code)
            if is_valid:
                # Syntax is valid, now run SAST security scan
                is_secure, sec_err_msg = verify_ast(test_wrapped_code)
                if is_secure:
                    logger.info(f"✅ AI generated valid & secure logic for {method} {path} (Attempt {attempt})")
                    return clean_code
                else:
                    logger.warning(f"⚠️ AI code failed Security SAST verification (Attempt {attempt}/{max_retries})")
                    err_msg = sec_err_msg
            else:
                logger.warning(f"⚠️ AI code failed AST verification (Attempt {attempt}/{max_retries}): {err_msg}")
            
            # Prepare self-repair prompt
            system_prompt = SYSTEM_PROMPT_RETRY
            current_prompt = f"The following code failed verification:\n\n{clean_code}\n\nError details:\n{err_msg}\n\nPlease fix and return corrected Python code ONLY."

        except Exception as e:
            logger.error(f"Error calling LLM API (Attempt {attempt}): {e}")

    logger.warning(f"Falling back to deterministic logic for {method} {path}")
    return generate_deterministic_fallback(method, model.name, operation_id)

def generate_deterministic_fallback(method: str, model_name: str, operation_id: str) -> str:
    m = method.upper()
    if m == "GET":
        return f"""# Retrieve records
db_item = db.query(models.{model_name}).first()
if not db_item:
    raise HTTPException(status_code=404, detail="{model_name} not found")
return db_item"""
    elif m == "POST":
        return f"""# Create record
db_item = models.{model_name}(**data.dict())
db.add(db_item)
db.commit()
db.refresh(db_item)
return db_item"""
    elif m in ["PUT", "PATCH"]:
        return f"""# Update record
db_item = db.query(models.{model_name}).filter(models.{model_name}.id == item_id).first()
if not db_item:
    raise HTTPException(status_code=404, detail="{model_name} not found")
for key, value in data.dict(exclude_unset=True).items():
    setattr(db_item, key, value)
db.commit()
db.refresh(db_item)
return db_item"""
    elif m == "DELETE":
        return f"""# Delete record
db_item = db.query(models.{model_name}).filter(models.{model_name}.id == item_id).first()
if not db_item:
    raise HTTPException(status_code=404, detail="{model_name} not found")
db.delete(db_item)
db.commit()
return {{"message": "{model_name} deleted successfully"}}"""
    
    return f'return {{"message": "Execution of {operation_id}"}}'
