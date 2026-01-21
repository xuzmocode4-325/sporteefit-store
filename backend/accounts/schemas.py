from ninja import Schema, UploadedFile, File
from typing import Optional
from pydantic import EmailStr

# -------------------------------------------------
# USER SCHEMAS
# -------------------------------------------------
class UserBaseSchema(Schema):
    id: int
    username: str
    email: EmailStr
    is_active: bool
    is_staff: bool

    class Config:
        from_attributes = True


class UserRegisterSchema(Schema):
    username: str
    email: EmailStr
    password: str


class UserLoginSchema(Schema):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: str


class UserOutSchema(Schema):
    id: int
    username: str
    email: EmailStr
    name: str
    surname: str
    is_active: bool
    is_staff: bool

    class Config:
        from_attributes = True


class UserUpdateSchema(Schema):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    name: Optional[str] = None
    surname: Optional[str] = None
    is_active: Optional[bool] = None
    is_staff: Optional[bool] = None


# -------------------------------------------------
# PROFILE SCHEMAS
# -------------------------------------------------
class ProfileBaseSchema(Schema):
    id: int
    name: str
    surname: str
    image: Optional[str] = None

    class Config:
        from_attributes = True


class ProfileUpdateSchema(Schema):
    name: Optional[str] = None
    surname: Optional[str] = None


# -------------------------------------------------
# ADMIN MANAGEMENT
# -------------------------------------------------
class AdminCreateUserSchema(Schema):
    username: str
    email: EmailStr
    password: str
    name: str
    surname: str
    is_active: bool = True
    is_staff: bool = False


class AdminUserUpdateSchema(Schema):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    name: Optional[str] = None
    surname: Optional[str] = None
    is_active: Optional[bool] = None
    is_staff: Optional[bool] = None
