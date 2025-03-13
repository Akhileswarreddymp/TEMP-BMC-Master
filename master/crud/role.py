from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from master.models.database.models import Roles
from master.models.api.roles_model import RoleBase,RoleFunctionResponse
from master.crud.base_backend import BaseBackend

class RolesService(BaseBackend):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Roles)

    async def add_roles(self, request : RoleBase):
        query = await self.session.execute(
            select(Roles).where(Roles.role == request.role)
        )

        query_data = query.scalars().first()

        if query_data:
            return RoleFunctionResponse(
                data_exists=True,
                data=RoleBase(
                    role=query_data.role,
                    is_active=query_data.is_active,
                    last_updated_by=query_data.last_updated_by,
                    last_updated_date=query_data.last_updated_date
                )
            )
        
        role_data = Roles(
            role=request.role,
            is_active=request.is_active,
            last_updated_by=request.last_updated_by
        )


        self.session.add(role_data)
        await self.session.commit()
        await self.session.refresh(role_data)

        return RoleFunctionResponse(
            data_exists=False,
            data=role_data
        )
    
