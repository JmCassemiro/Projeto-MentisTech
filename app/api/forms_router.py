import json

from fastapi import APIRouter, status

from schemas.forms_schemas import AnswerRequest


forms_router = APIRouter(prefix="/forms", tags=["forms"])


@forms_router.get("/questions")
def get_questions():
    with open("app/db/questions.json", "r") as file:
        return json.load(file)


@forms_router.post("/submit", status_code=status.HTTP_201_CREATED)
def submit_form(form_data: AnswerRequest):
    return {
        "message": "Formulário enviado com sucesso!",
        "data": form_data,
    }
