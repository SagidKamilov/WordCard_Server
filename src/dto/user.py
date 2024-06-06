from pydantic import BaseModel


class UserAuth(BaseModel):
    username: str
    password: str


class UserCreateHashPassword(BaseModel):
    username: str
    name: str
    hashed_password: str


class UserCreate(BaseModel):
    username: str
    name: str
    password: str


class UserUpdateHashedPassword(BaseModel):
    username: str = None
    name: str = None
    hashed_password: str = None


class UserUpdate(BaseModel):
    username: str
    name: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    name: str


class UserResponseMin(BaseModel):
    id: int
    username: str
