from typing import List

from fastapi import APIRouter
from starlette import status

from models import BusRouterCreate, BusRouteResponse, BusRoutePatch
from repositories.database_repository import DataBaseBusRouteRepository
from repositories.inmemory_repository import InMemoryBusRouteRepository
from services import BusRouteService

router = APIRouter(
    prefix="/routes",
    tags= ["Bus Routes"]
)

repository = DataBaseBusRouteRepository()
service = BusRouteService(repository)

@router.post("/", response_model=BusRouteResponse, status_code=status.HTTP_201_CREATED)
async def create_route(route: BusRouterCreate):
    return await service.create_route(route)

@router.get("/",response_model=List[BusRouterCreate], status_code=status.HTTP_200_OK)
async def get_all():
    return await service.get_all_routes()

@router.get("/{route_id}", response_model=BusRouteResponse, status_code=status.HTTP_200_OK)
async def get_route_by_id(route_id:int):
    return await service.get_route_by_id(route_id)

@router.put("/{route_id}", response_model=BusRouteResponse, status_code=status.HTTP_201_CREATED)
async def update_route(route_id:int, route:BusRouterCreate):
    return await service.repository.update_route(route_id,route)

@router.delete("/{route_id}",status_code=status.HTTP_200_OK)
async def delete_route(route_id:int):
    return await service.delete_route(route_id)

@router.patch("/{route_id}", status_code=status.HTTP_201_CREATED)
async def patch_route(route_id:int, route:BusRoutePatch):
    return await service.patch_route(route_id, route)