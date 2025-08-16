from sqlalchemy.exc import SQLAlchemyError
import socket
# Health check endpoints
@app.get("/health/db")
def health_db(db: Session = Depends(get_db)):
    try:
        # Simple query to check DB connection
        db.execute("SELECT 1")
        return {"status": "ok"}
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database not reachable")

# Dummy device health check (replace with real check as needed)
@app.get("/health/device")
def health_device():
    # Example: try to connect to device IP/port (replace with real logic)
    DEVICE_IP = "192.168.1.201"  # <-- set your device IP
    DEVICE_PORT = 4370            # <-- set your device port
    try:
        with socket.create_connection((DEVICE_IP, DEVICE_PORT), timeout=2):
            return {"status": "ok"}
    except Exception:
        raise HTTPException(status_code=500, detail="Device not reachable")
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from attendance_api.database import init_db
from attendance_api.models import Employee, Shift, SchedulePeriod, EmployeeSchedule, AttendanceRecord, AttendanceSummary, LeaveType, Leave, Holiday
from attendance_api.schemas import EmployeeCreate, EmployeeUpdate, EmployeeOut
from attendance_api.schemas_extra import (
    ShiftCreate, ShiftUpdate, ShiftOut,
    SchedulePeriodCreate, SchedulePeriodUpdate, SchedulePeriodOut,
    EmployeeScheduleCreate, EmployeeScheduleUpdate, EmployeeScheduleOut,
    AttendanceRecordCreate, AttendanceRecordUpdate, AttendanceRecordOut,
    AttendanceSummaryCreate, AttendanceSummaryUpdate, AttendanceSummaryOut,
    LeaveTypeCreate, LeaveTypeUpdate, LeaveTypeOut,
    LeaveCreate, LeaveUpdate, LeaveOut,
    HolidayCreate, HolidayUpdate, HolidayOut
)
from attendance_api.auth import (
    get_password_hash, verify_password, create_access_token,
    get_current_user, get_current_admin, get_db
)
from fastapi.security import OAuth2PasswordRequestForm
from typing import List
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vue dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add login endpoint
@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(Employee).filter(Employee.code == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    # Include is_admin in the token payload for frontend
    access_token = create_access_token(data={"sub": user.id, "is_admin": user.is_admin})
    return {"access_token": access_token, "token_type": "bearer"}

@app.on_event("startup")
def on_startup():
    init_db()


# Employee CRUD endpoints (admin only for create/delete/list, self or admin for get/update)
@app.post("/employees/", response_model=EmployeeOut, status_code=201)
def create_employee(employee: EmployeeCreate, db: Session = Depends(get_db), admin: Employee = Depends(get_current_admin)):
    db_employee = Employee(
        name=employee.name,
        code=employee.code,
        department=employee.department,
        password_hash=get_password_hash(employee.password),
        is_admin=employee.is_admin or False
    )
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee

@app.get("/employees/", response_model=List[EmployeeOut])
def read_employees(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), admin: Employee = Depends(get_current_admin)):
    return db.query(Employee).offset(skip).limit(limit).all()

@app.get("/employees/{employee_id}", response_model=EmployeeOut)
def read_employee(employee_id: int, db: Session = Depends(get_db), current_user: Employee = Depends(get_current_user)):
    emp = db.query(Employee).filter(Employee.id == employee_id).first()
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    # Only admin or the employee themselves can view
    if not current_user.is_admin and current_user.id != emp.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    return emp

@app.put("/employees/{employee_id}", response_model=EmployeeOut)
def update_employee(employee_id: int, employee: EmployeeUpdate, db: Session = Depends(get_db), current_user: Employee = Depends(get_current_user)):
    db_employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not db_employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    # Only admin or the employee themselves can update
    if not current_user.is_admin and current_user.id != db_employee.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    for var, value in vars(employee).items():
        if value is not None:
            if var == "password":
                db_employee.password_hash = get_password_hash(value)
            elif var == "is_admin" and not current_user.is_admin:
                continue  # Only admin can change admin status
            else:
                setattr(db_employee, var, value)
    db.commit()
    db.refresh(db_employee)
    return db_employee

@app.delete("/employees/{employee_id}")
def delete_employee(employee_id: int, db: Session = Depends(get_db), admin: Employee = Depends(get_current_admin)):
    db_employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not db_employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    db.delete(db_employee)
    db.commit()
    return {"ok": True}

# Shift CRUD endpoints
@app.post("/shifts/", response_model=ShiftOut)
def create_shift(shift: ShiftCreate, db: Session = Depends(get_db)):
    db_shift = Shift(**shift.dict())
    db.add(db_shift)
    db.commit()
    db.refresh(db_shift)
    return db_shift

