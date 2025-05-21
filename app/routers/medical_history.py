from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.database.config import get_connection
from typing import List, Optional
from datetime import date, datetime
import uuid

router = APIRouter()

@router.get("/patients/{patient_id}/medical-history")
def get_medical_history(patient_id: str):
    conn = get_connection()
    cursor = conn.cursor(dictionary = True)

    try:
        # Lay danh sách lượt khám của bệnh nhân
        cursor.execute("""
            SELECT * FROM emr_visits WHERE patient_id = %s
        """, (patient_id,))
        visits = cursor.fetchall()

        for visit in visits:
            # Lay danh sách thuốc theo visit_id
            cursor.execute("""
                SELECT * FROM emr_prescriptions WHERE visit_id = %s
            """, (visit['visit_id'],))
            visit['prescriptions'] = cursor.fetchall()

            return {
                "patient_id": patient_id,
                "visits": visits
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()