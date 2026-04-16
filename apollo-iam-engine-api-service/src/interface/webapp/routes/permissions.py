from src.interface.webapp._templates import templates as T
from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from src.interface.webapp.api_client import api_client, auth_headers

router = APIRouter()


def _h(r: Request): return auth_headers(r.session["user"]["token"])


@router.get("/admin/permissions", response_class=HTMLResponse)
async def list_perms(request: Request):
    async with api_client() as c:
        perms = (await c.get("/admin/permissions/", headers=_h(request))).json()
    return T.TemplateResponse("permissions/list.html", {
        "request": request, "permissions": perms or [],
        "msg": request.query_params.get("msg", ""),
    })


@router.post("/admin/permissions/new")
async def create_perm(request: Request, name: str = Form(...), resource: str = Form(...),
                      action: str = Form(...), description: str = Form("")):
    async with api_client() as c:
        await c.post("/admin/permissions/",
                     json={"name": name, "resource": resource, "action": action, "description": description},
                     headers=_h(request))
    return RedirectResponse(url="/admin/permissions?msg=Permissão+criada", status_code=302)


@router.post("/admin/permissions/{perm_id}/delete")
async def delete_perm(perm_id: str, request: Request):
    async with api_client() as c:
        await c.delete(f"/admin/permissions/{perm_id}", headers=_h(request))
    return RedirectResponse(url="/admin/permissions", status_code=302)
