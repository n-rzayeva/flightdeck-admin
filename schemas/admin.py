from pydantic import BaseModel, EmailStr


class AdminBase(BaseModel):
    username: str


class AdminLogin(AdminBase):
    password: str


class AdminOut(AdminBase):
    id: int
    full_name: str
    email: str
    role: str

    class Config:
        from_attributes = True  
