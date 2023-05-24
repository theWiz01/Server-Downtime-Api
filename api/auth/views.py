from fastapi import APIRouter, Depends
from api.auth.schemas import ChangePassword,Login, Signup
from api.auth.services import AuthService
from sqlmodel import Session
from database import get_session


router = APIRouter()


@router.post('/login')
def login(form : Login, session : Session = Depends(get_session)):
    service = AuthService(session=session)
    user = service.login(form)
    return user

@router.post('/signup')
def signup(form : Signup, session : Session = Depends(get_session)):
    service = AuthService(session=session)
    user = service.create_user(form)
    return user

@router.post('/change-password')
def change_password(
        form : ChangePassword, session : Session = Depends(get_session), 
        user_id = Depends(AuthService().auth_wrapper)):
    service = AuthService(session=session)
    password = service.change_password(form, user_id)
    return password