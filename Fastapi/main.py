from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
from sqlalchemy import create_engine

app = FastAPI()
# for static file
app.mount("/static", StaticFiles(directory="static"), name="static")

#for html templates 
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse(
        "index.html",{"request":request}
    )
