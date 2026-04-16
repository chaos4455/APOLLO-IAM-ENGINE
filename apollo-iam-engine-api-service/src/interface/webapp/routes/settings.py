from src.interface.webapp._templates import templates as T
from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from src.interface.webapp.api_client import api_client, auth_headers

router = APIRouter()


def _h(r: Request): return auth_headers(r.session["user"]["token"])


@router.get("/admin/settings", response_class=HTMLResponse)
async def settings_page(request: Request):
    async with api_client() as c:
        s = (await c.get("/admin/settings/", headers=_h(request))).json()
    return T.TemplateResponse("settings/index.html", {
        "request": request, "settings": s,
        "msg": request.query_params.get("msg", ""),
    })


@router.post("/admin/settings")
async def update_settings(
    request: Request,
    access_token_expire_minutes: int = Form(60),
    refresh_token_expire_days: int = Form(7),
    allow_registration: str = Form(None),
    max_login_attempts: int = Form(5),
    lockout_minutes: int = Form(15),
):
    payload = {
        "access_token_expire_minutes": access_token_expire_minutes,
        "refresh_token_expire_days": refresh_token_expire_days,
        "allow_registration": allow_registration == "on",
        "max_login_attempts": max_login_attempts,
        "lockout_minutes": lockout_minutes,
    }
    async with api_client() as c:
        await c.put("/admin/settings/", json=payload, headers=_h(request))
    return RedirectResponse(url="/admin/settings?msg=Configurações+salvas", status_code=302)
