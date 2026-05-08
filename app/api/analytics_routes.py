from fastapi import APIRouter

analytics_router = APIRouter(prefix="/analytics", tags=["analytics"])


@analytics_router.get("mood-by-user/{user_id}")
def mood_by_user():
    pass


@analytics_router.get("mood-by-user-monthly/{user_id}")
def mood_by_user_monthly():
    pass


@analytics_router.get(f"overall-mood/{user_id}")
def overall_mood_by_user():
    pass


@analytics_router.get(f"overall-mood/{role}")
def overall_mood_by_role():
    pass


@analytics_router.get(f"overall-mood/{team}")
def overall_mood_by_team():
    pass


@analytics_router.get("stress-by-team/team")
def stress_by_team():
    pass


@analytics_router.get("stress-by-role/role")
def stress_by_role():
    pass


@analytics_router.get("questions-avarage")
def questions_avarage():
    pass
