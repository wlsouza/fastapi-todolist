from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database.base import Base


class Task(Base):

    __tablename__ = "task"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    is_done = Column(Boolean)
    owner_id = Column(Integer, ForeignKey("user.id"))

    owner = relationship("User", back_populates="tasks")
