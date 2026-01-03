from fastapi import FastAPI, Request, Depends, HTTPException, status, Body, APIRouter, Form
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from urllib.parse import unquote_plus
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from app.backend.chat.chat import Chat
from app.backend.auth.auths import create_access_token, get_current_user, verify_password, hash_password, get_db
from app.backend.model.dbmodel import User, UserMessages


router = APIRouter(
    tags=["api"]
)

templates = Jinja2Templates(directory="app/frontend/templates")


@router.get("/", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.get("/signup", response_class=HTMLResponse)
def signup_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@router.post("/signup")
async def signup(request: Request, name: str = Form(...), email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    hashed_pwd = hash_password(password)
    existing_user = db.query(User).filter(User.email == email).first()
    if existing_user:
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "error": "Email already registered"}
        )

    user = User(name=name, email=email, password_hashed = hashed_pwd)
    try:
        db.add(user)
        db.commit()
        db.refresh(user)
    except Exception:
        db.rollback()
        raise
    return RedirectResponse(url="/", status_code=303)


@router.post("/login")
async def login(request: Request, email: str = Form(...), password : str = Form(...), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.password_hashed):
        return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid email or password"})
    access_token = create_access_token(data={"sub": user.email})
    response = RedirectResponse(url="/chat", status_code=303)
    response.set_cookie(key="access_token", value=access_token)
    return response


@router.get("/chat", response_class=HTMLResponse)
async def chat_page(request: Request, current_user: User = Depends(get_current_user)):
    return templates.TemplateResponse("chat_page.html",{"request": request, "email": current_user.email} )


@router.post("/chat", response_class=JSONResponse)
async def chat(message: str = Body(..., embed=True)):
    clean_message = unquote_plus(message)
    chat = Chat()
    response = chat.get_response(clean_message)
    return {"response": response.content}


@router.post("/logout")
def logout(request: Request, db: Session = Depends(get_db)):
    response = RedirectResponse(url="/")
    response.delete_cookie(key="access_token")
    return response
