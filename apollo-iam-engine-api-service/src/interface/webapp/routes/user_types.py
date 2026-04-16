from src.interface.webapp._templates import templates as T
from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from src.interface.webapp.api_client import api_client, auth_headers

router = APIRouter()


def _h(r: Request): return auth_headers(r.session["user"]["token"])


@router.get("/admin/user-types", response_class=HTMLResponse)
async def list_types(request: Request):
    async with api_client() as c:
        types = (await c.get("/admin/user-types/", headers=_h(request))).json()
    return T.TemplateResponse("user_types/list.html", {
        "request": request, "types": types or [],
        "msg": request.query_params.get("msg", ""),
    })


@router.post("/admin/user-types/new")
async def create_type(request: Request, name: str = Form(...), description: str = Form("")):
    async with api_client() as c:
        await c.post("/admin/user-types/", json={"name": name, "description": description}, headers=_h(request))
    return RedirectResponse(url="/admin/user-types?msg=Tipo+criado", status_code=302)


@router.post("/admin/user-types/{type_id}/delete")
async def delete_type(type_id: str, request: Request):
    async with api_client() as c:
        await c.delete(f"/admin/user-types/{type_id}", headers=_h(request))
    return RedirectResponse(url="/admin/user-types", status_code=302)
