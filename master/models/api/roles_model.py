from datetime import datetime
from typing import Optional,List
from pydantic import BaseModel


class RoleBase(BaseModel):
    role: str
    is_active: Optional[bool] = True
    last_updated_by: Optional[str]
    last_updated_date: datetime


class RoleResponse(BaseModel):
    message: str
    data: RoleBase


class RoleBulkResponse(BaseModel):
    message: str
    data: List[RoleBase]


class RoleFunctionResponse(BaseModel):
    data_exists: bool
    data: RoleBase


class RoleFunctionResponses(BaseModel):
    data_exists: bool
    data: List[RoleBase]