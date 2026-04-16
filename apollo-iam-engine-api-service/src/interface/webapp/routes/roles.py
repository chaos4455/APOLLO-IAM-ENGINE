from src.interface.webapp._templates import templates as T
from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from src.interface.webapp.api_client import api_client, auth_headers

router = APIRouter()


def _h(r: Request): return auth_headers(r.session["user"]["token"])


@router.get("/admin/roles", response_class=HTMLResponse)
async def list_roles(request: Request):
    async with api_client() as c:
        roles = (await c.get("/admin/roles/", headers=_h(request))).json()
        perms = (await c.get("/admin/permissions/", headers=_h(request))).json()
    return T.TemplateResponse("roles/list.html", {
        "request": request, "roles": roles or [], "all_perms": perms or [],
        "msg": request.query_params.get("msg", ""),
    })


@router.post("/admin/roles/new")
async def create_role(request: Request, name: str = Form(...), description: str = Form("")):
    async with api_client() as c:
        await c.post("/admin/roles/", json={"name": name, "description": description}, headers=_h(request))
    return RedirectResponse(url="/admin/roles?msg=Role+criada", status_code=302)


@router.post("/admin/roles/{role_id}/assign-perm")
async def assign_perm(role_id: str, request: Request, perm_id: str = Form(...)):
    async with api_client() as c:
        await c.post(f"/admin/permissions/{perm_id}/assign-role/{role_id}", headers=_h(request))
    return RedirectResponse(url="/admin/roles?msg=Permissão+atribuída", status_code=302)


@router.post("/admin/roles/{role_id}/delete")
async def delete_role(role_id: str, request: Request):
    async with api_client() as c:
        await c.delete(f"/admin/roles/{role_id}", headers=_h(request))
    return RedirectResponse(url="/admin/roles", status_code=302)
