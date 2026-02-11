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
    link = Column(String,nullable=True)
    upload_id = Column(String,nullable=True)
    status = Column(Enum(Status),default=Status.not_started)
    duration_seconds = Column(Integer, nullable=True)
    start_time = Column(DateTime(timezone=True),nullable=True)
    created_at = Column(DateTime(timezone=True),server_default=func.now())

    user = relationship("User",back_populates="meetings")
    parts = relationship("Part",back_populates="meeting",cascade="all, delete-orphan",order_by="Part.part_id")

class Part(Base):
    __tablename__ = "parts"

    id= Column(UUID(as_uuid=True),nullable=False,primary_key=True,default=uuid4)
    meeting_id = Column(UUID(as_uuid=True),ForeignKey("meetings.id",ondelete="CASCADE"),nullable=False)
    part_id=Column(Integer,nullable=False)
    etag=Column(String,nullable=True)

    meeting = relationship("Meeting",back_populates="parts")

class TranscriptionJobStatus(enum.Enum):
    queued = "queued"
    processing = "processing"
    completed = "completed"
    failed = "failed"

class TranscriptionJob(Base):
    __tablename__ = "transcription_jobs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    meeting_id = Column(UUID(as_uuid=True), ForeignKey("meetings.id", ondelete="CASCADE"), nullable=False)

    status = Column(Enum(TranscriptionJobStatus), default=TranscriptionJobStatus.queued)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)

    meeting = relationship("Meeting")

class Dialogue(Base):
    __tablename__ = "dialogues"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    meeting_id = Column(UUID(as_uuid=True), ForeignKey("meetings.id", ondelete="CASCADE"), nullable=False)

    speaker = Column(String, nullable=True)  
    text = Column(String, nullable=False)

    start_time = Column(Integer, nullable=False) 
    end_time = Column(Integer, nullable=False)

    sequence = Column(Integer, nullable=False)

    meeting = relationship("Meeting")


class SummaryType(enum.Enum):
    brief = "brief"
    detailed = "detailed"
    action_items = "action_items"
    decisions = "decisions"
    custom = "custom"


class SummaryStatus(enum.Enum):
    queued = "queued"
    processing = "processing"
    completed = "completed"
    failed = "failed"


class Summary(Base):
    __tablename__ = "summaries"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    meeting_id = Column(UUID(as_uuid=True), ForeignKey("meetings.id", ondelete="CASCADE"), nullable=False)

    type = Column(Enum(SummaryType), nullable=False)

    content = Column(String, nullable=True)
    status = Column(Enum(SummaryStatus), default=SummaryStatus.queued)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    meeting = relationship("Meeting")


class CalendarWebhook(Base):
    __tablename__ = "calendar_webhooks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        unique=True 
    )

    calendar_id = Column(String, nullable=False, default="primary")

    channel_id = Column(String, nullable=False, unique=True)
    resource_id = Column(String, nullable=False)
    resource_uri = Column(String, nullable=True)

    expiration = Column(DateTime(timezone=True), nullable=True)

    sync_token = Column(String, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User")
