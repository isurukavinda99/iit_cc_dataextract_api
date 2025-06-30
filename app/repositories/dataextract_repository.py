from sqlalchemy.orm import Session, joinedload
from app.entity.dataextract_entity import UserEvent as UserEventModal
from uuid import uuid4


class DataextractRepository:
    @staticmethod
    def create_dataextract(db: Session, dataextract_data: UserEventModal):
        try:
            db_item = UserEventModal(
                id=uuid4(),
                event_date=dataextract_data.event_date,
                event_time=dataextract_data.event_time,
                session_id=dataextract_data.session_id,
                user_id=dataextract_data.user_id,
                event_type=dataextract_data.event_type.value,
                element_id=dataextract_data.element_id,
                page_url=dataextract_data.page_url,
                scroll_depth=dataextract_data.scroll_depth,
                target_url=dataextract_data.target_url,
                x_position=dataextract_data.x_position,
                y_position=dataextract_data.y_position,
                viewport_width=dataextract_data.viewport_width,
                viewport_height=dataextract_data.viewport_height
            )
            db.add(db_item)
            db.commit()
            db.refresh(db_item)
            return db_item
        except Exception as e:
            db.rollback()
            raise e