@app.get("/shifts/", response_model=List[ShiftOut])
def read_shifts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Shift).offset(skip).limit(limit).all()

@app.get("/shifts/{shift_id}", response_model=ShiftOut)
def read_shift(shift_id: int, db: Session = Depends(get_db)):
    shift = db.query(Shift).filter(Shift.id == shift_id).first()
    if not shift:
        raise HTTPException(status_code=404, detail="Shift not found")
    return shift

@app.put("/shifts/{shift_id}", response_model=ShiftOut)
def update_shift(shift_id: int, shift: ShiftUpdate, db: Session = Depends(get_db)):
    db_shift = db.query(Shift).filter(Shift.id == shift_id).first()
    if not db_shift:
        raise HTTPException(status_code=404, detail="Shift not found")
    for var, value in vars(shift).items():
        if value is not None:
            setattr(db_shift, var, value)
    db.commit()
    db.refresh(db_shift)
    return db_shift

@app.delete("/shifts/{shift_id}")
def delete_shift(shift_id: int, db: Session = Depends(get_db)):
    db_shift = db.query(Shift).filter(Shift.id == shift_id).first()
    if not db_shift:
        raise HTTPException(status_code=404, detail="Shift not found")
    db.delete(db_shift)
    db.commit()
    return {"ok": True}

# SchedulePeriod CRUD endpoints
@app.post("/schedule_periods/", response_model=SchedulePeriodOut)
def create_schedule_period(period: SchedulePeriodCreate, db: Session = Depends(get_db)):
    db_period = SchedulePeriod(**period.dict())
    db.add(db_period)
    db.commit()
    db.refresh(db_period)
    return db_period

