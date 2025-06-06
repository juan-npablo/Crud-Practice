from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from db.schemas.user import UserCreate
from db.models.user import User 
from db.session import get_db
from services.user_service import create_user, authenticate_user, get_user_by_email
from core.security import create_access_token

router = APIRouter()

@router.post("/register", response_model=UserCreate, status_code=status.HTTP_201_CREATED)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = get_user_by_email(db, user.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email ya existe en el sistema"
        )
    
    new_user = create_user(db, user)
    return new_user

@router.post("/login", response_model=dict)
def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
        )
    
    access_token = create_access_token({"sub": str(user.user_id)})
    return {"access_token": access_token, "token_type": "bearer"}