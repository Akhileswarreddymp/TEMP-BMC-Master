from datetime import datetime
from typing import Optional
from pydantic import BaseModel,validator


class RoleBase(BaseModel):
    role: str 
    is_active: Optional[bool] = True
    last_updated_by: Optional[str]
    last_updated_date: datetime


    

class RoleResponse(BaseModel):
    message: str
    data: RoleBase

class RoleFunctionResponse(BaseModel):
    data_exists: bool
    data: RoleBase