@app.get("/schedule_periods/", response_model=List[SchedulePeriodOut])
def read_schedule_periods(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(SchedulePeriod).offset(skip).limit(limit).all()

@app.get("/schedule_periods/{period_id}", response_model=SchedulePeriodOut)
def read_schedule_period(period_id: int, db: Session = Depends(get_db)):
    period = db.query(SchedulePeriod).filter(SchedulePeriod.id == period_id).first()
    if not period:
        raise HTTPException(status_code=404, detail="Schedule period not found")
    return period

@app.put("/schedule_periods/{period_id}", response_model=SchedulePeriodOut)
def update_schedule_period(period_id: int, period: SchedulePeriodUpdate, db: Session = Depends(get_db)):
    db_period = db.query(SchedulePeriod).filter(SchedulePeriod.id == period_id).first()
    if not db_period:
        raise HTTPException(status_code=404, detail="Schedule period not found")
    for var, value in vars(period).items():
        if value is not None:
            setattr(db_period, var, value)
    db.commit()
    db.refresh(db_period)
    return db_period

@app.delete("/schedule_periods/{period_id}")
def delete_schedule_period(period_id: int, db: Session = Depends(get_db)):
    db_period = db.query(SchedulePeriod).filter(SchedulePeriod.id == period_id).first()
    if not db_period:
        raise HTTPException(status_code=404, detail="Schedule period not found")
    db.delete(db_period)
    db.commit()
    return {"ok": True}

# EmployeeSchedule CRUD endpoints

@app.post("/employee_schedules/", response_model=EmployeeScheduleOut)
def create_employee_schedule(es: EmployeeScheduleCreate, db: Session = Depends(get_db)):
    # Prevent overlapping schedules for the same employee
    overlap = db.query(EmployeeSchedule).filter(
        EmployeeSchedule.employee_id == es.employee_id,
        EmployeeSchedule.effective_from <= (es.effective_to or es.effective_from),
        (EmployeeSchedule.effective_to == None) | (EmployeeSchedule.effective_to >= es.effective_from)
    ).first()
    if overlap:
        raise HTTPException(status_code=400, detail="Overlapping schedule exists for this employee in the given period")
    db_es = EmployeeSchedule(**es.dict())
    db.add(db_es)
    db.commit()
    db.refresh(db_es)
    return db_es

@app.get("/employee_schedules/", response_model=List[EmployeeScheduleOut])
def read_employee_schedules(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(EmployeeSchedule).offset(skip).limit(limit).all()

@app.get("/employee_schedules/{es_id}", response_model=EmployeeScheduleOut)
def read_employee_schedule(es_id: int, db: Session = Depends(get_db)):
    es = db.query(EmployeeSchedule).filter(EmployeeSchedule.id == es_id).first()
    if not es:
        raise HTTPException(status_code=404, detail="Employee schedule not found")
    return es


@app.put("/employee_schedules/{es_id}", response_model=EmployeeScheduleOut)
def update_employee_schedule(es_id: int, es: EmployeeScheduleUpdate, db: Session = Depends(get_db)):
    db_es = db.query(EmployeeSchedule).filter(EmployeeSchedule.id == es_id).first()
    if not db_es:
        raise HTTPException(status_code=404, detail="Employee schedule not found")
    # Prevent overlapping schedules for the same employee (excluding current)
    new_from = es.effective_from or db_es.effective_from
    new_to = es.effective_to if es.effective_to is not None else db_es.effective_to
    overlap = db.query(EmployeeSchedule).filter(
        EmployeeSchedule.employee_id == db_es.employee_id,
        EmployeeSchedule.id != es_id,
        EmployeeSchedule.effective_from <= (new_to or new_from),
        (EmployeeSchedule.effective_to == None) | (EmployeeSchedule.effective_to >= new_from)
    ).first()
    if overlap:
        raise HTTPException(status_code=400, detail="Overlapping schedule exists for this employee in the given period")
    for var, value in vars(es).items():
        if value is not None:
            setattr(db_es, var, value)
    db.commit()
    db.refresh(db_es)
    return db_es

@app.delete("/employee_schedules/{es_id}")
def delete_employee_schedule(es_id: int, db: Session = Depends(get_db)):
    db_es = db.query(EmployeeSchedule).filter(EmployeeSchedule.id == es_id).first()
    if not db_es:
        raise HTTPException(status_code=404, detail="Employee schedule not found")
    db.delete(db_es)
    db.commit()
    return {"ok": True}

# AttendanceRecord CRUD endpoints

def calculate_attendance_summary(db, ar):
    # Get employee schedule for the date
    es = db.query(EmployeeSchedule).filter(
        EmployeeSchedule.employee_id == ar.employee_id,
        EmployeeSchedule.effective_from <= ar.date,
        (EmployeeSchedule.effective_to == None) | (EmployeeSchedule.effective_to >= ar.date)
    ).first()
    if not es:
        return None
    # If auto_apply_period, select correct period/shift for the date
    if es.auto_apply_period:
        period = db.query(SchedulePeriod).filter(SchedulePeriod.start_date <= ar.date, SchedulePeriod.end_date >= ar.date).first()
        if period:
            es.period_id = period.id
            # Optionally, select a shift based on period (if you have such mapping)
            # For now, keep the assigned shift
    shift = db.query(Shift).filter(Shift.id == es.shift_id).first()
    if not shift or not ar.in_time or not ar.out_time:
        return None
    # Calculate late/early/total
    shift_start = ar.in_time.replace(hour=shift.start_time.hour, minute=shift.start_time.minute, second=0, microsecond=0)
    shift_end = ar.in_time.replace(hour=shift.end_time.hour, minute=shift.end_time.minute, second=0, microsecond=0)
    late_minutes = max(0, int((ar.in_time - shift_start).total_seconds() // 60) - (shift.grace_period or 0))
    early_leave_minutes = max(0, int((shift_end - ar.out_time).total_seconds() // 60))
    total_work_minutes = int((ar.out_time - ar.in_time).total_seconds() // 60)
    return dict(
        employee_id=ar.employee_id,
        date=ar.date,
        late_minutes=late_minutes,
        early_leave_minutes=early_leave_minutes,
        total_work_minutes=total_work_minutes
    )

@app.post("/attendance_records/", response_model=AttendanceRecordOut)
def create_attendance_record(ar: AttendanceRecordCreate, db: Session = Depends(get_db)):
    # Validation: in_time before out_time
    if ar.in_time and ar.out_time and ar.in_time >= ar.out_time:
        raise HTTPException(status_code=400, detail="in_time must be before out_time")
    # Prevent duplicate attendance
    exists = db.query(AttendanceRecord).filter(AttendanceRecord.employee_id == ar.employee_id, AttendanceRecord.date == ar.date).first()
    if exists:
        raise HTTPException(status_code=400, detail="Attendance record already exists for this employee and date")
    # Prevent attendance on leave days
    leave = db.query(Leave).filter(Leave.employee_id == ar.employee_id, Leave.start_date <= ar.date, Leave.end_date >= ar.date, Leave.approved == True).first()
    if leave:
        raise HTTPException(status_code=400, detail="Employee is on approved leave for this date")
    # Prevent attendance on holidays
    holiday = db.query(Holiday).filter(Holiday.date == ar.date).first()
    if holiday:
        raise HTTPException(status_code=400, detail="This date is a holiday")
    db_ar = AttendanceRecord(**ar.dict())
    db.add(db_ar)
    db.commit()
    db.refresh(db_ar)
    # Calculate and store summary
    summary_data = calculate_attendance_summary(db, db_ar)
    if summary_data:
        db_summary = AttendanceSummary(**summary_data)
        db.add(db_summary)
        db.commit()
    return db_ar

@app.get("/attendance_records/", response_model=List[AttendanceRecordOut])
def read_attendance_records(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(AttendanceRecord).offset(skip).limit(limit).all()

@app.get("/attendance_records/{ar_id}", response_model=AttendanceRecordOut)
def read_attendance_record(ar_id: int, db: Session = Depends(get_db)):
    ar = db.query(AttendanceRecord).filter(AttendanceRecord.id == ar_id).first()
    if not ar:
        raise HTTPException(status_code=404, detail="Attendance record not found")
    return ar


@app.put("/attendance_records/{ar_id}", response_model=AttendanceRecordOut)
def update_attendance_record(ar_id: int, ar: AttendanceRecordUpdate, db: Session = Depends(get_db)):
    db_ar = db.query(AttendanceRecord).filter(AttendanceRecord.id == ar_id).first()
    if not db_ar:
        raise HTTPException(status_code=404, detail="Attendance record not found")
    # Validation: in_time before out_time
    if ar.in_time and ar.out_time and ar.in_time >= ar.out_time:
        raise HTTPException(status_code=400, detail="in_time must be before out_time")
    for var, value in vars(ar).items():
        if value is not None:
            setattr(db_ar, var, value)
    db.commit()
    db.refresh(db_ar)
    # Recalculate summary
    db.query(AttendanceSummary).filter(AttendanceSummary.employee_id == db_ar.employee_id, AttendanceSummary.date == db_ar.date).delete()
    summary_data = calculate_attendance_summary(db, db_ar)
    if summary_data:
        db_summary = AttendanceSummary(**summary_data)
        db.add(db_summary)
        db.commit()
    return db_ar

@app.delete("/attendance_records/{ar_id}")
def delete_attendance_record(ar_id: int, db: Session = Depends(get_db)):
    db_ar = db.query(AttendanceRecord).filter(AttendanceRecord.id == ar_id).first()
    if not db_ar:
        raise HTTPException(status_code=404, detail="Attendance record not found")
    db.delete(db_ar)
    db.commit()
    return {"ok": True}

# AttendanceSummary CRUD endpoints
@app.post("/attendance_summaries/", response_model=AttendanceSummaryOut)
def create_attendance_summary(asum: AttendanceSummaryCreate, db: Session = Depends(get_db)):
    db_asum = AttendanceSummary(**asum.dict())
    db.add(db_asum)
    db.commit()
    db.refresh(db_asum)
    return db_asum

@app.get("/attendance_summaries/", response_model=List[AttendanceSummaryOut])
def read_attendance_summaries(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(AttendanceSummary).offset(skip).limit(limit).all()

@app.get("/attendance_summaries/{asum_id}", response_model=AttendanceSummaryOut)
def read_attendance_summary(asum_id: int, db: Session = Depends(get_db)):
    asum = db.query(AttendanceSummary).filter(AttendanceSummary.id == asum_id).first()
    if not asum:
        raise HTTPException(status_code=404, detail="Attendance summary not found")
    return asum

@app.put("/attendance_summaries/{asum_id}", response_model=AttendanceSummaryOut)
def update_attendance_summary(asum_id: int, asum: AttendanceSummaryUpdate, db: Session = Depends(get_db)):
    db_asum = db.query(AttendanceSummary).filter(AttendanceSummary.id == asum_id).first()
    if not db_asum:
        raise HTTPException(status_code=404, detail="Attendance summary not found")
    for var, value in vars(asum).items():
        if value is not None:
            setattr(db_asum, var, value)
    db.commit()
    db.refresh(db_asum)
    return db_asum

@app.delete("/attendance_summaries/{asum_id}")
def delete_attendance_summary(asum_id: int, db: Session = Depends(get_db)):
    db_asum = db.query(AttendanceSummary).filter(AttendanceSummary.id == asum_id).first()
    if not db_asum:
        raise HTTPException(status_code=404, detail="Attendance summary not found")
    db.delete(db_asum)
    db.commit()
    return {"ok": True}

# LeaveType CRUD endpoints
@app.post("/leave_types/", response_model=LeaveTypeOut)
def create_leave_type(lt: LeaveTypeCreate, db: Session = Depends(get_db)):
    db_lt = LeaveType(**lt.dict())
    db.add(db_lt)
    db.commit()
    db.refresh(db_lt)
    return db_lt

@app.get("/leave_types/", response_model=List[LeaveTypeOut])
def read_leave_types(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(LeaveType).offset(skip).limit(limit).all()

@app.get("/leave_types/{lt_id}", response_model=LeaveTypeOut)
def read_leave_type(lt_id: int, db: Session = Depends(get_db)):
    lt = db.query(LeaveType).filter(LeaveType.id == lt_id).first()
    if not lt:
        raise HTTPException(status_code=404, detail="Leave type not found")
    return lt

@app.put("/leave_types/{lt_id}", response_model=LeaveTypeOut)
def update_leave_type(lt_id: int, lt: LeaveTypeUpdate, db: Session = Depends(get_db)):
    db_lt = db.query(LeaveType).filter(LeaveType.id == lt_id).first()
    if not db_lt:
        raise HTTPException(status_code=404, detail="Leave type not found")
    for var, value in vars(lt).items():
        if value is not None:
            setattr(db_lt, var, value)
    db.commit()
    db.refresh(db_lt)
    return db_lt

@app.delete("/leave_types/{lt_id}")
def delete_leave_type(lt_id: int, db: Session = Depends(get_db)):
    db_lt = db.query(LeaveType).filter(LeaveType.id == lt_id).first()
    if not db_lt:
        raise HTTPException(status_code=404, detail="Leave type not found")
    db.delete(db_lt)
    db.commit()
    return {"ok": True}

# Leave CRUD endpoints
@app.post("/leaves/", response_model=LeaveOut)
def create_leave(leave: LeaveCreate, db: Session = Depends(get_db)):
    db_leave = Leave(**leave.dict())
    db.add(db_leave)
    db.commit()
    db.refresh(db_leave)
    return db_leave

@app.get("/leaves/", response_model=List[LeaveOut])
def read_leaves(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Leave).offset(skip).limit(limit).all()

@app.get("/leaves/{leave_id}", response_model=LeaveOut)
def read_leave(leave_id: int, db: Session = Depends(get_db)):
    leave = db.query(Leave).filter(Leave.id == leave_id).first()
    if not leave:
        raise HTTPException(status_code=404, detail="Leave not found")
    return leave

@app.put("/leaves/{leave_id}", response_model=LeaveOut)
def update_leave(leave_id: int, leave: LeaveUpdate, db: Session = Depends(get_db)):
    db_leave = db.query(Leave).filter(Leave.id == leave_id).first()
    if not db_leave:
        raise HTTPException(status_code=404, detail="Leave not found")
    for var, value in vars(leave).items():
        if value is not None:
            setattr(db_leave, var, value)
    db.commit()
    db.refresh(db_leave)
    return db_leave

@app.delete("/leaves/{leave_id}")
def delete_leave(leave_id: int, db: Session = Depends(get_db)):
    db_leave = db.query(Leave).filter(Leave.id == leave_id).first()
    if not db_leave:
        raise HTTPException(status_code=404, detail="Leave not found")
    db.delete(db_leave)
    db.commit()
    return {"ok": True}

# Holiday CRUD endpoints
@app.post("/holidays/", response_model=HolidayOut)
def create_holiday(holiday: HolidayCreate, db: Session = Depends(get_db)):
    db_holiday = Holiday(**holiday.dict())
    db.add(db_holiday)
    db.commit()
    db.refresh(db_holiday)
    return db_holiday

@app.get("/holidays/", response_model=List[HolidayOut])
def read_holidays(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Holiday).offset(skip).limit(limit).all()

@app.get("/holidays/{holiday_id}", response_model=HolidayOut)
def read_holiday(holiday_id: int, db: Session = Depends(get_db)):
    holiday = db.query(Holiday).filter(Holiday.id == holiday_id).first()
    if not holiday:
        raise HTTPException(status_code=404, detail="Holiday not found")
    return holiday

@app.put("/holidays/{holiday_id}", response_model=HolidayOut)
def update_holiday(holiday_id: int, holiday: HolidayUpdate, db: Session = Depends(get_db)):
    db_holiday = db.query(Holiday).filter(Holiday.id == holiday_id).first()
    if not db_holiday:
        raise HTTPException(status_code=404, detail="Holiday not found")
    for var, value in vars(holiday).items():
        if value is not None:
            setattr(db_holiday, var, value)
    db.commit()
    db.refresh(db_holiday)
    return db_holiday

@app.delete("/holidays/{holiday_id}")
def delete_holiday(holiday_id: int, db: Session = Depends(get_db)):
    db_holiday = db.query(Holiday).filter(Holiday.id == holiday_id).first()
    if not db_holiday:
        raise HTTPException(status_code=404, detail="Holiday not found")
    db.delete(db_holiday)
    db.commit()
    return {"ok": True}
