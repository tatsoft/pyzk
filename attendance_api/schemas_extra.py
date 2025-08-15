from pydantic import BaseModel
from typing import Optional, List
from datetime import date, datetime, time

# Employee schemas already defined in schemas.py

class ShiftBase(BaseModel):
    name: str
    start_time: time
    end_time: time
    grace_period: Optional[int] = 0

class ShiftCreate(ShiftBase):
    pass

class ShiftUpdate(BaseModel):
    name: Optional[str] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    grace_period: Optional[int] = None

class ShiftOut(ShiftBase):
    id: int
    class Config:
        orm_mode = True

class SchedulePeriodBase(BaseModel):
    name: str
    start_date: date
    end_date: date

class SchedulePeriodCreate(SchedulePeriodBase):
    pass

class SchedulePeriodUpdate(BaseModel):
    name: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None

class SchedulePeriodOut(SchedulePeriodBase):
    id: int
    class Config:
        orm_mode = True


class EmployeeScheduleBase(BaseModel):
    employee_id: int
    shift_id: int
    period_id: int
    effective_from: date
    effective_to: Optional[date] = None
    auto_apply_period: Optional[bool] = True


class EmployeeScheduleCreate(EmployeeScheduleBase):
    pass


class EmployeeScheduleUpdate(BaseModel):
    shift_id: Optional[int] = None
    period_id: Optional[int] = None
    effective_from: Optional[date] = None
    effective_to: Optional[date] = None
    auto_apply_period: Optional[bool] = None


class EmployeeScheduleOut(EmployeeScheduleBase):
    id: int
    class Config:
        orm_mode = True

class AttendanceRecordBase(BaseModel):
    employee_id: int
    date: date
    in_time: Optional[datetime] = None
    out_time: Optional[datetime] = None

class AttendanceRecordCreate(AttendanceRecordBase):
    pass

class AttendanceRecordUpdate(BaseModel):
    in_time: Optional[datetime] = None
    out_time: Optional[datetime] = None

class AttendanceRecordOut(AttendanceRecordBase):
    id: int
    class Config:
        orm_mode = True

class AttendanceSummaryBase(BaseModel):
    employee_id: int
    date: date
    late_minutes: Optional[int] = None
    early_leave_minutes: Optional[int] = None
    total_work_minutes: Optional[int] = None

class AttendanceSummaryCreate(AttendanceSummaryBase):
    pass

class AttendanceSummaryUpdate(BaseModel):
    late_minutes: Optional[int] = None
    early_leave_minutes: Optional[int] = None
    total_work_minutes: Optional[int] = None

class AttendanceSummaryOut(AttendanceSummaryBase):
    id: int
    class Config:
        orm_mode = True

class LeaveTypeBase(BaseModel):
    name: str
    description: Optional[str] = None

class LeaveTypeCreate(LeaveTypeBase):
    pass

class LeaveTypeUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class LeaveTypeOut(LeaveTypeBase):
    id: int
    class Config:
        orm_mode = True

class LeaveBase(BaseModel):
    employee_id: int
    leave_type_id: int
    start_date: date
    end_date: date
    approved: Optional[bool] = False

class LeaveCreate(LeaveBase):
    pass

class LeaveUpdate(BaseModel):
    leave_type_id: Optional[int] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    approved: Optional[bool] = None

class LeaveOut(LeaveBase):
    id: int
    class Config:
        orm_mode = True

class HolidayBase(BaseModel):
    year: int
    date: date
    name: str
    description: Optional[str] = None

class HolidayCreate(HolidayBase):
    pass

class HolidayUpdate(BaseModel):
    year: Optional[int] = None
    date: Optional[date] = None
    name: Optional[str] = None
    description: Optional[str] = None

class HolidayOut(HolidayBase):
    id: int
    class Config:
        orm_mode = True
