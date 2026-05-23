from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.db.models.checkin import CheckIn
from app.db.models.user import User

analytics_router = APIRouter(prefix="/analytics", tags=["analytics"])


@analytics_router.get("/stress-level-by-user-monthly/{user_id}")
def stress_level_by_user_monthly(user_id: int, db: Session = Depends(get_db)):

    result = (
        db.query(
            func.strftime("%Y-%m", CheckIn.created_at).label("month"),
            func.avg(CheckIn.stress_level).label("average_stress"),
        )
        .filter(CheckIn.user_id == user_id)
        .group_by("month")
        .all()
    )

    return [
        {"month": checkin.month, "average_stress": checkin.average_stress}
        for checkin in result
    ]


@analytics_router.get("/stress-level/user/{user_id}")
def stress_level_by_user(user_id: int, db: Session = Depends(get_db)):

    result = db.query(CheckIn).filter(CheckIn.user_id == user_id).all()

    return [checkin.stress_level for checkin in result]


@analytics_router.get("/stress-level/role/{role}")
def stress_level_by_role(role: str, db: Session = Depends(get_db)):
    result = (
        db.query(func.avg(CheckIn.stress_level))
        .join(User, CheckIn.user_id == User.id)
        .filter(User.role == role)
        .scalar()
    )

    return {"role": role, "average_stress": result}


@analytics_router.get("/stress-level/team/{team}")
def stress_level_by_team(team: str, db: Session = Depends(get_db)):
    result = (
        db.query(func.avg(CheckIn.stress_level))
        .join(User)
        .filter(User.team == team)
        .scalar()
    )

    return {"team": team, "average_stress": result}


@analytics_router.get("/mood-by-team/{team}")
def mood_by_team(team: str, db: Session = Depends(get_db)):

    result = (
        db.query(CheckIn.overall_mood, func.count(CheckIn.id).label("count"))
        .join(User, CheckIn.user_id == User.id)
        .filter(User.team == team)
        .group_by(CheckIn.overall_mood)
        .all()
    )

    return [{"mood": row.overall_mood, "count": row.count} for row in result]


@analytics_router.get("/mood-by-role/{role}")
def mood_by_role(role: str, db: Session = Depends(get_db)):

    result = (
        db.query(CheckIn.overall_mood, func.count(CheckIn.id).label("count"))
        .join(User, CheckIn.user_id == User.id)
        .filter(User.role == role)
        .group_by(CheckIn.overall_mood)
        .all()
    )

    return [{"mood": row.overall_mood, "count": row.count} for row in result]


import json
from collections import defaultdict

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.db.models.checkin import CheckIn

analytics_router = APIRouter(prefix="/analytics", tags=["analytics"])


@analytics_router.get("/questions-average")
def questions_average(db: Session = Depends(get_db)):

    with open("app/db/questions.json", "r", encoding="utf-8") as file:
        questions_data = json.load(file)

    questions_map = {
        question["id"]: question["question"] for question in questions_data
    }

    checkins = db.query(CheckIn.answers_json).all()

    questions = defaultdict(list)

    for checkin in checkins:

        for answer in checkin.answers_json:

            questions[answer["question_id"]].append(answer["value"])

    return [
        {
            "question_id": question_id,
            "question": questions_map.get(question_id),
            "average": round(sum(values) / len(values), 2),
        }
        for question_id, values in questions.items()
    ]
