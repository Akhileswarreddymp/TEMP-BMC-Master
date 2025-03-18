from fastapi import APIRouter,Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from master.database import get_session
from master.models.api.sub_role_model import SubRoleBase, SubRoleIdBase, SubRoleResponse, SubRoleResponses
from master.crud.sub_role import SubRoleService

router = APIRouter(
    prefix="/sub_role",
    default={404: {"description": "Page not found"}},
    tags=["Sub Roles"]
)


@router.post("/add_sub_role")
async def add_sub_role(
    request: SubRoleBase,
    session: AsyncSession = Depends(get_session)
):
    resp_obj = SubRoleService(session)

    resp_data = await resp_obj.add_sub_role(request)

    if resp_data.data_exist:
        return SubRoleResponse(
            message="Data already exists",
            data=resp_data.data
        )
    
    return SubRoleResponse(
        message="Success",
        data=resp_data.data
    )

@router.get("/get_all_sub_roles/{status}")
async def get_all_sub_roles(
    status: str,
    session: AsyncSession = Depends(get_session)
):
    resp_obj = SubRoleService(session)

    resp_data = await resp_obj.get_all_sub_roles(status)

    if resp_data.data_exist:
        return SubRoleResponses(
            message="Success",
            data=resp_data.data
        )
    
    return HTTPException(
        status_code=404,
        detail="No sub role data exists"
    )


@router.get("/get_sub_role/{sub_role_name}")
async def get_sub_role_data(
    sub_role_name: str,
    session: AsyncSession = Depends(get_session)
):
    resp_obj = SubRoleService(session)

    resp_data = await resp_obj.get_sub_role(sub_role_name)

    if resp_data.data_exist:
        return SubRoleResponse(
            message="Success",
            data=resp_data.data
        )
    
    raise HTTPException(
        status_code=404,
        detail=f"{sub_role_name} sub role data does not exist in db"
    )


@router.put("/update_sub_role")
async def update_sub_role(
    request: SubRoleIdBase,
    session: AsyncSession = Depends(get_session)
):
    resp_obj = SubRoleService(session)

    resp_data = await resp_obj.update_sub_role(request)

    if resp_data.data_exist:
        return SubRoleResponse(
            message="Success",
            data=resp_data.data
        )
    
    raise HTTPException(
        status_code=404,
        detail=f"sub role data does not exist in db"
    )

@router.delete("/delete_sub_role")
async def temp_delete_sub_role(
    sub_role_name: str,
    session: AsyncSession = Depends(get_session)
):
    resp_obj = SubRoleService(session)

    resp_data = await resp_obj.delete_sub_role(sub_role_name)

    if resp_data.data_exist:
        return SubRoleResponse(
            message="Success",
            data=resp_data.data
        )
    
    raise HTTPException(
        status_code=404,
        detail=f"{sub_role_name} sub role data does not exist in db"
    )
