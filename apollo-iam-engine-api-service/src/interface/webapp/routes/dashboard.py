from src.interface.webapp._templates import templates as T
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from src.interface.webapp.api_client import api_client, auth_headers

router = APIRouter()


@router.get("/admin/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    tok = request.session["user"]["token"]
    h = auth_headers(tok)
    async with api_client() as c:
        users   = (await c.get("/admin/users/",       headers=h)).json()
        roles   = (await c.get("/admin/roles/",       headers=h)).json()
        groups  = (await c.get("/admin/groups/",      headers=h)).json()
        perms   = (await c.get("/admin/permissions/", headers=h)).json()
        attrs   = (await c.get("/admin/rbac/",        headers=h)).json()
        logs    = (await c.get("/admin/audit/?limit=5", headers=h)).json()
        types   = (await c.get("/admin/user-types/",  headers=h)).json()
        levels  = (await c.get("/admin/user-levels/", headers=h)).json()
        ent_types = (await c.get("/admin/custom-entities/types", headers=h)).json()

    def _n(v): return len(v) if isinstance(v, list) else 0

    stats = {
        "users": _n(users), "roles": _n(roles), "groups": _n(groups),
        "permissions": _n(perms), "rbac_attrs": _n(attrs),
        "user_types": _n(types), "user_levels": _n(levels),
        "entity_types": _n(ent_types),
    }
    recent_logs = logs[:5] if isinstance(logs, list) else []
    return T.TemplateResponse("dashboard.html", {
        "request": request, "stats": stats, "recent_logs": recent_logs,
    })
