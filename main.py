import uvicorn
from models.admin import Admin
from models.user import User
from database import Base, engine


Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8081, reload=True)  # "src.app:app"