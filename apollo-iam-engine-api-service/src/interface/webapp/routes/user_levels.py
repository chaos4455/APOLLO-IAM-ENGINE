from src.interface.webapp._templates import templates as T
from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from src.interface.webapp.api_client import api_client, auth_headers

router = APIRouter()


def _h(r: Request): return auth_headers(r.session["user"]["token"])


@router.get("/admin/user-levels", response_class=HTMLResponse)
async def list_levels(request: Request):
    async with api_client() as c:
        levels = (await c.get("/admin/user-levels/", headers=_h(request))).json()
    return T.TemplateResponse("user_levels/list.html", {
        "request": request, "levels": levels or [],
        "msg": request.query_params.get("msg", ""),
    })


@router.post("/admin/user-levels/new")
async def create_level(request: Request, name: str = Form(...),
                       rank: int = Form(0), description: str = Form("")):
    async with api_client() as c:
        await c.post("/admin/user-levels/",
                     json={"name": name, "rank": rank, "description": description},
                     headers=_h(request))
    return RedirectResponse(url="/admin/user-levels?msg=Nível+criado", status_code=302)


@router.post("/admin/user-levels/{level_id}/delete")
async def delete_level(level_id: str, request: Request):
    async with api_client() as c:
        await c.delete(f"/admin/user-levels/{level_id}", headers=_h(request))
    return RedirectResponse(url="/admin/user-levels", status_code=302)
