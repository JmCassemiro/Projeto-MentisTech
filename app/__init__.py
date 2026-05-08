from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api.register_routes import register_router
from app.api.home_routes import home_router
from app.api.hero_routes import hero_router
from app.api.forms_routes import forms_router
from app.api.email_routes import email_router


def create_app():
    app = FastAPI()

    app.mount(
        "/static",
        StaticFiles(directory="frontend/static"),
        name="static",
    )
    

    app.include_router(home_router)
    app.include_router(register_router)
    app.include_router(hero_router)
    app.include_router(forms_router)
    app.include_router(email_router)

    return app
