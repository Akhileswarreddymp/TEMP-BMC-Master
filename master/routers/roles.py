from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from master.models.api.roles_model import RoleBase, RoleResponse
from master.database import get_session
from master.crud.role import RolesService


router = APIRouter(
    prefix="/roles",
    default={404: {"description": "Page not found"}},
    tags=["Roles"]
)


@router.post("/add_roles")
async def add_role(
    request: RoleBase,
    session: AsyncSession = Depends(get_session)
):
    resp_obj = RolesService(session)

    resp_data = await resp_obj.add_roles(request)

    if resp_data.data_exists:
        return RoleResponse(
            message="Role already exist in database",
            data=resp_data.data
        )
    
    return RoleResponse(
        message="Success",
        data=resp_data.data
    )
