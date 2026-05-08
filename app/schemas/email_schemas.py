from pydantic import BaseModel, EmailStr

class EmailRequest(BaseModel):
    subject: str
    user_id: int
    user_name: str
    user_email: EmailStr
    email_to: EmailStr
    message: str
