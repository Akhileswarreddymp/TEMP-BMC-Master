from datetime import datetime
from typing import Optional,List
from pydantic import BaseModel


class RoleBase(BaseModel):
    role: str
    is_active: Optional[bool] = True
    last_updated_by: Optional[str]
    last_updated_date: datetime


class RoleBaseId(BaseModel):
    id: int
    role: str
    is_active: Optional[bool] = True
    last_updated_by: Optional[str]
    last_updated_date: datetime
    

class RoleResponse(BaseModel):
    message: str
    data: RoleBaseId


class RoleBulkResponse(BaseModel):
    message: str
    data: List[RoleBaseId]


class RoleFunctionResponse(BaseModel):
    data_exists: bool
    data: RoleBaseId


class RoleFunctionResponses(BaseModel):
    data_exists: bool
    data: List[RoleBaseId]