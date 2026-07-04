from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.infrastructure.database.session import get_db
from app.domain.entities.models import Patient
from app.domain.schemas.schemas import PatientResponse

router = APIRouter()

@router.get("/", response_model=list[PatientResponse])
def list_patients(db: Session = Depends(get_db)):
    return db.query(Patient).all()
