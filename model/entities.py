from sqlalchemy import Column, String, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship
from database import connector
from sqlalchemy.dialects.postgresql import UUID
import uuid


class Institution(connector.Manager.Base):
    __tablename__ = "institution"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100))
    description = Column(String(200))
    address = Column(String(100))
    creation_date = Column(DateTime())
    projects = relationship("Project", cascade="all, delete")


class Project(connector.Manager.Base):
    __tablename__ = "project"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100))
    description = Column(String(200))
    creation_date = Column(DateTime())
    end_date = Column(DateTime())
    user_id = Column(UUID, ForeignKey("user.id"))
    institution_id = Column(UUID, ForeignKey("institution.id"))


class User(connector.Manager.Base):
    __tablename__ = "user"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100))
    last_name = Column(String(100))
    RUT = Column(String(30), unique=True)
    birthday = Column(DateTime())
    job_tittle = Column(String(100))
    age = Column(Integer())
    projects = relationship("Project")
