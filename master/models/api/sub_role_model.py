from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel


class SubRoleBase(BaseModel):
    role_id: int
    sub_role_name: str
    sub_role_description: str
    is_active: Optional[bool] = True
    last_updated_by: Optional[str]
    last_updated_date: datetime


class SubRoleIdBase(BaseModel):
    id: int
    role_id: int
    sub_role_name: str
    sub_role_description: str
    is_active: Optional[bool] = True
    last_updated_by: Optional[str]
    last_updated_date: datetime


class SubRoleFunctionResponse(BaseModel):
    data_exist: bool
    data: SubRoleIdBase


class SubRoleFunctionResponses(BaseModel):
    data_exist: bool
    data: List[SubRoleIdBase]


class SubRoleResponse(BaseModel):
    message: str
    data: SubRoleIdBase


class SubRoleResponses(BaseModel):
    message: str
    data: List[SubRoleIdBase]
