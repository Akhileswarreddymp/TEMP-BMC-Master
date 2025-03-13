from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select
from master.models.api.city_model import (
    CityBase,
    CityFunctionResp,
    CitiesFunctionResponse,
)
from master.models.database.models import Cities
from master.crud.base_backend import BaseBackend


class CityService(BaseBackend):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Cities)

    async def add_cities(self, request: CityBase) -> CityFunctionResp:
        try:
            query = await self.session.execute(
                select(Cities).where(Cities.code == request.code)
            )

            query_data = query.scalars().first()

            if query_data:
                return CityFunctionResp(data_exists=True, data=query_data)

            city_data = Cities(
                code=request.code,
                name=request.name,
                is_active=request.is_active if hasattr(request, "is_active") else True,
                last_updated_by=request.last_updated_by,
            )

            self.session.add(city_data)
            await self.session.commit()
            await self.session.refresh(city_data)

            return CityFunctionResp(data_exists=False, data=city_data)
        except SQLAlchemyError as err:
            await self.session.rollback()
            raise HTTPException(
                status_code=500, detail=f"Database error: {str(err)}"
            ) from err
        except Exception as error:
            raise HTTPException(
                status_code=500,
                detail=f"Unexpected error while adding cities: {str(error)}",
            ) from error

    async def get_user(self, code: str) -> CityFunctionResp:
        try:
            query = await self.session.execute(
                select(Cities).where(Cities.code == code)
            )

            query_data = query.scalars().first()

            if query_data:
                return CityFunctionResp(data_exists=True, data=query_data)

            return CityFunctionResp(
                data_exists=False,
                data=Cities(code=code, name="", is_active=False, last_updated_by=""),
            )
        except SQLAlchemyError as err:
            await self.session.rollback()
            raise HTTPException(
                status_code=500, detail=f"Database error: {str(err)}"
            ) from err
        except Exception as error:
            raise HTTPException(
                status_code=500,
                detail=f"Unexpected error while getting city: {str(error)}",
            ) from error

    async def get_all_cities(self) -> CitiesFunctionResponse:
        try:
            query = await self.session.execute(select(Cities).where(Cities.is_active))

            query_data = query.scalars().all()

            if query_data:
                return CitiesFunctionResponse(data_exists=True, data=query_data)

            return CitiesFunctionResponse(
                data_exists=False,
                data=[Cities(code="", name="", is_active=False, last_updated_by="")],
            )
        except SQLAlchemyError as err:
            await self.session.rollback()
            raise HTTPException(
                status_code=500, detail=f"Database error: {str(err)}"
            ) from err
        except Exception as error:
            raise HTTPException(
                status_code=500,
                detail=f"Unexpected error while getting cities: {str(error)}",
            ) from error

    async def update_cities(self, request: CityBase) -> CityFunctionResp:
        try:
            query = await self.session.execute(
                select(Cities).where(Cities.code == request.code)
            )

            query_data = query.scalars().first()

            if query_data:
                query_data.name = request.name
                query_data.is_active = (
                    request.is_active if hasattr(request, "is_active") else True
                )
                query_data.last_updated_by = request.last_updated_by

                await self.session.commit()
                await self.session.refresh(query_data)

                return CityFunctionResp(data_exists=True, data=query_data)

            return CityFunctionResp(
                data_exists=False,
                data=Cities(code="", name="", is_active=False, last_updated_by=""),
            )
        except SQLAlchemyError as err:
            await self.session.rollback()
            raise HTTPException(
                status_code=500, detail=f"Database error: {str(err)}"
            ) from err
        except Exception as error:
            raise HTTPException(
                status_code=500,
                detail=f"Unexpected error while adding cities: {str(error)}",
            ) from error

    async def delete_city(self, code: str):
        query = await self.session.execute(select(Cities).where(Cities.code == code))

        query_data = query.scalars().first()

        if query_data:
            query_data.is_active = False

            await self.session.commit()
            await self.session.refresh(query_data)

            return CityFunctionResp(data_exists=True, data=query_data)
        return CityFunctionResp(
            data_exists=False,
            data=Cities(code=code, name="", is_active=False, last_updated_by=""),
        )
