from fastapi import Depends, Form, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordBearer
from models.user import User
from models.admin import Admin
from sqlalchemy.orm import Session
from schemas.user import UserCreate, UserLogin
from schemas.admin import AdminLogin
from settings import JWT_SECRET_KEY, JWT_REFRESH_SECRET_KEY, ALGORITHM
from jose import jwt, JWTError, ExpiredSignatureError
from utils import create_access_token, create_refresh_token, verify_password, get_hashed_password, is_token_expired
from database import get_db


app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_user_by_email(email: str, db: Session):
    """Fetch a user from the database by email."""
    return db.query(User).filter(User.email == email).first()


def get_admin_by_username(username: str, db: Session):
    """Fetch an admin from th database by username"""
    return db.query(Admin).filter(Admin.username == username).first()


def get_user_by_sub(sub: str, db: Session):
    """Helper function to fetch user/admin by subject (email/username)."""
    return get_user_by_email(sub, db) if "@" in sub else get_admin_by_username(sub, db)


def decode_and_validate_token(token: str, secret_key: str, check_expiration: bool = True):
    """Decodes a JWT token and returns subject & role. Returns None if invalid."""
    try:
        payload = jwt.decode(token, secret_key, algorithms=[ALGORITHM])
        sub = payload.get("sub")
        role = payload.get("role")
        exp = payload.get("exp")

        if not sub or (check_expiration and exp and not is_token_expired(exp)):
            return None, None, None

        return sub, role, exp
    except (ExpiredSignatureError, JWTError):
        return None, None, None


def determine_role(sub: str, user: User, role: str) -> str:
    """Helper function to determine the role of a user."""
    if role:
        return role
    if hasattr(user, "is_superadmin") and user.is_superadmin:
        return "superadmin"
    elif "@" in sub:
        return "user"
    return "admin"


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """Retrieve the current user and role from JWT token."""
    sub, role, _ = decode_and_validate_token(token, JWT_SECRET_KEY)

    if not sub:
        raise HTTPException(status_code=403, detail="Invalid or expired token")

    user = get_user_by_sub(sub, db)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.role = determine_role(sub, user, role)
    return user


def admin_required(user: User = Depends(get_current_user)):
    """Ensure the requester is an admin or superadmin."""
    if user.role not in ["admin", "superadmin"]:
        raise HTTPException(status_code=403, detail="Admin access required")
    return user


@app.post("/refresh")
async def refresh_access_token(refresh_token: str = Form(...), db: Session = Depends(get_db)):
    """Refreshes the access token using the refresh token."""
    sub, _, _ = decode_and_validate_token(refresh_token, JWT_REFRESH_SECRET_KEY, check_expiration=True)

    if not sub:
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")

    user = get_user_by_sub(sub, db)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    user.role = determine_role(sub, user, None)

    access_token = create_access_token(sub, user.role)

    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/signup")
async def signup(user: UserCreate, db: Session = Depends(get_db)):
    """Register a new user."""
    db_user = get_user_by_email(user.email, db)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = get_hashed_password(user.password)
    new_user = User(email=user.email, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User created successfully"}


@app.post("/login")
async def login(user: UserLogin, db: Session = Depends(get_db)):
    """Authenticate user and return an access token."""
    db_user = get_user_by_email(user.email, db)
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(db_user.email, "user")
    refresh_token = create_refresh_token(subject=db_user.email)

    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


@app.post("/admin/login")
async def admin_login(admin: AdminLogin, db: Session = Depends(get_db)):
    """Authenticate admin and return an access token."""
    db_admin = get_admin_by_username(admin.username, db)
    
    if not db_admin or not verify_password(admin.password, db_admin.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    role = "superadmin" if db_admin.is_superadmin else "admin"
    
    access_token = create_access_token(db_admin.username, role)
    refresh_token = create_refresh_token(subject=db_admin.username)
    
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


@app.get("/admin/dashboard")
async def admin_dashboard(user: User = Depends(admin_required)):
    return {"message": "Welcome to the admin dashboard!"}
