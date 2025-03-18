from datetime import datetime, timezone
from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from master.models.api.sub_role_model import SubRoleBase, SubRoleFunctionResponse, SubRoleFunctionResponses, SubRoleIdBase
from master.models.database.models import SubRoles
from master.crud.base_backend import BaseBackend

class SubRoleService(BaseBackend):
    def __init__(self, session: AsyncSession):
        super().__init__(session, SubRoles)

    async def add_sub_role(self,request: SubRoleBase):
        try:
            query = await self.session.execute(
                select(SubRoles).where(SubRoles.sub_role_name == request.sub_role_name)
            )

            query_data = query.scalars().first()

            if query_data:
                return SubRoleFunctionResponse(
                    data_exist=True,
                    data=query_data
                )
            
            sub_role_data = SubRoles(
                role_id=request.role_id,
                sub_role_name=request.sub_role_name,
                sub_role_description=request.sub_role_description,
                is_active=request.is_active,
                last_updated_by=request.last_updated_by,
                last_updated_date= datetime.now(tz=timezone.utc).replace(tzinfo=None)
            )
            self.session.add(sub_role_data)
            await self.session.commit()
            await self.session.refresh(sub_role_data)

            return SubRoleFunctionResponse(
                data_exist=False,
                data=sub_role_data
            )
        except SQLAlchemyError as err:
            await self.session.rollback()
            raise HTTPException(
                status_code=500, detail=f"Database error: {str(err)}"
            ) from err
        except Exception as error:
            raise HTTPException(
                status_code=500,
                detail=f"Unexpected error while adding sub role: {str(error)}",
            ) from error
        
    async def get_all_sub_roles(self, status: str):
        try:
            if status == "1":
                query = await self.session.execute(
                    select(SubRoles).where(SubRoles.is_active)
                )
            elif status == "0":
                query = await self.session.execute(
                    select(SubRoles).where(SubRoles.is_active == False)
                )
            else:
                query = await self.session.execute(
                    select(SubRoles)
                )

            query_data = query.scalars().all()

            if query_data:
                return SubRoleFunctionResponses(
                    data_exist=True,
                    data=query_data
                )
            
            return SubRoleFunctionResponses(
                data_exist=False,
                data=[SubRoleIdBase(
                    id=0,
                    role_id=0,
                    sub_role_name="",
                    sub_role_description="",
                    last_updated_by="",
                    last_updated_date=datetime.now(tz=timezone.utc).replace(tzinfo=None)
                )]
            )
        except SQLAlchemyError as err:
            await self.session.rollback()
            raise HTTPException(
                status_code=500, detail=f"Database error: {str(err)}"
            ) from err
        except Exception as error:
            raise HTTPException(
                status_code=500,
                detail=f"Unexpected error while getting sub roles: {str(error)}",
            ) from error
    
    async def get_sub_role(self,sub_role_name: str):
        try:
            query = await self.session.execute(
                select(SubRoles).where(SubRoles.sub_role_name == sub_role_name)
            )

            query_data = query.scalars().first()

            if query_data:
                return SubRoleFunctionResponse(
                    data_exist=True,
                    data=query_data
                )
            
            return SubRoleFunctionResponse(
                data_exist=False,
                data=SubRoleIdBase(
                    id=0,
                    role_id=0,
                    sub_role_name="",
                    sub_role_description="",
                    last_updated_by="",
                    last_updated_date=datetime.now(tz=timezone.utc).replace(tzinfo=None)
                )
            )
        except SQLAlchemyError as err:
            await self.session.rollback()
            raise HTTPException(
                status_code=500, detail=f"Database error: {str(err)}"
            ) from err
        except Exception as error:
            raise HTTPException(
                status_code=500,
                detail=f"Unexpected error while getting sub role: {str(error)}",
            ) from error
        
    async def update_sub_role(self,request: SubRoleIdBase):
        try:
            query = await self.session.execute(
                select(SubRoles).where(SubRoles.id == request.id)
            )

            query_data = query.scalars().first()

            if query_data:
                query_data.role_id = request.role_id
                query_data.sub_role_name = request.sub_role_name
                query_data.sub_role_description = request.sub_role_description
                query_data.is_active = request.is_active
                query_data.last_updated_by = request.last_updated_by
                query_data.last_updated_date = request.last_updated_date.replace(tzinfo=None)

                await self.session.commit()
                await self.session.refresh(query_data)

                return SubRoleFunctionResponse(
                    data_exist=True,
                    data=query_data
                )
            return SubRoleFunctionResponse(
                data_exist=False,
                data=SubRoleIdBase(
                    id=0,
                    role_id=0,
                    sub_role_name="",
                    sub_role_description="",
                    last_updated_by="",
                    last_updated_date=datetime.now(tz=timezone.utc).replace(tzinfo=None)
                )
            )
        except SQLAlchemyError as err:
            await self.session.rollback()
            raise HTTPException(
                status_code=500, detail=f"Database error: {str(err)}"
            ) from err
        except Exception as error:
            raise HTTPException(
                status_code=500,
                detail=f"Unexpected error while updating sub role: {str(error)}",
            ) from error
        
    async def delete_sub_role(self,sub_role_name: str):
        query = await self.session.execute(
            select(SubRoles).where(SubRoles.sub_role_name == sub_role_name)
        )

        query_data = query.scalars().first()

        if query_data:
            query_data.is_active = False

            await self.session.commit()
            await self.session.refresh(query_data)
            return SubRoleFunctionResponse(
                data_exist=True,
                data=query_data
            )
        return SubRoleFunctionResponse(
            data_exist=False,
            data=SubRoleIdBase(
                id=0,
                role_id=0,
                sub_role_name="",
                sub_role_description="",
                last_updated_by="",
                last_updated_date=datetime.now(tz=timezone.utc).replace(tzinfo=None)
            )
        )
