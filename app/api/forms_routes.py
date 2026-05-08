import json

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.schemas.forms_schemas import AnswerRequest

from app.db.models.checkin import CheckIn

forms_router = APIRouter(prefix="/forms", tags=["forms"])


@forms_router.get("/questions")
def get_questions():
    with open("app/db/questions.json", "r", encoding="utf-8") as file:
        return json.load(file)


@forms_router.post("/submit", status_code=status.HTTP_201_CREATED)
def submit_form(data: AnswerRequest, db: Session = Depends(get_db)):
    try:
        answer_quantity = len(data.answers)
        total_value_answers = sum(answer.value for answer in data.answers)
        overall_mood = total_value_answers / answer_quantity
        
        checkin = CheckIn(
            user_id=data.user_id,
            overall_mood=str(overall_mood),
            answers_json=[answer.model_dump() for answer in data.answers],
            stress_level=int(overall_mood * 10),
            ai_insights="Temporary AI insight",
            submitted_at=data.created_at,
        )

        db.add(checkin)
        db.commit()
        db.refresh(checkin)

        return {"message": "Formulário enviado com sucesso", "data": checkin}

    except SQLAlchemyError as e:
        db.rollback()

        raise HTTPException(
            status_code=500,
            detail=f"Database error: {str(e)}",
        )

    except Exception as e:
        db.rollback()

        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error: {str(e)}",
        )
