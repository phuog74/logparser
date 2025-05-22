from sqlalchemy import Column, Integer, String, DateTime
from ..core.database import Base
import datetime

class Credential(Base):
    __tablename__ = "credentials"

    id = Column(Integer, primary_key=True, index=True)
    software = Column(String, nullable=True)
    host = Column(String, nullable=True)
    username = Column(String, nullable=True)
    password = Column(String, nullable=True)
    domain = Column(String, nullable=True)
    local_part = Column(String, nullable=True)
    email_domain = Column(String, nullable=True)
    filepath = Column(String, nullable=True)
    stealer_name = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)