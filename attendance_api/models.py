from sqlalchemy import Column, Integer, String, Date, DateTime, Time, ForeignKey, Boolean, Float
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Employee(Base):
    __tablename__ = 'employees'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    code = Column(String, unique=True, nullable=False)
    department = Column(String)
    password_hash = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False)
    # ... add more fields as needed
    schedules = relationship('EmployeeSchedule', back_populates='employee')
    attendances = relationship('AttendanceRecord', back_populates='employee')
    leaves = relationship('Leave', back_populates='employee')

class Shift(Base):
    __tablename__ = 'shifts'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    grace_period = Column(Integer, default=0)  # minutes
    # ... add more fields as needed
    schedules = relationship('EmployeeSchedule', back_populates='shift')

class SchedulePeriod(Base):
    __tablename__ = 'schedule_periods'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    # e.g., 'summer', 'winter', 'ramadan'
    schedules = relationship('EmployeeSchedule', back_populates='period')

class EmployeeSchedule(Base):
    __tablename__ = 'employee_schedules'
    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey('employees.id'))
    shift_id = Column(Integer, ForeignKey('shifts.id'))
    period_id = Column(Integer, ForeignKey('schedule_periods.id'))
    effective_from = Column(Date, nullable=False)
    effective_to = Column(Date)
    auto_apply_period = Column(Boolean, default=True)  # If true, backend auto-selects period/shift
    employee = relationship('Employee', back_populates='schedules')
    shift = relationship('Shift', back_populates='schedules')
    period = relationship('SchedulePeriod', back_populates='schedules')

class AttendanceRecord(Base):
    __tablename__ = 'attendance_records'
    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey('employees.id'))
    date = Column(Date, nullable=False)
    in_time = Column(DateTime)
    out_time = Column(DateTime)
    employee = relationship('Employee', back_populates='attendances')

class AttendanceSummary(Base):
    __tablename__ = 'attendance_summaries'
    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey('employees.id'))
    date = Column(Date, nullable=False)
    late_minutes = Column(Integer)
    early_leave_minutes = Column(Integer)
    total_work_minutes = Column(Integer)
    # ... add more fields as needed

class LeaveType(Base):
    __tablename__ = 'leave_types'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    leaves = relationship('Leave', back_populates='leave_type')

class Leave(Base):
    __tablename__ = 'leaves'
    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey('employees.id'))
    leave_type_id = Column(Integer, ForeignKey('leave_types.id'))
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    approved = Column(Boolean, default=False)
    employee = relationship('Employee', back_populates='leaves')
    leave_type = relationship('LeaveType', back_populates='leaves')

class Holiday(Base):
    __tablename__ = 'holidays'
    id = Column(Integer, primary_key=True)
    year = Column(Integer, nullable=False)
    date = Column(Date, nullable=False)
    name = Column(String, nullable=False)
    description = Column(String)
    # ... add more fields as needed
