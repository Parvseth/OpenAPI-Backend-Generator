import os
import re
import subprocess
from typing import Optional
from logger import logger
from ai_engine.generator import get_groq_client, strip_code_fences
from ai_engine.prompts import SYSTEM_PROMPT_TEST_HEALING

def run_self_healing_loop(output_dir: str, max_retries: int = 3) -> bool:
    """
    Runs pytest on the generated backend. If it fails, uses the AI to parse the failure
    and rewrite the offending service logic.
    """
    logger.info("🧪 [Self-Healing] Starting test-driven self-healing loop...")
    client = get_groq_client()
    
    if not client:
        logger.warning("[Self-Healing] GROQ_API_KEY not set. Skipping self-healing.")
        return False
        
    for attempt in range(1, max_retries + 1):
        logger.info(f"🧪 [Self-Healing] Running tests (Attempt {attempt}/{max_retries})...")
        
        # Run pytest
        result = subprocess.run(
            ["pytest", "tests/"],
            cwd=output_dir,
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            logger.info("✅ [Self-Healing] All integration tests passed!")
            return True
            
        logger.warning(f"⚠️ [Self-Healing] Tests failed (Attempt {attempt})")
        error_log = result.stdout + "\n" + result.stderr
        
        # Determine which test failed and map it to the service file
        failed_services = extract_failed_services(error_log)
        
        if not failed_services:
            logger.error("[Self-Healing] Could not determine which service failed from the logs.")
            return False
            
        for service_name in failed_services:
            service_path = os.path.join(output_dir, "app", "services", f"{service_name}.py")
            if not os.path.exists(service_path):
                continue
                
            logger.info(f"🔧 [Self-Healing] AI is analyzing and rewriting {service_name}.py...")
            with open(service_path, "r", encoding="utf-8") as f:
                current_code = f.read()
                
            new_code = heal_service_code(client, current_code, error_log)
            if new_code:
                with open(service_path, "w", encoding="utf-8") as f:
                    f.write(new_code)
                    
    logger.error("❌ [Self-Healing] Max retries reached. Tests still failing.")
    return False

def extract_failed_services(error_log: str) -> list[str]:
    """
    Extracts the service names that correspond to failed test files or import errors.
    Example: 'tests/test_user.py FAILED' -> ['user_service']
    Example: 'ImportError: ... app.services.user_service' -> ['user_service']
    """
    failed_services = set()
    # Match pytest failures
    matches = re.findall(r"tests/test_([a-zA-Z0-9_]+)\.py", error_log)
    for match in matches:
        failed_services.add(f"{match}_service")
        
    # Regex 2: For ImportErrors caused by bad class names
    # Example: ImportError: cannot import name 'CustomercreateService' from 'app.services.customercreate_service'
    import_error_matches = re.findall(r"from 'app\.services\.(\w+)'", error_log)
    for s in import_error_matches:
        failed_services.add(f"{s}.py")

    # Regex 3: For ImportErrors or syntax errors inside the service file itself
    # Example: app\services\customer_service.py:6: in <module>
    traceback_matches = re.findall(r"app[\\/]services[\\/](\w+\.py):", error_log)
    for s in traceback_matches:
        failed_services.add(s)
        
    return list(failed_services)

def heal_service_code(client, current_code: str, error_log: str) -> Optional[str]:
    """Calls Groq to rewrite the code based on the error log."""
    prompt = f"""The following service layer code failed integration tests.

CURRENT CODE:
{current_code}

PYTEST OUTPUT:
{error_log[-2000:]}

Analyze the error and rewrite the entire Python file to fix it. Return ONLY the raw Python code. Do not use Markdown."""

    if "ImportError: cannot import name" in error_log:
        prompt += "\n\nHINT: The error is an ImportError. Make sure the class name in your code EXACTLY matches the name being imported."

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT_TEST_HEALING},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_tokens=2048
        )
        raw_code = response.choices[0].message.content or ""
        return strip_code_fences(raw_code)
    except Exception as e:
        logger.error(f"[Self-Healing] LLM API Error: {e}")
        return None
