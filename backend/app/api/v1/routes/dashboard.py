from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.infrastructure.database.session import get_db
from app.application.services.dashboard_service import DashboardService

router = APIRouter()

@router.get("/summary")
def dashboard_summary(db: Session = Depends(get_db)):
    return DashboardService().get_summary(db)
