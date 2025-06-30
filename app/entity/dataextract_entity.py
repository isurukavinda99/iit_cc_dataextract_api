from clickhouse_sqlalchemy import get_declarative_base, types, engines
from sqlalchemy import Column, String, UUID
from sqlalchemy import Enum as SQLAlchemyEnum
import uuid

Base = get_declarative_base()

class UserEvent(Base):
    __tablename__ = 'user_events'
    __table_args__ = (
        engines.MergeTree(
            order_by=('user_id', 'event_time')
        ),
    )

    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    event_date = Column(types.Date, nullable=False)
    event_time = Column(types.DateTime, nullable=False)
    session_id = Column(String, nullable=False)
    user_id = Column(String, nullable=False)

    event_type = Column(SQLAlchemyEnum('click', 'scroll', 'pageview', 'navigate', name='event_type_enum'))

    element_id = Column(String, nullable=True)
    page_url = Column(String, nullable=False)
    scroll_depth = Column(types.Float32, nullable=True)
    target_url = Column(String, nullable=True)
    x_position = Column(types.Int32, nullable=True)
    y_position = Column(types.Int32, nullable=True)
    viewport_width = Column(types.Int32, nullable=False)
    viewport_height = Column(types.Int32, nullable=False)
