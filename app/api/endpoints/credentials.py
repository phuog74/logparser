from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ...core.database import get_db
from ...models.credential import Credential
from ...schemas.credential import CredentialCreate, CredentialResponse

router = APIRouter()

@router.post("/", response_model=CredentialResponse)
def create_credential(credential: CredentialCreate, db: Session = Depends(get_db)):
    db_credential = Credential(**credential.dict())
    db.add(db_credential)
    db.commit()
    db.refresh(db_credential)
    return db_credential

@router.get("/", response_model=List[CredentialResponse])
def get_credentials(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    try:
        credentials = db.query(Credential).offset(skip).limit(limit).all()
        print(f"Debug: Found {len(credentials)} credentials")
        return credentials
    except Exception as e:
        print(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.get("/{credential_id}", response_model=CredentialResponse)
def get_credential(credential_id: int, db: Session = Depends(get_db)):
    try:
        credential = db.query(Credential).filter(Credential.id == credential_id).first()
        print(f"Debug: Searching for credential_id={credential_id}, Result={credential}")
        if credential is None:
            raise HTTPException(status_code=404, detail="Credential not found")
        return credential
    except Exception as e:
        print(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")