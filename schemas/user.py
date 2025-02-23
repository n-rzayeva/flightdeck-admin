from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr


class UserLogin(UserBase):
    password: str


class UserCreate(UserLogin):
    pass


class UserOut(UserBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True  
