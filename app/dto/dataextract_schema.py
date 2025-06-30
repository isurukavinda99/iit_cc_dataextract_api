from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime
from enum import Enum

# Enum for event_type
class EventType(str, Enum):
    click = 'click'
    scroll = 'scroll'
    pageview = 'pageview'
    navigate = 'navigate'

# Base model with all fields
class UserEventCreate(BaseModel):
    event_date: date
    event_time: datetime
    session_id: str
    user_id: str
    event_type: EventType
    element_id: Optional[str] = None
    page_url: str
    scroll_depth: Optional[float] = None
    target_url: Optional[str] = None
    x_position: Optional[int] = None
    y_position: Optional[int] = None
    viewport_width: int
    viewport_height: int
