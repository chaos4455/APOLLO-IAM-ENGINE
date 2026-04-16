
"""
fix-v2.py — Apollo IAM Engine API Service
Completa o que o populate e fix-v1 deixaram incompleto:
  1. Templates HTML (base, login, dashboard, users, roles, permissions, groups, rbac, settings, audit, partials, errors)
  2. api/main.py completo
  3. webapp CSS + JS
  4. __main__ com relatório rico (rich + colorama) em todos os 3 scripts
  5. Adiciona __main__ ao create_apollo_iam.py e populate_apollo_iam.py
O2 Data Solutions
"""

import os
import time

BASE = "apollo-iam-engine-api-service"


def w(rel: str, content: str):
    path = os.path.join(BASE, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return path


# ===========================================================================
# TEMPLATES HTML
# ===========================================================================

def templates_base():
    w("src/interface/webapp/templates/base.html", """\
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>{% block title %}Apollo IAM{% endblock %} — O2 Data Solutions</title>
  <link rel="stylesheet" href="/static/css/main.css"/>
  {% block head %}{% endblock %}
</head>
<body>
<div class="layout">
  {% include "partials/sidebar.html" %}
  <div class="main-content">
    {% include "partials/navbar.html" %}
    <main class="page">
      {% include "partials/alerts.html" %}
      {% block content %}{% endblock %}
    </main>
    {% include "partials/footer.html" %}
  </div>
</div>
<script src="/static/js/main.js"></script>
{% block scripts %}{% endblock %}
</body>
</html>
""")

    w("src/interface/webapp/templates/login.html", """\
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Login — Apollo IAM</title>
  <link rel="stylesheet" href="/static/css/main.css"/>
</head>
<body>
<div class="login-page">
  <div class="login-card">
    <div class="login-logo">
      <div class="logo-icon">🔐</div>
      <h1>Apollo IAM Engine</h1>
      <p>O2 Data Solutions — Painel de Controle</p>
    </div>
    {% if error %}
    <div class="alert alert-error">⚠️ {{ error }}</div>
    {% endif %}
    <form method="post" action="/admin/login">
      <div class="form-group">
        <label class="form-label">Usuário</label>
        <input class="form-control" type="text" name="username" placeholder="admin" required autofocus/>
      </div>
      <div class="form-group">
        <label class="form-label">Senha</label>
        <input class="form-control" type="password" name="password" placeholder="••••••••" required/>
      </div>
      <button class="btn btn-primary" style="width:100%;justify-content:center;margin-top:8px" type="submit">
        🚀 Entrar
      </button>
    </form>
    <div style="text-align:center;margin-top:20px;font-size:.75rem;color:var(--text-muted)">
      Apollo IAM Engine v1.0.0
    </div>
  </div>
</div>
</body>
</html>
""")

    w("src/interface/webapp/templates/dashboard.html", """\
{% extends "base.html" %}
{% block title %}Dashboard{% endblock %}
{% block content %}
<div class="page-header">
  <h1 class="page-title">📊 Dashboard</h1>
</div>
<div class="stat-grid">
  <div class="stat-card">
    <div class="stat-icon">👤</div>
    <div><div class="stat-value">{{ stats.users }}</div><div class="stat-label">Usuários</div></div>
  </div>
  <div class="stat-card">
    <div class="stat-icon">🎭</div>
    <div><div class="stat-value">{{ stats.roles }}</div><div class="stat-label">Roles</div></div>
  </div>
  <div class="stat-card">
    <div class="stat-icon">👥</div>
    <div><div class="stat-value">{{ stats.groups }}</div><div class="stat-label">Grupos</div></div>
  </div>
  <div class="stat-card">
    <div class="stat-icon">🔑</div>
    <div><div class="stat-value">{{ stats.permissions }}</div><div class="stat-label">Permissões</div></div>
  </div>
</div>
<div class="card">
  <h3 style="margin-bottom:12px;font-size:1rem">🚀 Início Rápido</h3>
  <p style="color:var(--text-muted);font-size:.9rem;line-height:1.6">
    Bem-vindo ao <strong>Apollo IAM Engine</strong>. Use o menu lateral para gerenciar
    usuários, roles, permissões, grupos e atributos RBAC.<br/>
    A API REST está disponível em <a href="http://localhost:8000/docs" target="_blank"
    style="color:var(--primary)">http://localhost:8000/docs</a>.
  </p>
</div>
{% endblock %}
""")


def templates_partials():
    w("src/interface/webapp/templates/partials/sidebar.html", """\
<aside class="sidebar">
  <div class="sidebar-logo">
    <span>🔐 Apollo IAM</span>
  </div>
  <nav class="sidebar-nav">
    <div class="nav-section">Principal</div>
    <a class="nav-item" href="/admin/dashboard">📊 Dashboard</a>
    <div class="nav-section">IAM</div>
    <a class="nav-item" href="/admin/users">👤 Usuários</a>
    <a class="nav-item" href="/admin/groups">👥 Grupos</a>
    <div class="nav-section">RBAC</div>
    <a class="nav-item" href="/admin/roles">🎭 Roles</a>
    <a class="nav-item" href="/admin/permissions">🔑 Permissões</a>
    <a class="nav-item" href="/admin/rbac">🏷️ Atributos RBAC</a>
    <div class="nav-section">Sistema</div>
    <a class="nav-item" href="/admin/settings">⚙️ Configurações</a>
    <a class="nav-item" href="/admin/audit">📋 Audit Logs</a>
    <a class="nav-item" href="/admin/logout" style="margin-top:auto">🚪 Sair</a>
  </nav>
</aside>
""")

    w("src/interface/webapp/templates/partials/navbar.html", """\
<header class="navbar">
  <span class="navbar-title">{% block navbar_title %}Apollo IAM Engine{% endblock %}</span>
  <div class="navbar-user">
    <div class="avatar">{{ request.session.get('user', {}).get('username', 'A')[0].upper() }}</div>
    <span>{{ request.session.get('user', {}).get('username', 'admin') }}</span>
  </div>
</header>
""")

    w("src/interface/webapp/templates/partials/footer.html", """\
<footer class="footer">
  <div class="footer-brand">
    🔐 Apollo IAM Engine v1.0.0 &nbsp;|&nbsp; Criado por <span>O2 Data Solutions</span>
  </div>
  <div>© 2024 O2 Data Solutions. Todos os direitos reservados.</div>
</footer>
""")

    w("src/interface/webapp/templates/partials/alerts.html", """\
{% if request.query_params.get('success') %}
<div class="alert alert-success" data-dismiss>✅ {{ request.query_params.get('success') }}</div>
{% endif %}
{% if request.query_params.get('error') %}
<div class="alert alert-error" data-dismiss>⚠️ {{ request.query_params.get('error') }}</div>
{% endif %}
""")


def templates_users():
    w("src/interface/webapp/templates/users/list.html", """\
{% extends "base.html" %}
{% block title %}Usuários{% endblock %}
{% block content %}
<div class="page-header">
  <h1 class="page-title">👤 Usuários</h1>
  <a class="btn btn-primary" href="/admin/users/new">➕ Novo Usuário</a>
</div>
<div class="card">
  <div class="table-wrap">
    <table>
      <thead><tr>
        <th>Usuário</th><th>E-mail</th><th>Roles</th><th>Status</th><th>Ações</th>
      </tr></thead>
      <tbody>
      {% for u in users %}
      <tr>
        <td><strong>{{ u.username }}</strong>{% if u.is_superuser %} <span class="badge badge-warning">superadmin</span>{% endif %}</td>
        <td>{{ u.email or '—' }}</td>
        <td>{% for r in u.roles %}<span class="badge badge-primary">{{ r }}</span> {% endfor %}</td>
        <td>
          {% if u.is_active %}<span class="badge badge-success">✅ Ativo</span>
          {% else %}<span class="badge badge-danger">❌ Inativo</span>{% endif %}
        </td>
        <td style="display:flex;gap:6px">
          <form method="post" action="/admin/users/{{ u.id }}/toggle">
            <button class="btn btn-outline btn-sm" type="submit">🔄</button>
          </form>
          <form method="post" action="/admin/users/{{ u.id }}/delete"
                onsubmit="return confirm('Excluir usuário {{ u.username }}?')">
            <button class="btn btn-danger btn-sm" type="submit">🗑️</button>
          </form>
        </td>
      </tr>
      {% else %}
      <tr><td colspan="5" style="text-align:center;color:var(--text-muted)">Nenhum usuário encontrado.</td></tr>
      {% endfor %}
      </tbody>
    </table>
  </div>
</div>
{% endblock %}
""")

    w("src/interface/webapp/templates/users/form.html", """\
{% extends "base.html" %}
{% block title %}Novo Usuário{% endblock %}
{% block content %}
<div class="page-header">
  <h1 class="page-title">➕ Novo Usuário</h1>
  <a class="btn btn-outline" href="/admin/users">← Voltar</a>
</div>
{% if error %}<div class="alert alert-error">⚠️ {{ error }}</div>{% endif %}
<div class="card" style="max-width:560px">
  <form method="post" action="/admin/users/new">
    <div class="form-group">
      <label class="form-label">Usuário *</label>
      <input class="form-control" name="username" placeholder="user, nome.sobrenome, email@..." required/>
    </div>
    <div class="form-group">
      <label class="form-label">Senha *</label>
      <input class="form-control" type="password" name="password" required/>
    </div>
    <div class="form-group">
      <label class="form-label">E-mail</label>
      <input class="form-control" type="email" name="email"/>
    </div>
    <div class="form-group">
      <label class="form-label">Nome completo</label>
      <input class="form-control" name="full_name"/>
    </div>
    <div class="form-group">
      <label class="form-label">Grupo</label>
      <select class="form-control" name="group_id">
        <option value="">— Sem grupo —</option>
        {% for g in groups %}<option value="{{ g.id }}">{{ g.name }}</option>{% endfor %}
      </select>
    </div>
    <button class="btn btn-primary" type="submit">💾 Criar Usuário</button>
  </form>
</div>
{% endblock %}
""")

    w("src/interface/webapp/templates/users/detail.html", """\
{% extends "base.html" %}
{% block title %}Usuário{% endblock %}
{% block content %}
<div class="page-header">
  <h1 class="page-title">👤 {{ user.username }}</h1>
  <a class="btn btn-outline" href="/admin/users">← Voltar</a>
</div>
<div class="card">
  <p><strong>ID:</strong> {{ user.id }}</p>
  <p><strong>E-mail:</strong> {{ user.email or '—' }}</p>
  <p><strong>Status:</strong> {{ 'Ativo' if user.is_active else 'Inativo' }}</p>
  <p><strong>Roles:</strong> {{ user.roles | join(', ') or '—' }}</p>
</div>
{% endblock %}
""")


def templates_roles():
    w("src/interface/webapp/templates/roles/list.html", """\
{% extends "base.html" %}
{% block title %}Roles{% endblock %}
{% block content %}
<div class="page-header">
  <h1 class="page-title">🎭 Roles</h1>
</div>
<div class="card" style="margin-bottom:20px;max-width:480px">
  <h3 style="margin-bottom:14px;font-size:.95rem">➕ Nova Role</h3>
  <form method="post" action="/admin/roles/new" style="display:flex;gap:10px;flex-wrap:wrap">
    <input class="form-control" name="name" placeholder="Nome da role" required style="flex:1;min-width:160px"/>
    <input class="form-control" name="description" placeholder="Descrição" style="flex:2;min-width:160px"/>
    <button class="btn btn-primary" type="submit">Criar</button>
  </form>
</div>
<div class="card">
  <div class="table-wrap">
    <table>
      <thead><tr><th>Nome</th><th>Descrição</th><th>Permissões</th><th>Ações</th></tr></thead>
      <tbody>
      {% for r in roles %}
      <tr>
        <td><strong>{{ r.name }}</strong></td>
        <td>{{ r.description or '—' }}</td>
        <td>{{ r.permissions | length }}</td>
        <td>
          <form method="post" action="/admin/roles/{{ r.id }}/delete"
                onsubmit="return confirm('Excluir role {{ r.name }}?')">
            <button class="btn btn-danger btn-sm" type="submit">🗑️</button>
          </form>
        </td>
      </tr>
      {% else %}
      <tr><td colspan="4" style="text-align:center;color:var(--text-muted)">Nenhuma role.</td></tr>
      {% endfor %}
      </tbody>
    </table>
  </div>
</div>
{% endblock %}
""")

    w("src/interface/webapp/templates/roles/form.html", """\
{% extends "base.html" %}
{% block title %}Role{% endblock %}
{% block content %}
<div class="page-header"><h1 class="page-title">🎭 Role</h1></div>
{% endblock %}
""")


def templates_permissions():
    w("src/interface/webapp/templates/permissions/list.html", """\
{% extends "base.html" %}
{% block title %}Permissões{% endblock %}
{% block content %}
<div class="page-header">
  <h1 class="page-title">🔑 Permissões</h1>
</div>
<div class="card" style="margin-bottom:20px;max-width:640px">
  <h3 style="margin-bottom:14px;font-size:.95rem">➕ Nova Permissão</h3>
  <form method="post" action="/admin/permissions/new" style="display:flex;gap:10px;flex-wrap:wrap">
    <input class="form-control" name="name" placeholder="users:read" required style="flex:1;min-width:120px"/>
    <input class="form-control" name="resource" placeholder="resource" required style="flex:1;min-width:100px"/>
    <input class="form-control" name="action" placeholder="action" required style="flex:1;min-width:80px"/>
    <button class="btn btn-primary" type="submit">Criar</button>
  </form>
</div>
<div class="card">
  <div class="table-wrap">
    <table>
      <thead><tr><th>Nome</th><th>Resource</th><th>Action</th><th>Ações</th></tr></thead>
      <tbody>
      {% for p in permissions %}
      <tr>
        <td><span class="badge badge-info">{{ p.name }}</span></td>
        <td>{{ p.resource }}</td>
        <td>{{ p.action }}</td>
        <td>
          <form method="post" action="/admin/permissions/{{ p.id }}/delete"
                onsubmit="return confirm('Excluir?')">
            <button class="btn btn-danger btn-sm" type="submit">🗑️</button>
          </form>
        </td>
      </tr>
      {% else %}
      <tr><td colspan="4" style="text-align:center;color:var(--text-muted)">Nenhuma permissão.</td></tr>
      {% endfor %}
      </tbody>
    </table>
  </div>
</div>
{% endblock %}
""")

    w("src/interface/webapp/templates/permissions/form.html", """\
{% extends "base.html" %}
{% block title %}Permissão{% endblock %}
{% block content %}
<div class="page-header"><h1 class="page-title">🔑 Permissão</h1></div>
{% endblock %}
""")


def templates_groups():
    w("src/interface/webapp/templates/groups/list.html", """\
{% extends "base.html" %}
{% block title %}Grupos{% endblock %}
{% block content %}
<div class="page-header">
  <h1 class="page-title">👥 Grupos</h1>
</div>
<div class="card" style="margin-bottom:20px;max-width:480px">
  <h3 style="margin-bottom:14px;font-size:.95rem">➕ Novo Grupo</h3>
  <form method="post" action="/admin/groups/new" style="display:flex;gap:10px;flex-wrap:wrap">
    <input class="form-control" name="name" placeholder="Nome do grupo" required style="flex:1;min-width:160px"/>
    <input class="form-control" name="description" placeholder="Descrição" style="flex:2;min-width:160px"/>
    <button class="btn btn-primary" type="submit">Criar</button>
  </form>
</div>
<div class="card">
  <div class="table-wrap">
    <table>
      <thead><tr><th>Nome</th><th>Descrição</th><th>Status</th><th>Ações</th></tr></thead>
      <tbody>
      {% for g in groups %}
      <tr>
        <td><strong>{{ g.name }}</strong></td>
        <td>{{ g.description or '—' }}</td>
        <td>{% if g.is_active %}<span class="badge badge-success">Ativo</span>{% else %}<span class="badge badge-danger">Inativo</span>{% endif %}</td>
        <td>
          <form method="post" action="/admin/groups/{{ g.id }}/delete"
                onsubmit="return confirm('Excluir grupo {{ g.name }}?')">
            <button class="btn btn-danger btn-sm" type="submit">🗑️</button>
          </form>
        </td>
      </tr>
      {% else %}
      <tr><td colspan="4" style="text-align:center;color:var(--text-muted)">Nenhum grupo.</td></tr>
      {% endfor %}
      </tbody>
    </table>
  </div>
</div>
{% endblock %}
""")

    w("src/interface/webapp/templates/groups/form.html", """\
{% extends "base.html" %}
{% block title %}Grupo{% endblock %}
{% block content %}
<div class="page-header"><h1 class="page-title">👥 Grupo</h1></div>
{% endblock %}
""")


def templates_rbac():
    w("src/interface/webapp/templates/rbac/list.html", """\
{% extends "base.html" %}
{% block title %}Atributos RBAC{% endblock %}
{% block content %}
<div class="page-header">
  <h1 class="page-title">🏷️ Atributos RBAC</h1>
</div>
<div class="card" style="margin-bottom:20px;max-width:640px">
  <h3 style="margin-bottom:14px;font-size:.95rem">➕ Novo Atributo</h3>
  <form method="post" action="/admin/rbac/new" style="display:flex;gap:10px;flex-wrap:wrap">
    <input class="form-control" name="key" placeholder="department" required style="flex:1;min-width:120px"/>
    <input class="form-control" name="label" placeholder="Departamento" required style="flex:1;min-width:120px"/>
    <select class="form-control" name="value_type" style="flex:1;min-width:100px">
      <option value="string">string</option>
      <option value="integer">integer</option>
      <option value="boolean">boolean</option>
      <option value="list">list</option>
    </select>
    <button class="btn btn-primary" type="submit">Criar</button>
  </form>
</div>
<div class="card">
  <div class="table-wrap">
    <table>
      <thead><tr><th>Key</th><th>Label</th><th>Tipo</th><th>Status</th><th>Ações</th></tr></thead>
      <tbody>
      {% for a in attributes %}
      <tr>
        <td><code>{{ a.key }}</code></td>
        <td>{{ a.label }}</td>
        <td><span class="badge badge-info">{{ a.value_type }}</span></td>
        <td>{% if a.is_active %}<span class="badge badge-success">Ativo</span>{% else %}<span class="badge badge-danger">Inativo</span>{% endif %}</td>
        <td>
          <form method="post" action="/admin/rbac/{{ a.id }}/delete"
                onsubmit="return confirm('Excluir atributo {{ a.key }}?')">
            <button class="btn btn-danger btn-sm" type="submit">🗑️</button>
          </form>
        </td>
      </tr>
      {% else %}
      <tr><td colspan="5" style="text-align:center;color:var(--text-muted)">Nenhum atributo.</td></tr>
      {% endfor %}
      </tbody>
    </table>
  </div>
</div>
{% endblock %}
""")

    w("src/interface/webapp/templates/rbac/form.html", """\
{% extends "base.html" %}
{% block title %}Atributo RBAC{% endblock %}
{% block content %}
<div class="page-header"><h1 class="page-title">🏷️ Atributo RBAC</h1></div>
{% endblock %}
""")


def templates_settings():
    w("src/interface/webapp/templates/settings/index.html", """\
{% extends "base.html" %}
{% block title %}Configurações{% endblock %}
{% block content %}
<div class="page-header">
  <h1 class="page-title">⚙️ Configurações</h1>
</div>
<div class="card" style="max-width:520px">
  <form method="post" action="/admin/settings">
    <div class="form-group">
      <label class="form-label">Expiração do Access Token (minutos)</label>
      <input class="form-control" type="number" name="access_token_expire_minutes"
             value="{{ settings.access_token_expire_minutes }}"/>
    </div>
    <div class="form-group">
      <label class="form-label">Expiração do Refresh Token (dias)</label>
      <input class="form-control" type="number" name="refresh_token_expire_days"
             value="{{ settings.refresh_token_expire_days }}"/>
    </div>
    <div class="form-group">
      <label class="form-label">Máx. tentativas de login</label>
      <input class="form-control" type="number" name="max_login_attempts"
             value="{{ settings.max_login_attempts }}"/>
    </div>
    <div class="form-group">
      <label class="form-label">Bloqueio após falhas (minutos)</label>
      <input class="form-control" type="number" name="lockout_minutes"
             value="{{ settings.lockout_minutes }}"/>
    </div>
    <button class="btn btn-primary" type="submit">💾 Salvar</button>
  </form>
</div>
{% endblock %}
""")


def templates_audit():
    w("src/interface/webapp/templates/audit/list.html", """\
{% extends "base.html" %}
{% block title %}Audit Logs{% endblock %}
{% block content %}
<div class="page-header">
  <h1 class="page-title">📋 Audit Logs</h1>
</div>
<div class="card">
  <div class="table-wrap">
    <table>
      <thead><tr><th>Data</th><th>Ator</th><th>Ação</th><th>Resource</th><th>Status</th><th>IP</th></tr></thead>
      <tbody>
      {% for l in logs %}
      <tr>
        <td style="font-size:.8rem;color:var(--text-muted)">{{ l.created_at }}</td>
        <td><strong>{{ l.actor }}</strong></td>
        <td>{{ l.action }}</td>
        <td>{{ l.resource }}</td>
        <td>
          {% if l.status == 'success' %}<span class="badge badge-success">✅ ok</span>
          {% else %}<span class="badge badge-danger">❌ falha</span>{% endif %}
        </td>
        <td style="font-size:.8rem">{{ l.ip_address or '—' }}</td>
      </tr>
      {% else %}
      <tr><td colspan="6" style="text-align:center;color:var(--text-muted)">Nenhum log.</td></tr>
      {% endfor %}
      </tbody>
    </table>
  </div>
</div>
{% endblock %}
""")


def templates_errors():
    for code, emoji, msg in [
        ("404", "🔍", "Página não encontrada"),
        ("403", "🚫", "Acesso negado"),
        ("500", "💥", "Erro interno do servidor"),
    ]:
        w(f"src/interface/webapp/templates/errors/{code}.html", f"""\
<!DOCTYPE html>
<html lang="pt-BR">
<head><meta charset="UTF-8"/><title>{code} — Apollo IAM</title>
<link rel="stylesheet" href="/static/css/main.css"/></head>
<body>
<div style="min-height:100vh;display:flex;align-items:center;justify-content:center;flex-direction:column;gap:16px">
  <div style="font-size:4rem">{emoji}</div>
  <h1 style="font-size:2rem;font-weight:700">{code}</h1>
  <p style="color:var(--text-muted)">{msg}</p>
  <a href="/admin/dashboard" class="btn btn-primary">← Voltar ao Dashboard</a>
</div>
</body>
</html>
""")


# ===========================================================================
# API main.py (completo)
# ===========================================================================

def api_main():
    w("src/interface/api/main.py", '''\
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.infrastructure.config.settings import get_settings
from src.infrastructure.database.connection import init_db, SessionLocal
from src.infrastructure.seed.seed_roles import seed_roles
from src.infrastructure.seed.seed_permissions import seed_permissions
from src.infrastructure.seed.seed_admin import seed_admin
from src.interface.api.routes.auth import router as auth_router
from src.interface.api.routes.admin.users import router as users_router
from src.interface.api.routes.admin.roles import router as roles_router
from src.interface.api.routes.admin.permissions import router as perms_router
from src.interface.api.routes.admin.groups import router as groups_router
from src.interface.api.routes.admin.rbac_attributes import router as rbac_router
from src.interface.api.routes.admin.settings import router as settings_router
from src.interface.api.routes.admin.audit_logs import router as audit_router
from src.infrastructure.logging.console_logger import success, info

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Servico centralizado de IAM + RBAC — O2 Data Solutions",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

for router in [auth_router, users_router, roles_router, perms_router,
               groups_router, rbac_router, settings_router, audit_router]:
    app.include_router(router)


@app.on_event("startup")
def startup():
    init_db()
    db = SessionLocal()
    try:
        seed_roles(db)
        seed_permissions(db)
        seed_admin(db)
    finally:
        db.close()
    success(f"Apollo IAM Engine v{settings.app_version} iniciado!")
    info("Docs: http://localhost:8000/docs")


@app.get("/health", tags=["Health"])
def health():
    return {"status": "ok", "service": settings.app_name, "version": settings.app_version}
''')


# ===========================================================================
# Webapp CSS + JS
# ===========================================================================

def webapp_assets():
    w("src/interface/webapp/static/css/variables.css", """\
:root {
  --primary: #f97316;
  --primary-dark: #ea580c;
  --gradient: linear-gradient(135deg, #f97316 0%, #ea580c 50%, #c2410c 100%);
  --bg: #0f172a;
  --bg-card: #1e293b;
  --bg-sidebar: #1e293b;
  --text: #f1f5f9;
  --text-muted: #94a3b8;
  --border: #334155;
  --success: #22c55e;
  --danger: #ef4444;
  --warning: #f59e0b;
  --info: #3b82f6;
  --radius: 10px;
  --shadow: 0 4px 24px rgba(0,0,0,0.4);
}
""")

    w("src/interface/webapp/static/css/main.css", """\
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
@import 'variables.css';
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: 'Inter', sans-serif; background: var(--bg); color: var(--text); min-height: 100vh; }
.layout { display: flex; min-height: 100vh; }
.sidebar { width: 260px; background: var(--bg-sidebar); border-right: 1px solid var(--border);
  display: flex; flex-direction: column; position: fixed; top: 0; left: 0; bottom: 0; z-index: 100; }
.sidebar-logo { padding: 24px 20px; background: var(--gradient); display: flex; align-items: center; gap: 12px; }
.sidebar-logo span { font-size: 1.1rem; font-weight: 700; color: #fff; }
.sidebar-nav { flex: 1; padding: 16px 0; overflow-y: auto; }
.nav-section { padding: 8px 20px 4px; font-size: .7rem; font-weight: 600;
  color: var(--text-muted); text-transform: uppercase; letter-spacing: .08em; }
.nav-item { display: flex; align-items: center; gap: 10px; padding: 10px 20px;
  color: var(--text-muted); text-decoration: none; font-size: .9rem; transition: all .2s;
  border-left: 3px solid transparent; }
.nav-item:hover, .nav-item.active { color: var(--primary); background: rgba(249,115,22,.08); border-left-color: var(--primary); }
.main-content { margin-left: 260px; flex: 1; display: flex; flex-direction: column; min-height: 100vh; }
.navbar { background: var(--bg-card); border-bottom: 1px solid var(--border); padding: 0 24px;
  height: 64px; display: flex; align-items: center; justify-content: space-between; position: sticky; top: 0; z-index: 50; }
.navbar-title { font-size: 1.1rem; font-weight: 600; }
.navbar-user { display: flex; align-items: center; gap: 10px; font-size: .9rem; color: var(--text-muted); }
.avatar { width: 36px; height: 36px; border-radius: 50%; background: var(--gradient);
  display: flex; align-items: center; justify-content: center; font-weight: 700; color: #fff; font-size: .85rem; }
.page { padding: 28px 32px; flex: 1; }
.page-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 24px; }
.page-title { font-size: 1.5rem; font-weight: 700; }
.card { background: var(--bg-card); border: 1px solid var(--border); border-radius: var(--radius);
  padding: 24px; box-shadow: var(--shadow); }
.stat-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px,1fr)); gap: 16px; margin-bottom: 28px; }
.stat-card { background: var(--bg-card); border: 1px solid var(--border); border-radius: var(--radius);
  padding: 20px; display: flex; align-items: center; gap: 16px; }
.stat-icon { width: 48px; height: 48px; border-radius: 12px; background: var(--gradient);
  display: flex; align-items: center; justify-content: center; font-size: 1.4rem; }
.stat-value { font-size: 1.8rem; font-weight: 700; }
.stat-label { font-size: .8rem; color: var(--text-muted); }
.table-wrap { overflow-x: auto; }
table { width: 100%; border-collapse: collapse; font-size: .9rem; }
th { text-align: left; padding: 12px 16px; background: rgba(255,255,255,.04);
  color: var(--text-muted); font-weight: 600; border-bottom: 1px solid var(--border);
  font-size: .8rem; text-transform: uppercase; letter-spacing: .05em; }
td { padding: 12px 16px; border-bottom: 1px solid var(--border); vertical-align: middle; }
tr:hover td { background: rgba(249,115,22,.04); }
.badge { display: inline-flex; align-items: center; gap: 4px; padding: 3px 10px;
  border-radius: 20px; font-size: .75rem; font-weight: 600; }
.badge-success { background: rgba(34,197,94,.15); color: var(--success); }
.badge-danger  { background: rgba(239,68,68,.15);  color: var(--danger); }
.badge-info    { background: rgba(59,130,246,.15);  color: var(--info); }
.badge-warning { background: rgba(245,158,11,.15);  color: var(--warning); }
.badge-primary { background: rgba(249,115,22,.15);  color: var(--primary); }
.btn { display: inline-flex; align-items: center; gap: 6px; padding: 8px 18px;
  border-radius: 8px; font-size: .875rem; font-weight: 500; cursor: pointer;
  border: none; transition: all .2s; text-decoration: none; }
.btn-primary { background: var(--gradient); color: #fff; }
.btn-primary:hover { opacity: .9; transform: translateY(-1px); }
.btn-outline { background: transparent; border: 1px solid var(--border); color: var(--text); }
.btn-outline:hover { border-color: var(--primary); color: var(--primary); }
.btn-danger { background: rgba(239,68,68,.15); color: var(--danger); border: 1px solid rgba(239,68,68,.3); }
.btn-danger:hover { background: var(--danger); color: #fff; }
.btn-sm { padding: 5px 12px; font-size: .8rem; }
.form-group { margin-bottom: 18px; }
.form-label { display: block; margin-bottom: 6px; font-size: .875rem; font-weight: 500; color: var(--text-muted); }
.form-control { width: 100%; padding: 10px 14px; background: rgba(255,255,255,.05);
  border: 1px solid var(--border); border-radius: 8px; color: var(--text); font-size: .9rem; transition: border-color .2s; }
.form-control:focus { outline: none; border-color: var(--primary); }
.form-control option { background: var(--bg-card); }
.login-page { min-height: 100vh; background: var(--bg); display: flex; align-items: center; justify-content: center; }
.login-card { width: 100%; max-width: 420px; background: var(--bg-card); border: 1px solid var(--border);
  border-radius: 16px; padding: 40px; box-shadow: var(--shadow); }
.login-logo { text-align: center; margin-bottom: 32px; }
.login-logo .logo-icon { width: 64px; height: 64px; border-radius: 16px; background: var(--gradient);
  display: flex; align-items: center; justify-content: center; font-size: 2rem; margin: 0 auto 12px; }
.login-logo h1 { font-size: 1.4rem; font-weight: 700; }
.login-logo p  { font-size: .85rem; color: var(--text-muted); margin-top: 4px; }
.footer { background: var(--bg-card); border-top: 1px solid var(--border); padding: 16px 32px;
  display: flex; align-items: center; justify-content: space-between; font-size: .8rem; color: var(--text-muted); }
.footer-brand { display: flex; align-items: center; gap: 6px; }
.footer-brand span { color: var(--primary); font-weight: 600; }
.alert { padding: 12px 16px; border-radius: 8px; margin-bottom: 16px;
  display: flex; align-items: center; gap: 8px; font-size: .875rem; }
.alert-error   { background: rgba(239,68,68,.1);  border: 1px solid rgba(239,68,68,.3);  color: #fca5a5; }
.alert-success { background: rgba(34,197,94,.1);  border: 1px solid rgba(34,197,94,.3);  color: #86efac; }
.alert-info    { background: rgba(59,130,246,.1); border: 1px solid rgba(59,130,246,.3); color: #93c5fd; }
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
""")

    w("src/interface/webapp/static/js/api.js", """\
const API_BASE = 'http://localhost:8000';
async function apiRequest(method, path, body = null, token = null) {
  const headers = { 'Content-Type': 'application/json' };
  if (token) headers['Authorization'] = `Bearer ${token}`;
  const opts = { method, headers };
  if (body) opts.body = JSON.stringify(body);
  const res = await fetch(API_BASE + path, opts);
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(err.detail || 'Erro na requisicao');
  }
  return res.status === 204 ? null : res.json();
}
function getToken() { return localStorage.getItem('apollo_token'); }
function setToken(t) { localStorage.setItem('apollo_token', t); }
function clearToken() { localStorage.removeItem('apollo_token'); }
""")

    w("src/interface/webapp/static/js/main.js", """\
document.addEventListener('DOMContentLoaded', () => {
  const path = window.location.pathname;
  document.querySelectorAll('.nav-item').forEach(el => {
    if (el.getAttribute('href') && path.startsWith(el.getAttribute('href'))) {
      el.classList.add('active');
    }
  });
  document.querySelectorAll('.alert[data-dismiss]').forEach(el => {
    setTimeout(() => el.remove(), 4000);
  });
  document.querySelectorAll('[data-confirm]').forEach(btn => {
    btn.addEventListener('click', e => {
      if (!confirm(btn.dataset.confirm)) e.preventDefault();
    });
  });
});
""")


# ===========================================================================
# Adiciona __main__ com relatório rico ao create_apollo_iam.py
# ===========================================================================

def patch_create_script():
    path = "create_apollo_iam.py"
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    main_block = '''

# ===========================================================================
# RELATÓRIO FINAL
# ===========================================================================

def _report(start: float):
    import os, time
    from colorama import init, Fore, Style
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel

    init(autoreset=True)
    console = Console()
    elapsed = time.time() - start

    base = "apollo-iam-engine-api-service"
    total_files = 0
    total_bytes = 0
    for root, _, files in os.walk(base):
        for f in files:
            fp = os.path.join(root, f)
            total_files += 1
            total_bytes += os.path.getsize(fp)

    table = Table(title="📁 Estrutura Criada", border_style="orange1", show_lines=True)
    table.add_column("Métrica", style="bold cyan")
    table.add_column("Valor", style="bold green")
    table.add_row("📂 Diretório base", base)
    table.add_row("📄 Total de arquivos", str(total_files))
    table.add_row("💾 Tamanho total", f"{total_bytes / 1024:.1f} KB")
    table.add_row("⏱️  Tempo de execução", f"{elapsed:.2f}s")
    console.print(table)
    console.print(Panel.fit(
        "[bold green]✅ Estrutura do projeto criada com sucesso![/bold green]\\n"
        "[dim]Próximo passo: execute [bold]python populate_apollo_iam.py[/bold][/dim]",
        border_style="green"
    ))


if __name__ == "__main__":
    import time
    _start = time.time()
    create_structure()
    _report(_start)
'''

    if "if __name__" not in content:
        with open(path, "a", encoding="utf-8") as f:
            f.write(main_block)
        return True
    return False


# ===========================================================================
# Adiciona __main__ com relatório rico ao populate_apollo_iam.py
# ===========================================================================

def patch_populate_script():
    path = "populate_apollo_iam.py"
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    main_block = '''

# ===========================================================================
# RELATÓRIO FINAL
# ===========================================================================

def _report(files_written: list, start: float):
    import time
    from colorama import init, Fore, Style
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel

    init(autoreset=True)
    console = Console()
    elapsed = time.time() - start

    total_bytes = sum(os.path.getsize(f) for f in files_written if os.path.exists(f))

    table = Table(title="🚀 Populate Concluído", border_style="orange1", show_lines=True)
    table.add_column("Métrica", style="bold cyan")
    table.add_column("Valor", style="bold green")
    table.add_row("📄 Arquivos populados", str(len(files_written)))
    table.add_row("💾 Bytes escritos", f"{total_bytes / 1024:.1f} KB")
    table.add_row("⏱️  Tempo de execução", f"{elapsed:.2f}s")
    console.print(table)

    console.print(Panel.fit(
        "[bold green]✅ Todos os arquivos foram populados![/bold green]\\n"
        "[dim]Próximo passo: execute [bold]python fix-v1.py[/bold] e depois [bold]python fix-v2.py[/bold][/dim]",
        border_style="green"
    ))


if __name__ == "__main__":
    import time
    _start = time.time()
    _written = []
    _orig_w = w

    def w_tracked(rel, content):
        path = _orig_w(rel, content)
        _written.append(path)
        return path

    # monkey-patch w globally
    import builtins
    _g = globals()
    _g["w"] = w_tracked

    root_files()
    domain_entities()
    domain_value_objects()
    domain_events()
    domain_exceptions()
    domain_ports()
    infra_config()
    infra_database()
    infra_models()
    infra_security()
    infra_repositories()
    infra_logging()
    infra_seed()
    application_dtos()
    application_use_cases()
    api_dependencies()
    api_schemas()
    api_routes()

    _report(_written, _start)
'''

    if "if __name__" not in content:
        with open(path, "a", encoding="utf-8") as f:
            f.write(main_block)
        return True
    return False


# ===========================================================================
# Adiciona __main__ com relatório rico ao fix-v1.py
# ===========================================================================

def patch_fix_v1_script():
    path = "fix-v1.py"
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    main_block = '''

# ===========================================================================
# RELATÓRIO FINAL
# ===========================================================================

def _report(files_written: list, start: float):
    import time
    from colorama import init
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel

    init(autoreset=True)
    console = Console()
    elapsed = time.time() - start
    total_bytes = sum(os.path.getsize(f) for f in files_written if os.path.exists(f))

    table = Table(title="🔧 Fix-v1 Concluído", border_style="orange1", show_lines=True)
    table.add_column("Arquivo corrigido", style="bold cyan")
    table.add_column("Tamanho", style="bold green")
    for f in files_written:
        kb = os.path.getsize(f) / 1024 if os.path.exists(f) else 0
        table.add_row(f.replace(BASE + os.sep, ""), f"{kb:.1f} KB")
    console.print(table)

    summary = Table(title="📊 Resumo", border_style="green", show_lines=True)
    summary.add_column("Métrica", style="bold cyan")
    summary.add_column("Valor", style="bold green")
    summary.add_row("🔧 Arquivos corrigidos", str(len(files_written)))
    summary.add_row("💾 Total escrito", f"{total_bytes / 1024:.1f} KB")
    summary.add_row("⏱️  Tempo", f"{elapsed:.2f}s")
    console.print(summary)

    console.print(Panel.fit(
        "[bold green]✅ Fix-v1 aplicado com sucesso![/bold green]\\n"
        "[dim]Próximo passo: execute [bold]python fix-v2.py[/bold][/dim]",
        border_style="green"
    ))


if __name__ == "__main__":
    import time
    _start = time.time()
    _written = []
    _orig_w = w

    def w_tracked(rel, content):
        path = os.path.join(BASE, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        _written.append(path)
        return path

    w.__code__ = w_tracked.__code__

    fix_password_hasher()
    fix_auth_route()
    fix_application_services()
    fix_webapp_middleware()
    fix_webapp_dependencies()
    fix_webapp_routes()
    fix_webapp_main()

    _report(_written, _start)
'''

    if "if __name__" not in content:
        with open(path, "a", encoding="utf-8") as f:
            f.write(main_block)
        return True
    return False


# ===========================================================================
# MAIN — executa tudo e exibe relatório rico
# ===========================================================================

if __name__ == "__main__":
    import time
    from colorama import init, Fore, Style
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.progress import track

    init(autoreset=True)
    console = Console()
    _start = time.time()
    _written = []

    console.print(Panel.fit(
        "[bold orange1]🔧 APOLLO IAM — fix-v2.py[/bold orange1]\n"
        "[dim]Completando templates, assets, api/main e patches nos scripts...[/dim]\n"
        "[dim]O2 Data Solutions[/dim]",
        border_style="orange1"
    ))

    # rastreia arquivos escritos
    _orig_w = w
    def _w_tracked(rel: str, content: str):
        path = _orig_w(rel, content)
        _written.append(path)
        return path

    # substitui w no escopo global
    import sys
    _mod = sys.modules[__name__]
    _mod.w = _w_tracked

    steps = [
        ("🖼️  Templates base + login + dashboard", templates_base),
        ("🧩  Partials (sidebar, navbar, footer, alerts)", templates_partials),
        ("👤  Templates de usuários", templates_users),
        ("🎭  Templates de roles", templates_roles),
        ("🔑  Templates de permissões", templates_permissions),
        ("👥  Templates de grupos", templates_groups),
        ("🏷️   Templates RBAC", templates_rbac),
        ("⚙️   Templates de configurações", templates_settings),
        ("📋  Templates de audit logs", templates_audit),
        ("❌  Templates de erros (404/403/500)", templates_errors),
        ("🚀  API main.py", api_main),
        ("🎨  Webapp CSS + JS", webapp_assets),
    ]

    for label, fn in track(steps, description="[orange1]Aplicando fixes...[/orange1]"):
        fn()
        console.print(f"  [green]✅[/green] {label}")

    # patches nos scripts
    console.print("\n[bold cyan]📝 Aplicando patches nos scripts...[/bold cyan]")

    patched = []
    if patch_create_script():
        patched.append("create_apollo_iam.py  → __main__ + relatório adicionado")
        console.print("  [green]✅[/green] create_apollo_iam.py — __main__ adicionado")
    else:
        console.print("  [yellow]⚠️[/yellow]  create_apollo_iam.py — já tinha __main__, pulado")

    if patch_populate_script():
        patched.append("populate_apollo_iam.py → __main__ + relatório adicionado")
        console.print("  [green]✅[/green] populate_apollo_iam.py — __main__ adicionado")
    else:
        console.print("  [yellow]⚠️[/yellow]  populate_apollo_iam.py — já tinha __main__, pulado")

    if patch_fix_v1_script():
        patched.append("fix-v1.py             → __main__ + relatório adicionado")
        console.print("  [green]✅[/green] fix-v1.py — __main__ adicionado")
    else:
        console.print("  [yellow]⚠️[/yellow]  fix-v1.py — já tinha __main__, pulado")

    # relatório final
    elapsed = time.time() - _start
    total_bytes = sum(os.path.getsize(f) for f in _written if os.path.exists(f))

    table = Table(title="📊 Relatório fix-v2.py", border_style="orange1", show_lines=True)
    table.add_column("Métrica", style="bold cyan", min_width=30)
    table.add_column("Valor", style="bold green")
    table.add_row("📄 Arquivos criados/atualizados", str(len(_written)))
    table.add_row("💾 Total escrito", f"{total_bytes / 1024:.1f} KB")
    table.add_row("📝 Scripts patcheados", str(len(patched)))
    table.add_row("⏱️  Tempo de execução", f"{elapsed:.2f}s")
    console.print(table)

    if patched:
        patch_table = Table(title="🔧 Scripts Atualizados", border_style="cyan", show_lines=True)
        patch_table.add_column("Script", style="bold yellow")
        for p in patched:
            patch_table.add_row(p)
        console.print(patch_table)

    console.print(Panel.fit(
        "[bold green]✅ fix-v2.py concluído![/bold green]\n\n"
        "[bold white]Ordem de execução:[/bold white]\n"
        "  [cyan]1.[/cyan] python create_apollo_iam.py\n"
        "  [cyan]2.[/cyan] python populate_apollo_iam.py\n"
        "  [cyan]3.[/cyan] python fix-v1.py\n"
        "  [cyan]4.[/cyan] python fix-v2.py  [dim](este)[/dim]\n\n"
        "[bold white]Para rodar o projeto:[/bold white]\n"
        "  [cyan]API:[/cyan]    uvicorn src.interface.api.main:app --reload --port 8000\n"
        "  [cyan]WebApp:[/cyan] uvicorn src.interface.webapp.main:app --reload --port 8080\n\n"
        "  [dim]Admin: http://localhost:8080/admin  (admin / admin)[/dim]\n"
        "  [dim]Docs:  http://localhost:8000/docs[/dim]",
        border_style="green"
    ))
