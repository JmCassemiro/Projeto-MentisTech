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


@analytics_router.get("/mood-by-team")
def mood_by_team(db: Session = Depends(get_db)):

    result = (
        db.query(User.team, func.avg(CheckIn.overall_mood).label("average_mood"))
        .join(User)
        .group_by(User.team)
        .all()
    )

    return result


@analytics_router.get("/mood-by-role")
def mood_by_role(db: Session = Depends(get_db)):

    result = (
        db.query(User.role, func.avg(CheckIn.overall_mood).label("average_mood"))
        .join(User)
        .group_by(User.role)
        .all()
    )

    return result


@analytics_router.get("/questions-average")
def questions_average(db: Session = Depends(get_db)):

    checkins = db.query(CheckIn).all()

    questions = {}

    for checkin in checkins:

        for answer in checkin.answers_json:

            question_id = answer["question_id"]
            value = answer["value"]

            if question_id not in questions:
                questions[question_id] = []

            questions[question_id].append(value)

    result = []

    for question_id, values in questions.items():

        average = sum(values) / len(values)

        result.append({"question_id": question_id, "average": round(average, 2)})

    return result
