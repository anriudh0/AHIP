from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.infrastructure.database.session import get_db
from app.domain.entities.models import Provider
from app.domain.schemas.schemas import ProviderResponse

router = APIRouter()

@router.get("/", response_model=list[ProviderResponse])
def list_providers(db: Session = Depends(get_db)):
    return db.query(Provider).all()
