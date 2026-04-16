from src.interface.webapp._templates import templates as T
from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from src.interface.webapp.api_client import api_client, auth_headers

router = APIRouter()


def _h(r: Request): return auth_headers(r.session["user"]["token"])


@router.get("/admin/rbac", response_class=HTMLResponse)
async def list_attrs(request: Request):
    async with api_client() as c:
        attrs = (await c.get("/admin/rbac/", headers=_h(request))).json()
    return T.TemplateResponse("rbac/list.html", {
        "request": request, "attributes": attrs or [],
        "msg": request.query_params.get("msg", ""),
    })


@router.post("/admin/rbac/new")
async def create_attr(request: Request, key: str = Form(...), label: str = Form(...),
                      value_type: str = Form("string"), description: str = Form("")):
    async with api_client() as c:
        await c.post("/admin/rbac/",
                     json={"key": key, "label": label, "value_type": value_type, "description": description},
                     headers=_h(request))
    return RedirectResponse(url="/admin/rbac?msg=Atributo+criado", status_code=302)


@router.post("/admin/rbac/{attr_id}/delete")
async def delete_attr(attr_id: str, request: Request):
    async with api_client() as c:
        await c.delete(f"/admin/rbac/{attr_id}", headers=_h(request))
    return RedirectResponse(url="/admin/rbac", status_code=302)
