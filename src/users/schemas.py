from typing import Optional

from pydantic import BaseModel


class UserBase(BaseModel):
    user_id: str
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    post_code: Optional[str] = None
    membership_code: Optional[str] = None


    class Config:
        orm_mode = True

class UserBaseInput(BaseModel):
    user_id: str
    password: str
    name: str
    email: str
    phone: str
    address: str
    post_code: str

    class Config:
        orm_mode = True
