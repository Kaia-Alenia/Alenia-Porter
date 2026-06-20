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
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
@app.head("/")
def read_root():
    return {"status": "ok"}

class TelemetryPayload(BaseModel):
    uuid: str
    os_family: str
    interface_type: str
    file_type: str
    file_count: int

def get_db_connection():
    db_url = os.environ.get("DATABASE_URL")
    if not db_url:
        raise HTTPException(status_code=500, detail="Database URL environment variable missing.")
    return psycopg2.connect(db_url)

@app.post("/telemetry/event")
def record_event(payload: TelemetryPayload):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO telemetry_events (uuid, os_family, interface_type, file_type, file_count) VALUES (%s, %s, %s, %s, %s);",
            (payload.uuid, payload.os_family, payload.interface_type, payload.file_type, payload.file_count)
        )
        connection.commit()
        cursor.close()
        connection.close()
        return {"status": "ok", "message": "Event recorded successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/telemetry/stats")
def get_global_stats():
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        
        cursor.execute("SELECT file_type, SUM(file_count) FROM telemetry_events GROUP BY file_type;")
        rows = cursor.fetchall()
        stats = {row[0]: int(row[1]) for row in rows}
        
        cursor.execute("SELECT COUNT(DISTINCT uuid) FROM telemetry_events;")
        active_users = cursor.fetchone()[0]
        
        cursor.execute("SELECT os_family, COUNT(*) FROM (SELECT DISTINCT ON (uuid) uuid, os_family FROM telemetry_events ORDER BY uuid, timestamp DESC) AS unique_os GROUP BY os_family;")
        os_rows = cursor.fetchall()
        os_distribution = {row[0]: int(row[1]) for row in os_rows}
        
        cursor.close()
        connection.close()
        
        return {
            "status": "ok",
            "stats": {
                "audio": stats.get("audio", 0),
                "video": stats.get("video", 0),
                "image": stats.get("image", 0)
            },
            "active_users": int(active_users),
            "os_distribution": os_distribution
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
