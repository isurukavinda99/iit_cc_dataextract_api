from starlette import status

from app.dto.dataextract_schema import UserEventCreate
from app.config.config import get_db
from app.exceptions.exceptions import AppExceptionCase
from fastapi import Depends
from sqlalchemy.orm import Session
from app.repositories.dataextract_repository import DataextractRepository

class DataextractService:

    @staticmethod
    def create_dataextract(data: UserEventCreate, db: Session = Depends(get_db)):
        try:
            return DataextractRepository.create_dataextract(db, data)
        except Exception as e:
            raise AppExceptionCase(
                "data extract failed due to DB error : " + str(e),
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                code="DB_ERROR"
            ) from e