from pydantic import BaseModel, EmailStr

class EmailRequest(BaseModel):
    subject: str
    user_id: int
    user_name: str
    user_email: EmailStr
    message: str