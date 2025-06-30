from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dto.dataextract_schema import UserEventCreate
from app.config.config import get_db
import logging

from app.services.dataextract_service import DataextractService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/dataextract", tags=["dataextract"])

@router.post("")
async def create_item(data: UserEventCreate, db: Session = Depends(get_db)):
    dataextract = DataextractService.create_dataextract(data=data, db=db)
    return dataextract