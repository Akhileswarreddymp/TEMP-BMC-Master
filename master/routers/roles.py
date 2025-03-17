from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from master.models.api.roles_model import RoleBase, RoleResponse, RoleBulkResponse
from master.database import get_session
from master.crud.role import RolesService


router = APIRouter(
    prefix="/roles", default={404: {"description": "Page not found"}}, tags=["Roles"]
)


@router.post("/add_roles")
async def add_role(request: RoleBase, session: AsyncSession = Depends(get_session)):
    resp_obj = RolesService(session)

    resp_data = await resp_obj.add_roles(request)

    if resp_data.data_exists:
        return RoleResponse(
            message="Role already exist in database", data=resp_data.data
        )

    return RoleResponse(message="Success", data=resp_data.data)


@router.get("/get_all_roles")
async def get_roles(
    session: AsyncSession = Depends(get_session)
):
    resp_obj = RolesService(session)

    resp_data = await resp_obj.get_all_roles()

    if resp_data.data_exists:
        return RoleBulkResponse(
            message="Success",
            data=resp_data.data
        )
    
    raise HTTPException(
        status_code=404,
        detail={"No active roles exist in DB"}
    )


@router.get("/get_role/{role}")
async def get_role(
    role: str, session: AsyncSession = Depends(get_session)
):
    resp_obj = RolesService(session)

    resp_data = await resp_obj.get_role(role)

    if resp_data.data_exists:
        return RoleResponse(
            message="Success", data=resp_data.data
        )
    
    raise HTTPException(
        status_code=404,
        detail=f"Data for {role} role does not exist in DB",
    )
