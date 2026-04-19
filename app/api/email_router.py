from fastapi import APIRouter, HTTPException, status
from services.send_email import build_email_body, send_email
from schemas.email_schemas import EmailRequest

email_router = APIRouter(prefix="/email", tags=["email"])


@email_router.post("/send", status_code=status.HTTP_200_OK)
def send_email_endpoint(request: EmailRequest):
    body = build_email_body(request, "support")

    try:
        send_email(
            subject=request.subject,
            sender_email="inatelc317.mentistech.test@gmail.com",
            email_to="thomasvictor2909@gmail.com",
            body=body,
            reply_to=request.user_email,
        )
        return {"message": "Email enviado com sucesso!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao enviar email: {e}")
