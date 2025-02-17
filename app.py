from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import List
from models import User  # Your user model, with roles, for example


app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_current_user(token: str = Depends(oauth2_scheme)):
    
    user = get_user_from_token(token)  # Replace with your logic
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    return user


def admin_required(user: User = Depends(get_current_user)):
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return user


@app.post("/signup")
async def signup(user: UserCreate):
    # Registration logic
    pass


@app.post("/login")
async def login(user: UserLogin):
    # Login logic
    pass


@app.get("/admin/dashboard")
async def admin_dashboard(user: User = Depends(admin_required)):
    return {"message": "Welcome to the admin dashboard!"}


@app.post("/admin/login")
async def admin_login():
    # Admin login logic
    pass
