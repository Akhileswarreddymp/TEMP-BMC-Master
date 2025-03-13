from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from master.models.api.city_model import CityBase,CityResponse,CitiesBulkResponse
from master.database import get_session
from master.crud.city import CityService


router = APIRouter(
    prefix="/master",
    responses={404:{"description":"Not Found"}},
    tags=["Master"]
)


@router.post("/add_cities")
async def add_cities(
    request: CityBase,
    session: AsyncSession = Depends(get_session)
)->CityResponse:
    res_obj = CityService(session)

    resp_data = await res_obj.add_cities(request)

    if resp_data.data_exists:
        return CityResponse(
            message="City already Exists",
            data=resp_data.data
        )
    return CityResponse(
        message="Success",
        data=resp_data.data
    )

@router.get("/get_user/{code}")
async def get_city_by_code(
    code: str,
    session:AsyncSession = Depends(get_session)
)->CityResponse:
    resp_obj = CityService(session)

    resp_data = await resp_obj.get_user(code)

    if resp_data.data_exists:
        return CityResponse(
            message="Success",
            data=resp_data.data
        )
    
    raise HTTPException(
        status_code= 404,
        detail=f"Data not found with city code as {code}"
    )


@router.get("/get_all_cities")
async def  get_all_cities(
    session: AsyncSession = Depends(get_session)
):
    resp_obj = CityService(session)

    resp_data = await resp_obj.get_all_cities()

    if resp_data:
        return CitiesBulkResponse(
            message="Success",
            data=resp_data.data
        )
    
    raise HTTPException(
        status_code=404,
        detail="City details are not available"
    )

@router.put("/update_cities")
async def update_city_data(
    request: CityBase,
    session: AsyncSession = Depends(get_session)
):
    res_obj = CityService(session)

    resp_data = await res_obj.update_cities(request)

    if resp_data.data_exists:
        return CityResponse(
            message="Success",
            data=resp_data.data
        )
    
    raise HTTPException(
        status_code=404,
        detail=f"Data not found with city code {resp_data.data.code}"
    )

@router.delete("/inactivate_city")
async def partial_delete_city(
    city_code: str,
    session: AsyncSession = Depends(get_session)
):
    resp_obj = CityService(session)

    resp_data = await resp_obj.delete_city(city_code)

    if resp_data.data_exists:
        return CityResponse(
            message="Success",
            data=resp_data.data
        )
    
    raise HTTPException(
        status_code=404,
        detail=f"Data with {resp_data.data.code} is not found"
    )