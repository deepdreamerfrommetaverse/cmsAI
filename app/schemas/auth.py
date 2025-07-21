from pydantic import BaseModel, EmailStr

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    sub: EmailStr | None = None

class LoginPayload(BaseModel):
    email: EmailStr
    password: str
