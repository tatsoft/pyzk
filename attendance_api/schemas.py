from pydantic import BaseModel
from typing import Optional


class EmployeeBase(BaseModel):
    name: str
    code: str
    department: Optional[str] = None


class EmployeeCreate(EmployeeBase):
    password: str
    is_admin: Optional[bool] = False


class EmployeeUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    department: Optional[str] = None
    password: Optional[str] = None
    is_admin: Optional[bool] = None


class EmployeeOut(EmployeeBase):
    id: int
    is_admin: bool

    class Config:
        orm_mode = True
