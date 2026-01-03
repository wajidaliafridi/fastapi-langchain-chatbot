from fastapi import FastAPI, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import uvicorn
from app.backend.routes.routers import router
from app.backend.db_conn.database_conn import get_db


app = FastAPI(title="Chat App",
              version="1.0.0")

templates = Jinja2Templates(directory="app/frontend/templates")
app.mount("/static", StaticFiles(directory="app/frontend/static"), name="static")
app.include_router(router, dependencies=[Depends(get_db)])

@app.get("/health", tags=["health"])
def health_check():
    return {"status": "ok"}


if __name__ == "__main__": 
    uvicorn.run("main:app", port=8000, reload=True)









