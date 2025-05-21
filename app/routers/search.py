# app/routers/search.py
from fastapi import APIRouter, Query, HTTPException
from typing import Optional, List
from app.database.config import get_connection

router = APIRouter()

@router.get("/patients/search")
def search_patients(
    first_name: Optional[str] = Query(None),
    last_name: Optional[str] = Query(None),
    medical_id: Optional[str] = Query(None),
    gender: Optional[str] = Query(None),
    year_of_birth: Optional[int] = Query(None),
    address: Optional[str] = Query(None)
):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        sql = "SELECT * FROM emr_patients WHERE 1=1"
        params = []

        if first_name:
            sql += " AND first_name LIKE %s"
            params.append(f"%{first_name}%")
        if last_name:
            sql += " AND last_name LIKE %s"
            params.append(f"%{last_name}%")
        if medical_id:
            sql += " AND medical_id = %s"
            params.append(medical_id)
        if gender:
            sql += " AND gender = %s"
            params.append(gender)
        if year_of_birth:
            sql += " AND YEAR(date_of_birth) = %s"
            params.append(year_of_birth)
        if address:
            sql += " AND address LIKE %s"
            params.append(f"%{address}%")

        cursor.execute(sql, tuple(params))
        return cursor.fetchall()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()
