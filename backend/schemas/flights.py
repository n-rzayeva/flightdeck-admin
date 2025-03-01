from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum
from typing import List


class FlightStatus(str, Enum):
    ON_TIME = "ON_TIME"
    DELAYED = "DELAYED"
    BOARDING = "BOARDING"
    CANCELLED = "CANCELLED"
    LANDED = "LANDED"


class FlightBase(BaseModel):
    flight_number: str = Field(..., example="XYZ123")
    departure_airport: str = Field(..., example="JFK")
    arrival_airport: str = Field(..., example="LAX")
    scheduled_time: datetime


class FlightCreate(FlightBase):
    status: FlightStatus = FlightStatus.ON_TIME


class FlightUpdate(BaseModel):
    status: FlightStatus


class FlightOut(FlightBase):
    id: int
    updated_times: List[datetime] | None
    status: FlightStatus

    class Config:
        from_attributes = True

