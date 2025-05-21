from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from app.database.config import get_connection
from typing import List, Optional
from datetime import date, datetime
from uuid import uuid4
import logging

logging.basicConfig(level=logging.DEBUG)

router = APIRouter()


# Schema tạo mới lượt khám
class VisitCreate(BaseModel):
    patient_id: str
    doctor_id: str
    department_id: str
    facility_id: str
    visit_date: datetime
    symptoms: Optional[str]
    diagnosis: Optional[str]
    notes: Optional[str]
    status: str # 'in_progress', 'completed', 'cancelled'

# Schema lượt khám
class Visit(BaseModel):
    visit_id: str
    patient_id: str
    doctor_id: str
    department_id: str
    facility_id: str
    visit_date: datetime
    symptoms: Optional[str]
    diagnosis: Optional[str]
    notes: Optional[str]
    status: str # 'in_progress', 'completed', 'cancelled'
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

# API thêm mới lượt khám
@router.post("/visits")
def create_visit(visit: VisitCreate):
    connection = get_connection()
    cursor = connection.cursor()
    
    try:
        visit_id = str(uuid4())
        cursor.execute("""
            INSERT INTO emr_visits (visit_id, patient_id, doctor_id, department_id, facility_id, visit_date, symptoms, diagnosis, notes, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (visit_id, visit.patient_id, visit.doctor_id, visit.department_id,
              visit.facility_id, visit.visit_date, visit.symptoms,
              visit.diagnosis, visit.notes, visit.status))
        connection.commit()
        return {"message": "Visit created successfully", "visit_id": visit_id}
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        connection.close()

# API lấy danh sách lượt khám theo ID bệnh nhân
@router.get("/visits/{patient_id}", response_model=List[Visit])
def get_visits_by_patient_id(patient_id: str):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM emr_visits WHERE patient_id = %s", (patient_id,))
        return cursor.fetchall()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        connection.close()

# API lấy danh sách lượt khám theo ngày hoặc theo id bác sĩ
from datetime import timedelta

@router.get("/visits/filter", response_model=List[Visit])
def filter_visits(
    visit_date: Optional[date] = Query(None),
    doctor_id: Optional[str] = Query(None)
):
    print("===> ĐÃ CHẠY VÀO HÀM filter_visits")

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        sql = "SELECT * FROM emr_visits WHERE 1=1"
        params = []

        if visit_date:
            start = datetime.combine(visit_date, datetime.min.time())
            end = start + timedelta(days=1)
            sql += " AND visit_date >= %s AND visit_date < %s"
            params.extend([start, end])

        if doctor_id:
            sql += " AND doctor_id = %s"
            params.append(doctor_id)

        print("DEBUG SQL:", sql)
        print("DEBUG PARAMS:", params)

        cursor.execute(sql, tuple(params))
        return cursor.fetchall()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()
