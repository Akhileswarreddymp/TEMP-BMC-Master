from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, validator


class CityBase(BaseModel):
    code: str
    name: str
    is_active: Optional[bool] = True
    last_updated_by: Optional[str]
    last_updated_date: datetime



class CityFunctionResp(BaseModel):
    data_exists: bool
    data: CityBase


class CityResponse(BaseModel):
    message: str
    data: CityBase


class CitiesFunctionResponse(BaseModel):
    data_exists: bool
    data: List[CityBase]


class CitiesBulkResponse(BaseModel):
    message: str
    data: List[CityBase]
