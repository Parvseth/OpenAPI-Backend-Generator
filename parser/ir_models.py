from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class IRField(BaseModel):
    name: str
    openapi_type: str
    python_type: str = "str"
    sqlalchemy_type: str = "String"
    pydantic_type: str = "str"
    required: bool = False
    nullable: bool = True
    default: Optional[Any] = None
    description: Optional[str] = None
    format: Optional[str] = None
    min_length: Optional[int] = None
    max_length: Optional[int] = None
    pattern: Optional[str] = None
    is_primary_key: bool = False
    is_foreign_key: bool = False
    foreign_key_target: Optional[str] = None  # e.g., "users.id"
    enum_values: Optional[List[str]] = None

class IRRelationship(BaseModel):
    name: str
    target_model: str
    relationship_type: str = "many-to-one"  # one-to-many, many-to-one, one-to-one
    foreign_key_field: Optional[str] = None

class IRModel(BaseModel):
    name: str
    table_name: str
    description: Optional[str] = None
    fields: List[IRField] = Field(default_factory=list)
    relationships: List[IRRelationship] = Field(default_factory=list)

class IRParameter(BaseModel):
    name: str
    location: str  # path, query, header, cookie
    python_type: str = "str"
    required: bool = False
    default: Optional[Any] = None
    description: Optional[str] = None

class IRRequestBody(BaseModel):
    model_config = {"protected_namespaces": ()}
    required: bool = False
    model_name: Optional[str] = None
    content_type: str = "application/json"
    fields: List[IRField] = Field(default_factory=list)

class IRResponse(BaseModel):
    model_config = {"protected_namespaces": ()}
    status_code: int = 200
    description: str = "Success"
    model_name: Optional[str] = None
    is_list: bool = False

class IRRoute(BaseModel):
    path: str
    method: str  # GET, POST, PUT, PATCH, DELETE
    operation_id: str
    summary: Optional[str] = None
    description: Optional[str] = None
    tags: List[str] = Field(default_factory=list)
    parameters: List[IRParameter] = Field(default_factory=list)
    request_body: Optional[IRRequestBody] = None
    responses: List[IRResponse] = Field(default_factory=list)
    target_model: Optional[str] = None
    service_method_name: str = ""

class IRSpec(BaseModel):
    title: str = "Generated API"
    version: str = "1.0.0"
    description: Optional[str] = None
    base_url: str = "http://localhost:8000"
    models: List[IRModel] = Field(default_factory=list)
    routes: List[IRRoute] = Field(default_factory=list)
    tags: List[str] = Field(default_factory=list)
