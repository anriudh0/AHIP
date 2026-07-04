from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.infrastructure.database.session import get_db
from app.domain.entities.models import Claim
from app.domain.schemas.schemas import ClaimResponse

router = APIRouter()

@router.get("/", response_model=list[ClaimResponse])
def list_claims(db: Session = Depends(get_db)):
    return db.query(Claim).all()
