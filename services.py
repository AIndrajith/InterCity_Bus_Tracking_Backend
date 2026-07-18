from fastapi import HTTPException
from starlette import status

from models import BusRouterCreate, BusRoutePatch
from repositories.database_repository import DataBaseBusRouteRepository
from repositories.inmemory_repository import InMemoryBusRouteRepository


class BusRouteService:
    def __init__(self, repository:DataBaseBusRouteRepository):
        self.repository = repository

    async def create_route(self, route:BusRouterCreate):
        if await self.repository.exist_by_route_number(route.route_number):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="Bus Already Existes")

        return await self.repository.create_route(route)

    async def get_all_routes(self):
        return await self.repository.get_all()

    async def get_route_by_id(self, route_id:int):
        route = await self.repository.get_route_by_id(route_id)

        if route is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bus route not Found")

        return route

    async def update_route(self, route_id:int, route:BusRouterCreate):
        updated = await self.repository.update_route(route_id, route)

        if updated is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bus Route Not Found")

        return updated

    async def delete_route(self, route_id:int):
        # route = await self.repository.get_route_by_id(route_id)
        #
        # if route is None:
        #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bus route not Found")
        #
        # return self.repository.delete_route(route_id)

        deleted = await  self.repository.delete_route(route_id)

        if not deleted:
            raise  HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Bus route Not found")

        return {"message":f"{route_id} Bus route Deleted Successfully."}

    async def patch_route(self,route_id:int, route:BusRoutePatch):
        patched = await self.repository.patch_route(route_id,route)

        if patched is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bus route not found")

        return patched