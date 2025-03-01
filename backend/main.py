import uvicorn
from models.flights import Flight
from database import Base, engine


Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    uvicorn.run("api:api", host="0.0.0.0", port=8081, reload=True)
