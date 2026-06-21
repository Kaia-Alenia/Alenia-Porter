from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import os
import psycopg2
import platform

app = FastAPI(title="Alenia Porter Telemetry API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_db_migration():
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS telemetry_events (id SERIAL PRIMARY KEY, uuid VARCHAR, nickname VARCHAR, os_family VARCHAR, interface_type VARCHAR, file_type VARCHAR, file_count INTEGER, duration_seconds FLOAT, timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP);")
        cursor.execute("ALTER TABLE telemetry_events ADD COLUMN IF NOT EXISTS duration_seconds FLOAT;")
        cursor.execute("ALTER TABLE telemetry_events ADD COLUMN IF NOT EXISTS nickname VARCHAR;")
        cursor.execute("CREATE TABLE IF NOT EXISTS telemetry_feedback (uuid VARCHAR, nickname VARCHAR, rating INTEGER, uses_godot BOOLEAN, comments TEXT, timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP);")
        cursor.execute("CREATE TABLE IF NOT EXISTS telemetry_crashes (id SERIAL PRIMARY KEY, app_version VARCHAR, error_code VARCHAR, message TEXT, stack_trace TEXT, os_family VARCHAR, cpu_cores INTEGER, ram_gb INTEGER, timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP);")
        cursor.execute("ALTER TABLE telemetry_crashes ADD COLUMN IF NOT EXISTS uuid VARCHAR;")
        cursor.execute("ALTER TABLE telemetry_crashes ADD COLUMN IF NOT EXISTS nickname VARCHAR;")
        connection.commit()
        cursor.close()
        connection.close()
    except Exception as e:
        pass

@app.get("/")
@app.head("/")
def read_root():
    return {"status": "ok"}

class TelemetryPayload(BaseModel):
    uuid: str
    nickname: Optional[str] = None
    os_family: str
    interface_type: str
    file_type: str
    file_count: int
    duration_seconds: float

class FeedbackPayload(BaseModel):
    uuid: str
    nickname: Optional[str] = None
    rating: int
    uses_godot: bool
    comments: str

class SystemMetadata(BaseModel):
    os_family: str
    cpu_cores: int
    ram_gb: int

class CrashPayload(BaseModel):
    uuid: str
    nickname: Optional[str] = None
    app_version: str
    error_code: str
    message: str
    stack_trace: str
    system_metadata: SystemMetadata

@app.post("/telemetry/feedback")
def record_feedback(payload: FeedbackPayload):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO telemetry_feedback (uuid, nickname, rating, uses_godot, comments) VALUES (%s, %s, %s, %s, %s);",
            (payload.uuid, payload.nickname, payload.rating, payload.uses_godot, payload.comments)
        )
        connection.commit()
        cursor.close()
        connection.close()
        return {"status": "ok", "message": "Feedback recorded successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/telemetry/crash")
def record_crash(payload: CrashPayload):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO telemetry_crashes (app_version, error_code, message, stack_trace, os_family, cpu_cores, ram_gb, uuid, nickname) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);",
            (payload.app_version, payload.error_code, payload.message, payload.stack_trace, payload.system_metadata.os_family, payload.system_metadata.cpu_cores, payload.system_metadata.ram_gb, payload.uuid, payload.nickname)
        )
        connection.commit()
        cursor.close()
        connection.close()
        return {"status": "ok", "message": "Crash report recorded successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

def get_db_connection():
    db_url = os.environ.get("DATABASE_URL")
    if not db_url:
        raise HTTPException(status_code=500, detail="Internal server error")
    return psycopg2.connect(db_url)

@app.post("/telemetry/event")
def record_event(payload: TelemetryPayload):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO telemetry_events (uuid, nickname, os_family, interface_type, file_type, file_count, duration_seconds) VALUES (%s, %s, %s, %s, %s, %s, %s);",
            (payload.uuid, payload.nickname, payload.os_family, payload.interface_type, payload.file_type, payload.file_count, payload.duration_seconds)
        )
        connection.commit()
        cursor.close()
        connection.close()
        return {"status": "ok", "message": "Event recorded successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/telemetry/stats")
def get_global_stats():
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        
        cursor.execute("SELECT file_type, SUM(file_count) FROM telemetry_events GROUP BY file_type;")
        rows = cursor.fetchall()
        stats = {row[0]: int(row[1]) if row[1] is not None else 0 for row in rows}
        
        cursor.execute("SELECT COUNT(DISTINCT uuid) FROM telemetry_events;")
        active_users = cursor.fetchone()[0]
        
        cursor.execute("SELECT os_family, COUNT(*) FROM (SELECT DISTINCT ON (uuid) uuid, os_family FROM telemetry_events ORDER BY uuid, timestamp DESC) AS unique_os GROUP BY os_family;")
        os_rows = cursor.fetchall()
        os_distribution = {row[0]: int(row[1]) if row[1] is not None else 0 for row in os_rows}
        
        cursor.execute("SELECT file_type, SUM(duration_seconds), SUM(file_count) FROM telemetry_events GROUP BY file_type;")
        avg_rows = cursor.fetchall()
        avg_time_by_type = {}
        for row in avg_rows:
            f_type, total_time, total_count = row
            if total_count and total_count > 0 and total_time is not None:
                avg_time_by_type[f_type] = round(float(total_time) / float(total_count), 3)
            else:
                avg_time_by_type[f_type] = 0.0
                
        cursor.execute("SELECT SUM(duration_seconds), SUM(file_count) FROM telemetry_events;")
        total_time_sum, total_count_sum = cursor.fetchone()
        avg_time_per_file = round(float(total_time_sum) / float(total_count_sum), 3) if total_count_sum and total_time_sum is not None else 0.0
        
        cursor.execute("SELECT nickname, SUM(file_count) as total FROM telemetry_events WHERE nickname IS NOT NULL GROUP BY nickname ORDER BY total DESC LIMIT 10;")
        top_rows = cursor.fetchall()
        top_users = [{"nickname": row[0], "total": int(row[1])} for row in top_rows]
        
        cursor.close()
        connection.close()
        
        return {
            "status": "ok",
            "stats": {
                "audio": stats.get("audio", 0),
                "video": stats.get("video", 0),
                "image": stats.get("image", 0)
            },
            "active_users": int(active_users) if active_users is not None else 0,
            "os_distribution": os_distribution,
            "avg_time_per_file": avg_time_per_file,
            "avg_time_by_type": avg_time_by_type,
            "top_users": top_users
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")
