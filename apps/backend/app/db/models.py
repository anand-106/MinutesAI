from sqlalchemy import Column,String,DateTime
from sqlalchemy.orm import declarative_base
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
