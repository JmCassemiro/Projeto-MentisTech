from pydantic import BaseModel, field_validator

class EmailRequest(BaseModel):
    subject: str
    message: str

    @field_validator("subject", "message")
    @classmethod
    def strip_text_fields(cls, value: str) -> str:
        return value.strip()
