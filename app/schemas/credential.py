from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class CredentialBase(BaseModel):
    software: Optional[str] = None
    host: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    domain: Optional[str] = None
    local_part: Optional[str] = None
    email_domain: Optional[str] = None
    filepath: Optional[str] = None
    stealer_name: Optional[str] = None

class CredentialCreate(CredentialBase):
    pass

class CredentialResponse(CredentialBase):
    id: int
    created_at: Optional[datetime] = None  # Cho phép None
    updated_at: Optional[datetime] = None  # Cho phép None

    class Config:
        from_attributes = True