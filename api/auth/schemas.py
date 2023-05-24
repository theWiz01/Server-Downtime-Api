from pydantic import BaseModel, EmailStr, ValidationError, validator

class Login(BaseModel):
    email : EmailStr
    password : str


class Signup(BaseModel):
    first_name : str
    last_name : str
    email : EmailStr
    password : str


class ChangePassword(BaseModel):
    current_password : str
    new_password : str
    confirm_password : str

    @validator('confirm_password')
    def password_match(cls, v, values, **kwargs):
        if 'new_password' in values and v != values['new_password']:
            raise ValueError("Password Must Match")
        return v