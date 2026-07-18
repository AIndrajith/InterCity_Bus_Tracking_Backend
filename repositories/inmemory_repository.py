from datetime import datetime
from typing import Optional, List

from models import BusRouterCreate, BusRouteResponse


class InMemoryBusRouteRepository:

    def __init__(self):
        self.routes = []
        self.next_id = 1


    async def create_route(self, route:BusRouterCreate) -> BusRouteResponse:
        new_route = BusRouteResponse(
            id= self.next_id,
            route_number=route.route_number,
            start_location=route.start_location,
            end_location=route.end_location,
            bus_type=route.bus_type,
            ticket_price=route.ticket_price,
            created_at=datetime.now()
        )

        self.routes.append(new_route)
        self.next_id += 1

        return new_route

    async def get_all(self)-> List[BusRouteResponse]:
        return self.routes

    async def get_route_by_id(self,route_id:int) -> Optional[BusRouteResponse]:
        for route in self.routes:
            if route.id == route_id:
                return route

        return None

    async def exist_by_route_number(self,route_number:str) -> bool:
        for route in self.routes:
            if route.route_number.lower() == route_number.lower():
                return True

        return False

    async def update_route(self,route_id:int, route:BusRouterCreate):
        for index, existing_route in enumerate(self.routes):
            if existing_route.id == route_id:
                updated_router = BusRouteResponse(
                    id = existing_route.id,
                    route_number= route.route_number,
                    start_location=route.start_location,
                    end_location=route.end_location,
                    bus_type=route.bus_type,
                    ticket_price=route.ticket_price,
                    created_at=datetime.now()
                )

                self.routes[index] = updated_router
                return updated_router
        return None

    async def delete_route(self,route_id:int) -> bool:
        for index,route in enumerate(self.routes):
            if route.id == route_id:
                del self.routes[index]
                return True

        return False