from sqlalchemy import Column, Integer, String, DateTime, Enum
from sqlalchemy.orm import relationship
from database import Base
import enum


class FlightStatus(enum.Enum):
    ON_TIME = "ON_TIME"
    DELAYED = "DELAYED"
    BOARDING = "BOARDING"
    CANCELLED = "CANCELLED"
    LANDED = "LANDED"


class Flight(Base):
    __tablename__ = "flights"

    id = Column(Integer, primary_key=True, index=True)
    flight_number = Column(String, unique=True, index=True, nullable=False)
    departure_airport = Column(String, nullable=False)
    arrival_airport = Column(String, nullable=False)
    scheduled_time = Column(DateTime, nullable=False, index=True)
    updated_time = Column(DateTime, nullable=True)
    status = Column(Enum(FlightStatus), default=FlightStatus.ON_TIME, nullable=False)
    updated_times = relationship("FlightUpdate", back_populates="flight")


