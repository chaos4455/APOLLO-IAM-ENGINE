from src.interface.webapp._templates import templates as T
from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from src.interface.webapp.api_client import api_client, auth_headers

router = APIRouter()


def _h(r: Request): return auth_headers(r.session["user"]["token"])


@router.get("/admin/groups", response_class=HTMLResponse)
async def list_groups(request: Request):
    async with api_client() as c:
        groups = (await c.get("/admin/groups/", headers=_h(request))).json()
    return T.TemplateResponse("groups/list.html", {
        "request": request, "groups": groups or [],
        "msg": request.query_params.get("msg", ""),
    })


@router.post("/admin/groups/new")
async def create_group(request: Request, name: str = Form(...), description: str = Form("")):
    async with api_client() as c:
        await c.post("/admin/groups/", json={"name": name, "description": description}, headers=_h(request))
    return RedirectResponse(url="/admin/groups?msg=Grupo+criado", status_code=302)


@router.post("/admin/groups/{group_id}/delete")
async def delete_group(group_id: str, request: Request):
    async with api_client() as c:
        await c.delete(f"/admin/groups/{group_id}", headers=_h(request))
    return RedirectResponse(url="/admin/groups", status_code=302)
