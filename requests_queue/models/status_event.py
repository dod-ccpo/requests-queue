from sqlalchemy import Column, func, ForeignKey
from sqlalchemy.types import DateTime, String
from sqlalchemy.dialects.postgresql import UUID

from requests_queue.models import Base
from requests_queue.models.types import Id


class StatusEvent(Base):
    __tablename__ = 'status_events'

    id = Id()
    new_status = Column(String())
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    request_id = Column(UUID(as_uuid=True), ForeignKey('requests.id'))
