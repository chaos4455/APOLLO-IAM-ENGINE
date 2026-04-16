from src.interface.webapp._templates import templates as T
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from src.interface.webapp.api_client import api_client, auth_headers

router = APIRouter()


@router.get("/admin/audit", response_class=HTMLResponse)
async def list_logs(request: Request, skip: int = 0, limit: int = 100):
    tok = request.session["user"]["token"]
    async with api_client() as c:
        logs = (await c.get(f"/admin/audit/?skip={skip}&limit={limit}",
                            headers=auth_headers(tok))).json()
    return T.TemplateResponse("audit/list.html", {
        "request": request, "logs": logs or [],
        "skip": skip, "limit": limit,
    })
