from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class BusRouterCreate(BaseModel):
    route_number : str = Field(...,min_length=3, max_length=50, description="Bus Route Number")
    start_location : str = Field(..., min_length=3, max_length=100, description="Trip start location")
    end_location : str = Field(..., min_length=3, max_length=100, description="Trip end location")
    bus_type : str = Field(..., min_length=3, description="Luxury | Super Luxury | Semi Luxury | Normal service")
    ticket_price : float = Field(..., gt=0, description="Strat location ticket price")

class BusRouteResponse(BusRouterCreate):
    id : int
    created_at:datetime
    updated_at:Optional[datetime] = None

class BusRoutePatch(BaseModel):
    route_number : Optional[str] = Field(None,min_length=3, max_length=50, description="Bus Route Number")
    start_location : Optional[str] = Field(None, min_length=3, max_length=100, description="Trip start location")
    end_location : Optional[str] = Field(None, min_length=3, max_length=100, description="Trip end location")
    bus_type : Optional[str] = Field(None, min_length=3, description="Luxury | Super Luxury | Semi Luxury | Normal service")
    ticket_price : Optional[float] = Field(None, gt=0, description="Strat location ticket price")