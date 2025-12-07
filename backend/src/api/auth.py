from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from backend.src.database.database import get_db
from backend.src.models import orm, student, token
from backend.src.services import auth_service
from backend.src.config import settings

router = APIRouter(prefix="/auth", tags=["authentication"])

@router.post("/signup", response_model=student.StudentInDB)
def signup(user: student.StudentCreate, db: Session = Depends(get_db)):
    db_user = db.query(orm.Student).filter(orm.Student.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = auth_service.get_password_hash(user.password)
    db_student = orm.Student(
        email=user.email, 
        name=user.name,
        hashed_password=hashed_password,
        software_background=user.software_background,
        hardware_background=user.hardware_background,
        language_preference=user.language_preference
    )
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

@router.post("/token", response_model=token.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(orm.Student).filter(orm.Student.email == form_data.username).first()
    if not user or not auth_service.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth_service.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
