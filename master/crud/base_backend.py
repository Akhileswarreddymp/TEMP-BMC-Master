from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession


class BaseBackend:
    def __init__(self, session: AsyncSession, concrete_type: type[BaseModel]) -> None:
        self.session = session
        self.concrete_type = concrete_type
