from fastapi import FastAPI, Form
from fastapi.templating import Jinja2Templates
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


@app.post("/analise-lexica")
def analise_lexica(codigo: str = Form(..., max_length=250)):
    print(f"Enviado: {codigo}")
    return templates.TemplateResponse(
        "result.html",
        {"result": {"tokens": analisador_lexico(codigo)}},
    )
