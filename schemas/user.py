from pydantic import BaseModel


class User(BaseModel):
    email: str


class UserCreate(User):
    password: str


class UserOut(User):
    email: str
    is_active: bool
