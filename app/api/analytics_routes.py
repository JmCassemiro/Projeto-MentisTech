import json
import unicodedata
from collections import defaultdict

from fastapi import APIRouter, Depends, HTTPException, Security, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user_bearer, get_db
from app.db.models.checkin import CheckIn
from app.db.models.user import User

analytics_router = APIRouter(prefix="/analytics", tags=["analytics"])


def normalize_text(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value or "")
    without_accents = "".join(
        char for char in normalized if not unicodedata.combining(char)
    )
    return without_accents.lower().strip()


def is_psychologist(user: User) -> bool:
    role = normalize_text(user.role)
    return "psicolog" in role or "pscolog" in role or "psicoloc" in role


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
        .join(User, CheckIn.user_id == User.id)
        .filter(User.role == team)
        .scalar()
    )

    return {"team": team, "average_stress": result}


@analytics_router.get("/mood-by-team/{team}")
def mood_by_team(team: str, db: Session = Depends(get_db)):
    result = (
        db.query(CheckIn.overall_mood, func.count(CheckIn.id).label("count"))
        .join(User, CheckIn.user_id == User.id)
        .filter(User.role == team)
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


@analytics_router.get("/company-overview")
def company_overview(
    db: Session = Depends(get_db),
    current_user: User = Security(get_current_user_bearer, scopes=[]),
):
    if not is_psychologist(current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Dashboard geral disponivel apenas para psicologos.",
        )

    users = (
        db.query(User)
        .filter(User.company_id == current_user.company_id)
        .order_by(User.full_name.asc())
        .all()
    )
    user_ids = [user.id for user in users]

    if not user_ids:
        return {
            "total_users": 0,
            "total_checkins": 0,
            "average_stress": None,
            "mood_distribution": [],
            "groups": [],
            "users": [],
        }

    checkins = (
        db.query(CheckIn)
        .filter(CheckIn.user_id.in_(user_ids))
        .order_by(CheckIn.created_at.desc())
        .all()
    )

    checkins_by_user: dict[int, list[CheckIn]] = defaultdict(list)
    mood_counts: dict[str, int] = defaultdict(int)
    group_stats: dict[str, dict[str, object]] = {}
    total_stress = 0

    users_by_id = {user.id: user for user in users}

    for checkin in checkins:
        user = users_by_id.get(checkin.user_id)

        if user is None:
            continue

        group = user.role or "Sem cargo"
        group_stats.setdefault(
            group,
            {
                "group": group,
                "users": set(),
                "checkins": 0,
                "stress_total": 0,
            },
        )

        checkins_by_user[checkin.user_id].append(checkin)
        mood_counts[checkin.overall_mood] += 1
        total_stress += checkin.stress_level
        group_stats[group]["users"].add(user.id)
        group_stats[group]["checkins"] += 1
        group_stats[group]["stress_total"] += checkin.stress_level

    groups = []
    for stats in group_stats.values():
        checkin_count = int(stats["checkins"])
        stress_total = int(stats["stress_total"])
        groups.append(
            {
                "group": stats["group"],
                "users": len(stats["users"]),
                "checkins": checkin_count,
                "average_stress": round(stress_total / checkin_count, 2)
                if checkin_count
                else None,
            }
        )

    user_rows = []
    for user in users:
        user_checkins = checkins_by_user.get(user.id, [])
        latest_checkin = user_checkins[0] if user_checkins else None
        user_rows.append(
            {
                "id": user.id,
                "name": user.full_name,
                "role": user.role,
                "checkins": len(user_checkins),
                "last_mood": latest_checkin.overall_mood if latest_checkin else None,
                "last_stress": latest_checkin.stress_level if latest_checkin else None,
            }
        )

    return {
        "total_users": len(users),
        "total_checkins": len(checkins),
        "average_stress": round(total_stress / len(checkins), 2)
        if checkins
        else None,
        "mood_distribution": [
            {"mood": mood, "count": count}
            for mood, count in sorted(
                mood_counts.items(),
                key=lambda item: item[1],
                reverse=True,
            )
        ],
        "groups": sorted(groups, key=lambda item: item["group"]),
        "users": user_rows,
    }


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
