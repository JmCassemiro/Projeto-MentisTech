from fastapi import APIRouter, Depends, HTTPException, status

from app.core.config import SUPPORT_EMAIL
from app.core.dependencies import get_current_user
from app.db.models.user import User
from app.services.send_email import build_email_body, send_email, EmailNotConfiguredError
from app.schemas.email_schemas import EmailRequest

email_router = APIRouter(prefix="/email", tags=["email"])


@email_router.post("/send", status_code=status.HTTP_200_OK)
def send_email_endpoint(
    request: EmailRequest,
    current_user: User = Depends(get_current_user),
):
    body = build_email_body(
        {
            "user_name": current_user.full_name,
            "user_email": current_user.corporate_email,
            "user_id": current_user.id,
            "message": request.message,
        },
        "support",
    )

    try:
        send_email(
            subject=request.subject,
            email_to=SUPPORT_EMAIL,
            reply_to=current_user.corporate_email,
            body=body,
        )
        return {"message": "Email enviado com sucesso!"}
    except EmailNotConfiguredError as e:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao enviar email: {e}")
