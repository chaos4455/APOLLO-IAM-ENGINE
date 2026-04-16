from src.interface.webapp._templates import templates as T
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, JSONResponse
from src.interface.webapp.api_client import api_client, auth_headers

router = APIRouter()


def _h(r: Request): return auth_headers(r.session["user"]["token"])


@router.get("/admin/metrics", response_class=HTMLResponse)
async def metrics_page(request: Request):
    async with api_client() as c:
        data = (await c.get("/admin/metrics/", headers=_h(request))).json()
    return T.TemplateResponse("metrics/dashboard.html", {"request": request, "m": data})


@router.get("/admin/metrics/live")
async def metrics_live(request: Request):
    """Endpoint JSON para polling em tempo real via JS."""
    async with api_client() as c:
        data = (await c.get("/admin/metrics/", headers=_h(request))).json()
    return JSONResponse(data)


@router.get("/admin/metrics/logs", response_class=HTMLResponse)
async def logs_page(request: Request, skip: int = 0, limit: int = 200):
    async with api_client() as c:
        data = (await c.get(f"/admin/metrics/logs?skip={skip}&limit={limit}",
                            headers=_h(request))).json()
    return T.TemplateResponse("metrics/logs.html", {
        "request": request, "data": data, "skip": skip, "limit": limit,
    })
