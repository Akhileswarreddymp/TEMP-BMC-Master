from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from master.models.api.roles_model import (
    RoleBase,
    RoleResponse,
    RoleBulkResponse,
    RoleBaseId,
)
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


@router.get("/get_all_roles/{status}")
async def get_roles(status: str, session: AsyncSession = Depends(get_session)):
    resp_obj = RolesService(session)

    resp_data = await resp_obj.get_all_roles(status)

    if resp_data.data_exists:
        return RoleBulkResponse(message="Success", data=resp_data.data)

    raise HTTPException(status_code=404, detail="No active roles exist in DB")


@router.get("/get_role/{role}")
async def get_role(role: str, session: AsyncSession = Depends(get_session)):
    resp_obj = RolesService(session)

    resp_data = await resp_obj.get_role(role)

    if resp_data.data_exists:
        return RoleResponse(message="Success", data=resp_data.data)

    raise HTTPException(
        status_code=404,
        detail=f"Data for {role} role does not exist in DB",
    )


@router.put("/update_role")
async def update_user(
    request: RoleBaseId, session: AsyncSession = Depends(get_session)
):
    resp_obj = RolesService(session)
    resp_data = await resp_obj.update_role(request)

    if resp_data.data_exists:
        return RoleResponse(message="Success", data=resp_data.data)

    raise HTTPException(
        status_code=404,
        detail=f"Data for {request.role} role does not exist in DB",
    )


@router.delete("/delete_role")
async def delete_role_temperarly(
    role: str, name: str, session: AsyncSession = Depends(get_session)
):
    resp_obj = RolesService(session)

    resp_data = await resp_obj.delete_role(role, name)

    if resp_data.data_exists:
        return RoleResponse(message="Success", data=resp_data.data)
    raise HTTPException(
        status_code=404,
        detail=f"Data for {role} role does not exist in DB",
    )
