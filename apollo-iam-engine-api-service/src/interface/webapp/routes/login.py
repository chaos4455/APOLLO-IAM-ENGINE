from src.interface.webapp._templates import templates as T
from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from src.interface.webapp.api_client import api_client

router = APIRouter()


@router.get("/admin/login", response_class=HTMLResponse)
async def login_page(request: Request, error: str = ""):
    return T.TemplateResponse("login.html", {"request": request, "error": error})


@router.post("/admin/login")
async def login_submit(request: Request, username: str = Form(...), password: str = Form(...)):
    try:
        async with api_client() as c:
            r = await c.post("/auth/token", data={"username": username, "password": password})
        if r.status_code == 200:
            data = r.json()
            request.session["user"] = {"username": username, "token": data["access_token"]}
            return RedirectResponse(url="/admin/dashboard", status_code=302)
        error = "Credenciais inválidas."
    except Exception as e:
        error = f"API indisponível: {e}"
    return T.TemplateResponse("login.html", {"request": request, "error": error})


@router.get("/admin/logout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/admin/login", status_code=302)
