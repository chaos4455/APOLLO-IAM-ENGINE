from src.interface.webapp._templates import templates as T
from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from typing import Optional
from src.interface.webapp.api_client import api_client, auth_headers

router = APIRouter()


def _h(r: Request): return auth_headers(r.session["user"]["token"])


@router.get("/admin/users", response_class=HTMLResponse)
async def list_users(request: Request):
    async with api_client() as c:
        users = (await c.get("/admin/users/", headers=_h(request))).json()
    return T.TemplateResponse("users/list.html", {"request": request, "users": users or []})


@router.get("/admin/users/new", response_class=HTMLResponse)
async def new_user_form(request: Request):
    async with api_client() as c:
        roles  = (await c.get("/admin/roles/",       headers=_h(request))).json()
        groups = (await c.get("/admin/groups/",      headers=_h(request))).json()
        types  = (await c.get("/admin/user-types/",  headers=_h(request))).json()
        levels = (await c.get("/admin/user-levels/", headers=_h(request))).json()
    return T.TemplateResponse("users/form.html", {
        "request": request, "user": None,
        "roles": roles or [], "groups": groups or [],
        "types": types or [], "levels": levels or [],
        "error": request.query_params.get("error", ""),
    })


@router.post("/admin/users/new")
async def create_user(
    request: Request,
    username: str = Form(...), password: str = Form(...),
    email: Optional[str] = Form(None), full_name: Optional[str] = Form(None),
    is_active: Optional[str] = Form(None), is_superuser: Optional[str] = Form(None),
    group_id: Optional[str] = Form(None),
    type_id: Optional[str] = Form(None), level_id: Optional[str] = Form(None),
):
    payload = {
        "username": username, "password": password,
        "email": email or None, "full_name": full_name or None,
        "is_active": is_active == "on",
        "is_superuser": is_superuser == "on",
        "group_id": group_id or None,
        "type_id": type_id or None,
        "level_id": level_id or None,
        "role_names": [],
    }
    async with api_client() as c:
        r = await c.post("/admin/users/", json=payload, headers=_h(request))
    if r.status_code == 201:
        return RedirectResponse(url="/admin/users", status_code=302)
    err = r.json().get("detail", "Erro ao criar usuário")
    return RedirectResponse(url=f"/admin/users/new?error={err}", status_code=302)


@router.get("/admin/users/{user_id}", response_class=HTMLResponse)
async def user_detail(user_id: str, request: Request):
    async with api_client() as c:
        h = _h(request)
        user   = (await c.get(f"/admin/users/{user_id}", headers=h)).json()
        roles  = (await c.get("/admin/roles/",           headers=h)).json()
        groups = (await c.get("/admin/groups/",          headers=h)).json()
        attrs  = (await c.get("/admin/rbac/",            headers=h)).json()
        types  = (await c.get("/admin/user-types/",      headers=h)).json()
        levels = (await c.get("/admin/user-levels/",     headers=h)).json()
        ent_types = (await c.get("/admin/custom-entities/types", headers=h)).json()
        user_entities = (await c.get(f"/admin/custom-entities/user/{user_id}", headers=h)).json()
    return T.TemplateResponse("users/detail.html", {
        "request": request, "user": user,
        "all_roles": roles or [], "all_groups": groups or [],
        "all_attrs": attrs or [], "all_types": types or [],
        "all_levels": levels or [],
        "entity_types": ent_types or [],
        "user_entities": user_entities or [],
        "msg": request.query_params.get("msg", ""),
        "error": request.query_params.get("error", ""),
    })


@router.post("/admin/users/{user_id}/edit")
async def edit_user(
    user_id: str, request: Request,
    email: Optional[str] = Form(None), full_name: Optional[str] = Form(None),
    is_active: Optional[str] = Form(None), is_superuser: Optional[str] = Form(None),
    group_id: Optional[str] = Form(None),
    type_id: Optional[str] = Form(None), level_id: Optional[str] = Form(None),
):
    payload = {
        "email": email or None, "full_name": full_name or None,
        "is_active": is_active == "on",
        "is_superuser": is_superuser == "on",
        "group_id": group_id or None,
        "type_id": type_id or None,
        "level_id": level_id or None,
    }
    async with api_client() as c:
        r = await c.put(f"/admin/users/{user_id}", json=payload, headers=_h(request))
    if r.status_code == 200:
        return RedirectResponse(url=f"/admin/users/{user_id}?msg=Usuário+atualizado", status_code=302)
    return RedirectResponse(url=f"/admin/users/{user_id}?error=Erro+ao+atualizar", status_code=302)


@router.post("/admin/users/{user_id}/assign-role")
async def assign_role(user_id: str, request: Request, role_id: str = Form(...)):
    async with api_client() as c:
        await c.post(f"/admin/roles/{role_id}/assign-user/{user_id}", headers=_h(request))
    return RedirectResponse(url=f"/admin/users/{user_id}?msg=Role+atribuída", status_code=302)


@router.post("/admin/users/{user_id}/revoke-role")
async def revoke_role(user_id: str, request: Request, role_id: str = Form(...)):
    async with api_client() as c:
        await c.delete(f"/admin/roles/{role_id}/revoke-user/{user_id}", headers=_h(request))
    return RedirectResponse(url=f"/admin/users/{user_id}?msg=Role+revogada", status_code=302)


@router.post("/admin/users/{user_id}/assign-rbac")
async def assign_rbac(user_id: str, request: Request,
                      attribute_key: str = Form(...), value: str = Form(...)):
    async with api_client() as c:
        await c.post(f"/admin/rbac/assign/{user_id}",
                     json={"attribute_key": attribute_key, "value": value},
                     headers=_h(request))
    return RedirectResponse(url=f"/admin/users/{user_id}?msg=Atributo+RBAC+atribuído", status_code=302)


@router.post("/admin/users/{user_id}/assign-entity")
async def assign_entity(user_id: str, request: Request,
                        entity_type_slug: str = Form(...), entity_value_id: str = Form(...)):
    async with api_client() as c:
        await c.post(f"/admin/custom-entities/assign/{user_id}",
                     json={"entity_type_slug": entity_type_slug, "entity_value_id": entity_value_id},
                     headers=_h(request))
    return RedirectResponse(url=f"/admin/users/{user_id}?msg=Entidade+ABAC+atribuída", status_code=302)


@router.post("/admin/users/{user_id}/reset-password")
async def reset_password(user_id: str, request: Request, new_password: str = Form(...)):
    async with api_client() as c:
        await c.post(f"/admin/users/{user_id}/reset-password",
                     json={"new_password": new_password}, headers=_h(request))
    return RedirectResponse(url=f"/admin/users/{user_id}?msg=Senha+redefinida", status_code=302)


@router.post("/admin/users/{user_id}/toggle")
async def toggle_user(user_id: str, request: Request):
    async with api_client() as c:
        await c.post(f"/admin/users/{user_id}/toggle-status", headers=_h(request))
    return RedirectResponse(url="/admin/users", status_code=302)


@router.post("/admin/users/{user_id}/delete")
async def delete_user(user_id: str, request: Request):
    async with api_client() as c:
        await c.delete(f"/admin/users/{user_id}", headers=_h(request))
    return RedirectResponse(url="/admin/users", status_code=302)
