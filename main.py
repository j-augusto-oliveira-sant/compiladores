from fastapi import FastAPI, Form, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

# from pydantic import BaseModel
from analisador_lexico import analisador_lexico

app = FastAPI(
    title="Compiladores",
    description="Materia IF",
    docs_url="/docs",
)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
def show_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/analise-lexica")
def analise_lexica(request: Request, codigo: str = Form(..., max_length=250)):
    return templates.TemplateResponse(
        "result.html",
        {"result": {"tokens": analisador_lexico(codigo)}, "request": request},
    )
