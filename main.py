from fastapi import FastAPI, Form, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from analisador_lexico import AnalisadorLexico

app = FastAPI(
    title="Compiladores",
    description="Materia IF",
    docs_url="/docs",
)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

analisador_lexico = AnalisadorLexico()


@app.get("/", response_class=HTMLResponse)
async def show_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/analise-lexica")
async def analise_lexica(
    request: Request, codigo: str = Form(..., max_length=2500), mode: str = Form(...)
):
    tokens = analisador_lexico.tokenize_code(codigo)
    if mode == "formatted_mode":
        return templates.TemplateResponse(
            "formatted_result.html",
            {"tokens": tokens, "request": request},
        )
    else:
        return tokens
