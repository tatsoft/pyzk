from sqlalchemy import create_engine, text
engine = create_engine("sqlite:///./attendance.db", connect_args={"check_same_thread": False})
try:
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
        print("Direct DB connection OK")
except Exception as e:
    print("Direct DB connection failed:", e)
