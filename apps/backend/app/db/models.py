import enum
from sqlalchemy import Column, Enum, ForeignKey, Integer,String,DateTime
from sqlalchemy.orm import declarative_base, relationship
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func


Base = declarative_base()

class User(Base):
    __tablename__="users"

    id = Column(UUID(as_uuid=True),primary_key=True,default=uuid4)
    external_auth_id = Column(String,unique=True,nullable=False)
    email=Column(String,unique=True,nullable=True)
    created_at = Column(DateTime(timezone=True),server_default=func.now())

    meetings = relationship("Meeting",back_populates="user",cascade="all, delete-orphan")

class Status(enum.Enum):
    not_started = "not_started"
    uploading = "uploading"
    finished = "finished"

class Meeting(Base):
    __tablename__="meetings"

    id= Column(UUID(as_uuid=True),nullable=False,primary_key=True,default=uuid4)
    user_id = Column(UUID(as_uuid=True),ForeignKey("users.id",ondelete="CASCADE"),nullable=False)
    bucket = Column(String,nullable=True)
    key = Column(String,nullable=True)
    upload_id = Column(String,nullable=True)
    status = Column(Enum(Status),default=Status.not_started)

    user = relationship("User",back_populates="meetings")
    parts = relationship("Part",back_populates="meeting",cascade="all, delete-orphan",order_by="Part.part_number")

class Part(Base):
    __tablename__ = "parts"

    id= Column(UUID(as_uuid=True),nullable=False,primary_key=True,default=uuid4)
    meeting_id = Column(UUID(as_uuid=True),ForeignKey("meetings.id",ondelete="CASCADE"),nullable=False)
    part_id=Column(Integer,nullable=False)
    etag=Column(String,nullable=True)

    meeting = relationship("Meeting",back_populates="parts")
