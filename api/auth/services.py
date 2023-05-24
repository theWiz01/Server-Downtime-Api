from fastapi import Depends, Security
from api.auth.schemas import ChangePassword, Login, Signup
from sqlmodel import select, Session
from models.user import User
from database import get_session
from passlib.context import CryptContext
from utils.funcs import exception_message
from datetime import  datetime, timedelta
from jose import JWTError, jwt
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer



security = HTTPBearer()

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    def __init__(self, session : Session = Depends(get_session)):
        self.session = session
    
    def get_password_hash(self, password):
        return pwd_context.hash(password)
    
    def verify_password(self, plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)
    
    def authenticate_user(self, email: str, password: str):
        statement = select(User).where(User.email == email)
        user = self.session.execute(statement).scalars().first()
        if user:
            if self.verify_password(password, user.password):
                return user
        raise exception_message(status_code=401, message="Invalid Email or Password")
    
    def create_access_token(self, data: dict, expires_delta: timedelta = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    
    def decode_token(self, token):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            user_id: str = payload.get("sub")
            return user_id
        except JWTError:
            raise exception_message(401, 'Invalid Token')
    
    def login(self, form : Login):
        user = self.authenticate_user(email=form.email, password=form.password)
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = self.create_access_token(
            data={"sub": f'{user.id}'}, expires_delta=access_token_expires
        )
        return {
            "user" : user,
            "access_token": access_token, 
            "token_type": "Bearer"}

    
    def create_user(self, user : Signup):
        statement = select(User).where(User.email == user.email)
        details = self.session.execute(statement).scalars().first()
        if not details:
            user.password = self.get_password_hash(user.password)
            new_user = User(**user.dict())
            self.session.add(new_user)
            self.session.commit()
            self.session.refresh(new_user)
            return new_user
        raise exception_message(status_code=409, message="Email Already Exists")
    
    def auth_wrapper(self, token: HTTPAuthorizationCredentials = Security(security)):
        return self.decode_token(token.credentials)
    
    def user_passes_test(self, user_id, obj_id):
        pass
    
    def change_password(self, passwords : ChangePassword , user_id : str ):
        statement = select(User).where(User.id == user_id)
        user = self.session.execute(statement).scalars().first()
        if user:
            if self.verify_password(passwords.current_password, user.password):
                user.password = self.get_password_hash(passwords.new_password)
                self.session.add(user)
                self.session.commit()
                self.session.refresh(user)
                return {
                    "user" : user,
                    "message" : "Password Changed"
                    }
        return exception_message(status_code=404, message="User Not Found")