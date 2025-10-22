from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os

app = FastAPI(title="ConvoSearch WebUI")

# Mount static files and templates
app.mount("/static", StaticFiles(directory="webui/static"), name="static")
templates = Jinja2Templates(directory="webui/templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/chat", response_class=HTMLResponse)
async def chat_interface(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})

@app.get("/triage", response_class=HTMLResponse)
async def triage_interface(request: Request):
    return templates.TemplateResponse("triage.html", {"request": request})