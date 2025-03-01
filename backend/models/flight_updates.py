from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class FlightUpdate(Base):
    __tablename__ = "flight_updates"

    id = Column(Integer, primary_key=True, index=True)
    flight_id = Column(Integer, ForeignKey("flights.id"), nullable=False)
    updated_time = Column(DateTime, nullable=False)

    flight = relationship("Flight", back_populates="updated_times")
