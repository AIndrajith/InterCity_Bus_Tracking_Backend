from idlelib import query
from math import dist
from typing import Optional, List

from database import create_db_connection
from models import BusRouterCreate, BusRouteResponse, BusRoutePatch


class DataBaseBusRouteRepository:
    async def create_route(self, route:BusRouterCreate) -> Optional[BusRouteResponse]:

        query = """
                INSERT into bus_routes (route_number, start_location, end_location, bus_type, ticket_price)
                VALUES ($1,$2,$3,$4,$5) RETURNING *;
        """

        conn = await create_db_connection()

        try:
            async with conn.transaction():
                new_bus_route = await conn.fetchrow(
                    query,route.route_number,route.start_location,route.end_location,route.bus_type, route.ticket_price
                )

                return BusRouteResponse(**dict(new_bus_route)) if new_bus_route else None

            # dict(new_bus_route) = {"route_number":"101","start_location":"moratuwa",...}
            # **dict(new_bus_route) = {route_number="101", start_location="moratuwa",... <- unpacking

        finally:
            await conn.close()


    async def get_all(self) -> List[BusRouteResponse]:
        query = "SELECT * FROM bus_routes ORDER BY id;"

        conn = await create_db_connection()
        print("Connected to Database")

        try:
            rows = await conn.fetch(query)
            return [BusRouteResponse (**(dict(row))) for row in rows]

        finally:
            await conn.close()

    async def exists_by_route_number(self,route_number:str) -> bool:
        query = """
            SELECT EXISTS (SELECT 1 FROM bus_routes WHERE LOWER(route_number) = LOWER($1));
        """

        conn = await create_db_connection()

        try:
            exists = await conn.fetchval(query, route_number)
            return exists
        finally:
            await conn.close()

    async def get_by_id(self,route_id:int) -> Optional[BusRouteResponse]:
        query = "SELECT * FROM bus_routes WHERE id=$1"

        conn = await create_db_connection()

        try:
            row = await conn.fetchrow(query,route_id)
            return BusRouteResponse(**dict(row)) if row else None

        finally:
            await conn.close()

    async def update_route(self,route_id:int, route:BusRouterCreate) -> Optional[BusRouteResponse]:
        query = """
            UPDATE bus_routes 
            SET route_number=$1,
                start_location=$2,
                end_location=$3,
                bus_type=$4,
                ticket_price=$5,
                updated_at=CURRENT_TIMESTAMP
            WHERE id=$6
            RETURNING * 
        """

        conn = await create_db_connection()
        try:
            async with conn.transaction():
                row = await conn.fetchrow(query, route.route_number, route.start_location, route.end_location,route.bus_type,route.ticket_price,route_id)
                return BusRouteResponse(**dict(row)) if row else None

        finally:
            await conn.close()


    async def delete_route(self,route_id:int) -> bool:
        query = """DELETE FROM bus_route WHERE id=$1"""

        conn = await create_db_connection()

        try:
            result = await conn.execute(query,route_id)
            return result == "DELETE 1"

        finally:
            await conn.close()

    async def patch_route(self,route_id, route:BusRoutePatch) -> Optional[BusRouteResponse]:
        query = """
            UPDATE bus_routes
            SET route_number = COALESCE($1, route_number),
                start_location = COALESCE($2,start_location),
                end_location = COALESCE($3,end_location),
                bus_type=COALESCE($4,bus_type),
                ticket_price=COALESCE($5,ticket_price)
            WHERE id = $6
            RETURNING *
        """

        conn = await create_db_connection()

        try:
            async with conn.transaction():
                row = await conn.fetchrow(
                    query,route.route_number,route.start_location,route.end_location,route.bus_type,route.ticket_price,route_id
                )
                return BusRouteResponse(**dict(row)) if row else None
        finally:
            await conn.close()

