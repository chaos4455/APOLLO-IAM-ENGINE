from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import RedirectResponse


class SessionAuthMiddleware(BaseHTTPMiddleware):
    """Redireciona para /admin/login se não houver sessão ativa."""

    EXEMPT = {"/admin/login", "/admin/login/", "/admin/logout"}

    async def dispatch(self, request: Request, call_next):
        path = request.url.path

        # sempre libera static files e rotas de login
        if path.startswith("/static") or path in self.EXEMPT:
            return await call_next(request)

        # rotas que não são /admin não precisam de sessão
        if not path.startswith("/admin"):
            return await call_next(request)

        # verifica sessão — com try/except caso o SessionMiddleware
        # ainda não tenha inicializado (ordem de middleware incorreta)
        try:
            user = request.session.get("user")
        except AssertionError:
            # SessionMiddleware não inicializado ainda
            return RedirectResponse(url="/admin/login", status_code=302)

        if not user:
            return RedirectResponse(url="/admin/login", status_code=302)

        return await call_next(request)
