import uvicorn
from fastapi import FastAPI

from api.forms_router import forms_router
from api.email_router import email_router

app = FastAPI()
app.include_router(forms_router)
app.include_router(email_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
