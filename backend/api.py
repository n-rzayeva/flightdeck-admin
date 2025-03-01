from fastapi import FastAPI, Request, HTTPException, Depends, Security, WebSocket, WebSocketDisconnect
from fastapi.security.api_key import APIKeyHeader
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from schemas.flights import FlightCreate, FlightUpdate, FlightOut
from models.flights import Flight, FlightStatus
from database import get_db
from config import API_KEY
from typing import List


api = FastAPI()

api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api_key_header = APIKeyHeader(name="X-API-KEY", auto_error=True)


def check_api_key(api_key: str = Security(api_key_header)):
    """Function to check API key"""
    if api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized: Invalid API Key")


@api.get("/flights/{flight_number}", response_model=FlightOut)
def get_flight_by_number(flight_number: str, db: Session = Depends(get_db)):
    flight = db.query(Flight).filter(Flight.flight_number == flight_number).first()
    if not flight:
        raise HTTPException(status_code=404, detail="Flight not found")
    return flight


@api.post("/flights", response_model=List[FlightOut])
def create_flights(
    flights: List[FlightCreate],
    db: Session = Depends(get_db),
    api_key: str = Depends(check_api_key)
):
    """Insert multiple flights into the database."""
    inserted_flights = []
    for flight in flights:
        db_flight = Flight(**flight.dict())
        db.add(db_flight)
        db.commit()
        db.refresh(db_flight)
        inserted_flights.append(db_flight)
    
    return inserted_flights


@api.patch("/flights/{flight_id}", response_model=FlightOut)
def update_flight(flight_id: int, flight_update: FlightUpdate, request: Request, db: Session = Depends(get_db)):
    check_api_key(request)
    flight = db.query(Flight).filter(Flight.id == flight_id).first()
    # To Do
    if not flight:
        raise HTTPException(status_code=404, detail="Flight not found")
    flight.status = flight_update.status
    db.commit()
    db.refresh(flight)
    return flight


@api.delete("/flights/{flight_id}", response_model=FlightOut)
def delete_flight(flight_id: int, request: Request, db: Session = Depends(get_db)):
    check_api_key(request)
    flight = db.query(Flight).filter(Flight.id == flight_id).first()
    # To Do
    if not flight:
        raise HTTPException(status_code=404, detail="Flight not found")
    db.delete(flight)
    db.commit()
    return flight


@api.get("/notifications")
def get_notifications():
    # To Do
    return {"message": "Real-time flight updates will be here."}


@api.websocket("/flights/updates")
async def websocket_flight_updates(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            # To Do
            await websocket.send_text("Live flight updates here!")
    except WebSocketDisconnect:
        print("Client disconnected")
