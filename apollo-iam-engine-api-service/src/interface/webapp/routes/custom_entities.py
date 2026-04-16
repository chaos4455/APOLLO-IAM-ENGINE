from src.interface.webapp._templates import templates as T
from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from src.interface.webapp.api_client import api_client, auth_headers

router = APIRouter()


def _h(r: Request): return auth_headers(r.session["user"]["token"])


@router.get("/admin/entities", response_class=HTMLResponse)
async def list_entity_types(request: Request):
    async with api_client() as c:
        types = (await c.get("/admin/custom-entities/types", headers=_h(request))).json()
    return T.TemplateResponse("entities/list.html", {
        "request": request, "types": types or [],
        "msg": request.query_params.get("msg", ""),
    })


@router.post("/admin/entities/new-type")
async def create_type(request: Request, slug: str = Form(...),
                      label: str = Form(...), description: str = Form("")):
    async with api_client() as c:
        await c.post("/admin/custom-entities/types",
                     json={"slug": slug, "label": label, "description": description},
                     headers=_h(request))
    return RedirectResponse(url="/admin/entities?msg=Tipo+criado", status_code=302)


@router.get("/admin/entities/{slug}", response_class=HTMLResponse)
async def entity_values(slug: str, request: Request):
    async with api_client() as c:
        h = _h(request)
        type_info = (await c.get(f"/admin/custom-entities/types/{slug}", headers=h)).json()
        values    = (await c.get(f"/admin/custom-entities/{slug}/values", headers=h)).json()
    return T.TemplateResponse("entities/values.html", {
        "request": request, "type_info": type_info,
        "values": values or [], "slug": slug,
        "msg": request.query_params.get("msg", ""),
    })


@router.post("/admin/entities/{slug}/new-value")
async def create_value(slug: str, request: Request,
                       name: str = Form(...), description: str = Form("")):
    async with api_client() as c:
        await c.post(f"/admin/custom-entities/{slug}/values",
                     json={"name": name, "description": description, "metadata": {}},
                     headers=_h(request))
    return RedirectResponse(url=f"/admin/entities/{slug}?msg=Valor+criado", status_code=302)


@router.post("/admin/entities/{slug}/delete-value/{value_id}")
async def delete_value(slug: str, value_id: str, request: Request):
    async with api_client() as c:
        await c.delete(f"/admin/custom-entities/{slug}/values/{value_id}", headers=_h(request))
    return RedirectResponse(url=f"/admin/entities/{slug}", status_code=302)


@router.post("/admin/entities/delete-type/{slug}")
async def delete_type(slug: str, request: Request):
    async with api_client() as c:
        await c.delete(f"/admin/custom-entities/types/{slug}", headers=_h(request))
    return RedirectResponse(url="/admin/entities", status_code=302)


from fastapi.responses import JSONResponse

@router.get("/admin/entities/{slug}/values-json")
async def values_json(slug: str, request: Request):
    async with api_client() as c:
        r = await c.get(f"/admin/custom-entities/{slug}/values", headers=_h(request))
    return JSONResponse(r.json() if r.status_code == 200 else [])
