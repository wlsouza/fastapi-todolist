from uuid import uuid4

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from app.database.base_class import Base


class Task(Base):

    id = Column(Integer, primary_key=True, index=True)
    external_id = Column(UUID(as_uuid=True), index=True, unique=True, default=uuid4)
    title = Column(String, index=True)
    description = Column(String, index=True)
    is_done = Column(Boolean)
    owner_id = Column(Integer, ForeignKey("user.id"))

    owner = relationship("User", back_populates="tasks")