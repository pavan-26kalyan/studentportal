from fastapi import FastAPI, Request,Form,Depends,Query
from fastapi.responses import HTMLResponse,RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from typing import Annotated
from pydantic import BaseModel

from database import engine, Base,SessionLocal
from models import Forms
DATABASE_URL = "sqlite:///./task.db"


Base.metadata.create_all(bind=engine)

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
#this function helps to create temp connection between backend and server
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class Inputtype(BaseModel):
        first_name:str
        last_name:str
        phone_number:str
        email:str
        gender:str
        city:str
        role:str

@app.get("/", response_class=HTMLResponse)
def home(req: Request):
    return templates.TemplateResponse(
        request=req,
        name="login.html",

    )
@app.get("/register", response_class=HTMLResponse)
def home(req: Request):
    return templates.TemplateResponse(
        request=req,
        name="register.html"

    )


@app.post('/register')
def register(user:Annotated[Inputtype,Form()],db=Depends(get_db)):
    new_user = Forms(
        first_name=user.first_name,
        last_name=user.last_name,
        phone_number=user.phone_number,
        email=user.email,
        gender=user.gender,
        city=user.city,
        role=user.role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return RedirectResponse(
        url="/",
        status_code=303
    )
