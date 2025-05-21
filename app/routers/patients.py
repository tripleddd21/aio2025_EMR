from fastapi import APIRouter, HTTPException, Path, Query
from pydantic import BaseModel
from app.database.config import get_connection
import uuid
from typing import List, Optional
from datetime import date, datetime


router = APIRouter()

# Model tạo mới bệnh nhân (không có patient_id)
class PatientCreate(BaseModel):
    medical_id: str
    first_name: str
    last_name: str
    date_of_birth: str  # YYYY-MM-DD
    gender: str
    address: str = None
    phone_number: str = None
    email: str = None

# Model bệnh nhân (có patient_id)
class Patient(BaseModel):
    patient_id: str
    medical_id: str
    first_name: str
    last_name: str
    date_of_birth: date  # YYYY-MM-DD
    gender: str
    address: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[str] = None
    created_at: Optional[datetime] = None

# Model cập nhật thông tin bệnh nhân
class PatientUpdate(BaseModel):
    medical_id: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    date_of_birth: Optional[date] = None
    gender: Optional[str] = None
    address: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[str] = None

# Model xóa bệnh nhân



@router.post("/patients")

# Thêm mới
def create_patient(patient: PatientCreate):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        patient_id = str(uuid.uuid4()) # Tạo ID ngẫu nhiên cho bệnh nhân
        # Chuẩn bị lệnh SQL
        sql = """
            INSERT INTO emr_patients (
                patient_id, medical_id, first_name, last_name,
                date_of_birth, gender, address, phone_number, email
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        # Thực thi
        cursor.execute(sql, (
            patient_id,
            patient.medical_id,
            patient.first_name,
            patient.last_name,
            patient.date_of_birth,
            patient.gender,
            patient.address,
            patient.phone_number,
            patient.email
        ))

        conn.commit()
        return {"message": "Patient created successfully", "patient_id": patient_id}

    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        cursor.close()
        conn.close()


# Truy vấn toàn bộ bệnh nhân
@router.get("/patients", response_model=List[Patient])
def get_patients():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM emr_patients")
        rows = cursor.fetchall()
        return rows
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

# Truy vấn bệnh nhân theo ID
@router.get("/patients/{patient_id}", response_model=Patient)
def get_patient_by_id(patient_id: str = Path(..., title="Patient ID", description="ID of the patient to retrieve")):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM emr_patients WHERE patient_id = %s", (patient_id,))
        row = cursor.fetchone()
        if row is None:
            raise HTTPException(status_code=404, detail="Patient not found")
        return row
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

# Cập nhật thông tin bệnh nhân
@router.put("/patients/{patient_id}", response_model=PatientUpdate)
def update_patient(patient_id: str, patient: PatientUpdate):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        # Kieem tra xem bệnh nhân có tồn tại không
        cursor.execute("SELECT * FROM emr_patients WHERE patient_id = %s", (patient_id,))
        row = cursor.fetchone()
        if row is None:
            raise HTTPException(status_code=404, detail="Patient not found")
        # Tao danh sach cac truong can cap nhat
        update_fields = []
        update_values = []
        for field, value in patient.dict(exclude_unset=True).items():
            update_fields.append(f"{field} = %s")
            update_values.append(value)
        if not update_fields:
            raise HTTPException(status_code=400, detail="No fields to update")
        update_values.append(patient_id)
        # Thuc thi lenh cap nhat
        sql = f"UPDATE emr_patients SET {', '.join(update_fields)} WHERE patient_id = %s"
        cursor.execute(sql, update_values)
        conn.commit()
        return {"message": "Patient updated successfully"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()
# Xóa bệnh nhân
@router.delete("/patients/{patient_id}")
def delete_patient(patient_id: str):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        #Check
        cursor.execute("SELECT * FROM emr_patients WHERE patient_id = %s", (patient_id,))
        row = cursor.fetchone()
        if row is None:
            raise HTTPException(status_code=404, detail="Patient not found")
        # Thuc thi lenh xoa
        cursor.execute("DELETE FROM emr_patients WHERE patient_id = %s", (patient_id,))
        conn.commit()
        return {"message": "Patient deleted successfully"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()


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
    