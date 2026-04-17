#!/usr/bin/env python3
"""
fix4.py
╔══════════════════════════════════════════════════════════════════════════════╗
║  APOLLO IAM ENGINE — Fix & Patch Suite v4                                  ║
║  Corrige automaticamente todos os problemas identificados:                  ║
║  1. Cria webapp/routes/policies.py (painel admin para policies)            ║
║  2. Cria templates HTML para policies no painel admin                      ║
║  3. Registra rota de policies no webapp/main.py                            ║
║  4. Reescreve project-production-test.py com 100% de cobertura             ║
║  5. Corrige benchmark-stress.py (diretório de logs garantido)              ║
║  O2 Data Solutions                                                          ║
╚══════════════════════════════════════════════════════════════════════════════╝

Uso (Windows):
    python fix4.py
"""
from __future__ import annotations

import os
import re
import sys
from pathlib import Path

try:
    from colorama import Fore, Style, init
    init(autoreset=True)
    _GREEN  = Fore.GREEN
    _RED    = Fore.RED
    _CYAN   = Fore.CYAN
    _YELLOW = Fore.YELLOW
    _RESET  = Style.RESET_ALL
except ImportError:
    _GREEN = _RED = _CYAN = _YELLOW = _RESET = ""

_HERE = Path(__file__).parent.resolve()
_ERRORS: list[str] = []


def ok(msg: str):
    print(f"  {_GREEN}OK{_RESET}  {msg}")


def fail(msg: str):
    _ERRORS.append(msg)
    print(f"  {_RED}FAIL{_RESET}  {msg}")


def info(msg: str):
    print(f"  {_CYAN}..{_RESET}  {msg}")


def hdr(title: str):
    print(f"\n{_CYAN}{'='*72}{_RESET}")
    print(f"{_CYAN}  {title}{_RESET}")
    print(f"{_CYAN}{'='*72}{_RESET}")


def write_file(path: Path, content: str):
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        ok(f"Escrito: {path.relative_to(_HERE)}")
    except Exception as e:
        fail(f"Erro ao escrever {path}: {e}")


def patch_file(path: Path, old: str, new: str, label: str = ""):
    try:
        text = path.read_text(encoding="utf-8")
        if old not in text:
            info(f"Patch '{label}' já aplicado ou não encontrado em {path.name}")
            return
        path.write_text(text.replace(old, new, 1), encoding="utf-8")
        ok(f"Patch '{label}' aplicado em {path.name}")
    except Exception as e:
        fail(f"Erro ao patchear {path}: {e}")


# ══════════════════════════════════════════════════════════════════════════════
# FIX 1 — webapp/routes/policies.py
# ══════════════════════════════════════════════════════════════════════════════

def fix_webapp_policies_route():
    hdr("FIX 1 — Criar webapp/routes/policies.py")
    content = (
        '"""policies.py — Webapp admin routes para policies DSL. fix4.py"""\n'
        "from __future__ import annotations\n"
        "import json as _json\n"
        "from typing import Optional\n"
        "from fastapi import APIRouter, Request, Form\n"
        "from fastapi.responses import HTMLResponse, RedirectResponse\n"
        "from src.interface.webapp._templates import templates as T\n"
        "from src.interface.webapp.api_client import api_client, auth_headers\n\n"
        "router = APIRouter()\n\n"
        "def _h(r: Request) -> dict:\n"
        "    return auth_headers(r.session['user']['token'])\n\n"
        "@router.get('/admin/policies', response_class=HTMLResponse)\n"
        "async def list_policies(request: Request, tenant_id: Optional[str] = None):\n"
        "    async with api_client() as c:\n"
        "        h = _h(request)\n"
        "        params = {'tenant_id': tenant_id} if tenant_id else {}\n"
        "        r = await c.get('/admin/policies/', headers=h, params=params)\n"
        "        policies = r.json() if r.status_code == 200 else []\n"
        "        cr = await c.get('/admin/policies/cache/stats', headers=h)\n"
        "        cache_stats = cr.json() if cr.status_code == 200 else {}\n"
        "    return T.TemplateResponse('policies/list.html', {\n"
        "        'request': request, 'policies': policies or [],\n"
        "        'cache_stats': cache_stats, 'tenant_id': tenant_id or '',\n"
        "        'msg': request.query_params.get('msg', ''),\n"
        "        'error': request.query_params.get('error', ''),\n"
        "    })\n\n"
        "@router.post('/admin/policies/new')\n"
        "async def create_policy(\n"
        "    request: Request, name: str = Form(...), description: str = Form(''),\n"
        "    effect: str = Form('allow'), priority: int = Form(100),\n"
        "    actions: str = Form('*'), resources: str = Form('*'),\n"
        "    tenant_id: Optional[str] = Form(None), enabled: Optional[str] = Form(None),\n"
        "):\n"
        "    payload = {\n"
        "        'name': name, 'description': description, 'effect': effect,\n"
        "        'priority': priority,\n"
        "        'actions': [a.strip() for a in actions.split(',') if a.strip()] or ['*'],\n"
        "        'resources': [r.strip() for r in resources.split(',') if r.strip()] or ['*'],\n"
        "        'conditions': [], 'tenant_id': tenant_id or None,\n"
        "        'enabled': enabled == 'on',\n"
        "    }\n"
        "    async with api_client() as c:\n"
        "        r = await c.post('/admin/policies/', json=payload, headers=_h(request))\n"
        "    if r.status_code in (200, 201):\n"
        "        async with api_client() as c:\n"
        "            await c.post('/admin/policies/reload', headers=_h(request))\n"
        "        return RedirectResponse(url='/admin/policies?msg=Policy+criada', status_code=302)\n"
        "    detail = r.json().get('detail', 'Erro') if r.content else 'Erro'\n"
        "    return RedirectResponse(url=f'/admin/policies?error={detail}', status_code=302)\n\n"
        "@router.post('/admin/policies/{policy_id}/toggle')\n"
        "async def toggle_policy(policy_id: str, request: Request, enabled: str = Form('true')):\n"
        "    enabled_bool = enabled.lower() in ('true', 'on', '1', 'yes')\n"
        "    async with api_client() as c:\n"
        "        await c.patch(f'/admin/policies/{policy_id}/toggle',\n"
        "                      headers=_h(request), params={'enabled': str(enabled_bool).lower()})\n"
        "    return RedirectResponse(url='/admin/policies?msg=Policy+atualizada', status_code=302)\n\n"
        "@router.post('/admin/policies/{policy_id}/delete')\n"
        "async def delete_policy(policy_id: str, request: Request):\n"
        "    async with api_client() as c:\n"
        "        await c.delete(f'/admin/policies/{policy_id}', headers=_h(request))\n"
        "    return RedirectResponse(url='/admin/policies?msg=Policy+removida', status_code=302)\n\n"
        "@router.post('/admin/policies/reload')\n"
        "async def reload_policies(request: Request):\n"
        "    async with api_client() as c:\n"
        "        r = await c.post('/admin/policies/reload', headers=_h(request))\n"
        "    loaded = r.json().get('loaded', 0) if r.status_code == 200 else 0\n"
        "    return RedirectResponse(\n"
        "        url=f'/admin/policies?msg=Engine+recarregado+({loaded}+policies)', status_code=302)\n\n"
        "@router.get('/admin/policies/{policy_id}', response_class=HTMLResponse)\n"
        "async def policy_detail(policy_id: str, request: Request):\n"
        "    async with api_client() as c:\n"
        "        r = await c.get(f'/admin/policies/{policy_id}', headers=_h(request))\n"
        "    if r.status_code != 200:\n"
        "        return RedirectResponse(url='/admin/policies?error=Policy+nao+encontrada', status_code=302)\n"
        "    return T.TemplateResponse('policies/detail.html', {\n"
        "        'request': request, 'policy': r.json(),\n"
        "        'msg': request.query_params.get('msg', ''),\n"
        "    })\n\n"
        "@router.get('/admin/policies-evaluate', response_class=HTMLResponse)\n"
        "async def evaluate_page(request: Request):\n"
        "    return T.TemplateResponse('policies/evaluate.html',\n"
        "                              {'request': request, 'result': None, 'payload': None})\n\n"
        "@router.post('/admin/policies-evaluate', response_class=HTMLResponse)\n"
        "async def evaluate_policy(\n"
        "    request: Request, subject_json: str = Form('{}'),\n"
        "    action: str = Form(...), resource: str = Form(...),\n"
        "    tenant_id: Optional[str] = Form(None), subject_id: str = Form(''),\n"
        "    use_cache: Optional[str] = Form(None),\n"
        "):\n"
        "    try:\n"
        "        subject = _json.loads(subject_json)\n"
        "    except Exception:\n"
        "        subject = {}\n"
        "    payload = {'subject': subject, 'action': action, 'resource': resource,\n"
        "               'tenant_id': tenant_id or None, 'subject_id': subject_id,\n"
        "               'use_cache': use_cache == 'on'}\n"
        "    async with api_client() as c:\n"
        "        r = await c.post('/admin/policies/evaluate', json=payload, headers=_h(request))\n"
        "    result = r.json() if r.status_code == 200 else {'error': r.text}\n"
        "    return T.TemplateResponse('policies/evaluate.html',\n"
        "                              {'request': request, 'result': result, 'payload': payload})\n\n"
        "@router.get('/admin/policies-audit', response_class=HTMLResponse)\n"
        "async def audit_page(\n"
        "    request: Request, tenant_id: Optional[str] = None,\n"
        "    subject_id: Optional[str] = None, decision: Optional[str] = None, limit: int = 50,\n"
        "):\n"
        "    params = {'limit': limit}\n"
        "    if tenant_id: params['tenant_id'] = tenant_id\n"
        "    if subject_id: params['subject_id'] = subject_id\n"
        "    if decision: params['decision'] = decision\n"
        "    async with api_client() as c:\n"
        "        r = await c.get('/admin/policies/audit', headers=_h(request), params=params)\n"
        "    decisions = r.json() if r.status_code == 200 else []\n"
        "    return T.TemplateResponse('policies/audit.html', {\n"
        "        'request': request, 'decisions': decisions or [],\n"
        "        'tenant_id': tenant_id or '', 'subject_id': subject_id or '',\n"
        "        'decision': decision or '', 'limit': limit,\n"
        "    })\n"
    )
    dest = _HERE / "src" / "interface" / "webapp" / "routes" / "policies.py"
    write_file(dest, content)


# ══════════════════════════════════════════════════════════════════════════════
# FIX 2 — Templates HTML para policies
# ══════════════════════════════════════════════════════════════════════════════

def fix_policies_templates():
    hdr("FIX 2 — Criar templates HTML para policies")
    base = _HERE / "src" / "interface" / "webapp" / "templates" / "policies"

    list_html = """\
{% extends "base.html" %}
{% block title %}Policies DSL{% endblock %}
{% block content %}
<div class="d-flex justify-content-between align-items-center mb-3">
  <h2>Policies DSL</h2>
  <div>
    <a href="/admin/policies-evaluate" class="btn btn-outline-primary btn-sm me-1">Avaliar</a>
    <a href="/admin/policies-audit" class="btn btn-outline-secondary btn-sm me-1">Audit Trail</a>
    <form method="post" action="/admin/policies/reload" class="d-inline">
      <button class="btn btn-outline-warning btn-sm me-1">Reload Engine</button>
    </form>
    <button class="btn btn-primary btn-sm" data-bs-toggle="modal" data-bs-target="#newPolicyModal">+ Nova Policy</button>
  </div>
</div>
{% if msg %}<div class="alert alert-success">{{ msg }}</div>{% endif %}
{% if error %}<div class="alert alert-danger">{{ error }}</div>{% endif %}
{% if cache_stats %}
<div class="alert alert-info py-1 small">
  Cache: hits={{ cache_stats.hits }} misses={{ cache_stats.misses }}
  hit_rate={{ "%.1f"|format((cache_stats.hit_rate or 0) * 100) }}% size={{ cache_stats.size }}
</div>
{% endif %}
<form method="get" class="row g-2 mb-3">
  <div class="col-auto">
    <input type="text" name="tenant_id" class="form-control form-control-sm"
           placeholder="Filtrar por tenant_id" value="{{ tenant_id }}">
  </div>
  <div class="col-auto"><button class="btn btn-sm btn-outline-secondary">Filtrar</button></div>
</form>
<table class="table table-sm table-hover">
  <thead><tr><th>Nome</th><th>Efeito</th><th>Prioridade</th><th>Tenant</th><th>Scope</th><th>Ativo</th><th>Acoes</th></tr></thead>
  <tbody>
  {% for p in policies %}
  <tr>
    <td><a href="/admin/policies/{{ p.id }}">{{ p.name }}</a></td>
    <td>{% if p.effect == "allow" %}<span class="badge bg-success">allow</span>{% else %}<span class="badge bg-danger">deny</span>{% endif %}</td>
    <td>{{ p.priority }}</td>
    <td><small>{{ p.tenant_id or "global" }}</small></td>
    <td><small>{{ p.scope or "tenant" }}</small></td>
    <td>{% if p.enabled %}<span class="badge bg-success">sim</span>{% else %}<span class="badge bg-secondary">nao</span>{% endif %}</td>
    <td>
      <form method="post" action="/admin/policies/{{ p.id }}/toggle" class="d-inline">
        <input type="hidden" name="enabled" value="{{ 'false' if p.enabled else 'true' }}">
        <button class="btn btn-sm btn-outline-warning py-0">{{ "Desativar" if p.enabled else "Ativar" }}</button>
      </form>
      <form method="post" action="/admin/policies/{{ p.id }}/delete" class="d-inline" onsubmit="return confirm('Remover?')">
        <button class="btn btn-sm btn-outline-danger py-0">Remover</button>
      </form>
    </td>
  </tr>
  {% else %}
  <tr><td colspan="7" class="text-center text-muted">Nenhuma policy cadastrada.</td></tr>
  {% endfor %}
  </tbody>
</table>
<div class="modal fade" id="newPolicyModal" tabindex="-1">
  <div class="modal-dialog modal-lg">
    <div class="modal-content">
      <div class="modal-header"><h5 class="modal-title">Nova Policy</h5>
        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
      </div>
      <form method="post" action="/admin/policies/new">
        <div class="modal-body">
          <div class="row g-2">
            <div class="col-8"><label class="form-label">Nome *</label>
              <input type="text" name="name" class="form-control" required></div>
            <div class="col-4"><label class="form-label">Efeito</label>
              <select name="effect" class="form-select">
                <option value="allow">allow</option><option value="deny">deny</option>
              </select></div>
            <div class="col-6"><label class="form-label">Actions (virgula)</label>
              <input type="text" name="actions" class="form-control" value="*"></div>
            <div class="col-6"><label class="form-label">Resources (virgula)</label>
              <input type="text" name="resources" class="form-control" value="*"></div>
            <div class="col-4"><label class="form-label">Prioridade</label>
              <input type="number" name="priority" class="form-control" value="100"></div>
            <div class="col-4"><label class="form-label">Tenant ID</label>
              <input type="text" name="tenant_id" class="form-control" placeholder="(global)"></div>
            <div class="col-4 d-flex align-items-end">
              <div class="form-check">
                <input class="form-check-input" type="checkbox" name="enabled" value="on" checked>
                <label class="form-check-label">Ativo</label>
              </div>
            </div>
            <div class="col-12"><label class="form-label">Descricao</label>
              <input type="text" name="description" class="form-control"></div>
          </div>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
          <button type="submit" class="btn btn-primary">Criar Policy</button>
        </div>
      </form>
    </div>
  </div>
</div>
{% endblock %}
"""

    detail_html = """\
{% extends "base.html" %}
{% block title %}Policy: {{ policy.name }}{% endblock %}
{% block content %}
<div class="d-flex justify-content-between align-items-center mb-3">
  <h2>{{ policy.name }}</h2>
  <a href="/admin/policies" class="btn btn-outline-secondary btn-sm">Voltar</a>
</div>
{% if msg %}<div class="alert alert-success">{{ msg }}</div>{% endif %}
<div class="card mb-3"><div class="card-body">
  <dl class="row mb-0">
    <dt class="col-3">ID</dt><dd class="col-9"><code>{{ policy.id }}</code></dd>
    <dt class="col-3">Efeito</dt>
    <dd class="col-9">{% if policy.effect == "allow" %}<span class="badge bg-success">allow</span>{% else %}<span class="badge bg-danger">deny</span>{% endif %}</dd>
    <dt class="col-3">Prioridade</dt><dd class="col-9">{{ policy.priority }}</dd>
    <dt class="col-3">Tenant</dt><dd class="col-9">{{ policy.tenant_id or "global" }}</dd>
    <dt class="col-3">Scope</dt><dd class="col-9">{{ policy.scope or "tenant" }}</dd>
    <dt class="col-3">Versao</dt><dd class="col-9">{{ policy.version }}</dd>
    <dt class="col-3">Ativo</dt>
    <dd class="col-9">{% if policy.enabled %}<span class="badge bg-success">Sim</span>{% else %}<span class="badge bg-secondary">Nao</span>{% endif %}</dd>
    <dt class="col-3">Descricao</dt><dd class="col-9">{{ policy.description or "nenhuma" }}</dd>
    <dt class="col-3">Actions</dt><dd class="col-9"><code>{{ policy.actions | join(", ") }}</code></dd>
    <dt class="col-3">Resources</dt><dd class="col-9"><code>{{ policy.resources | join(", ") }}</code></dd>
    <dt class="col-3">Logic</dt><dd class="col-9">{{ policy.condition_logic }}</dd>
  </dl>
</div></div>
{% if policy.conditions %}
<h5>Condicoes</h5>
<table class="table table-sm"><thead><tr><th>Field</th><th>Op</th><th>Value</th></tr></thead>
<tbody>{% for c in policy.conditions %}
<tr><td><code>{{ c.field }}</code></td><td>{{ c.op }}</td><td><code>{{ c.value }}</code></td></tr>
{% endfor %}</tbody></table>
{% endif %}
{% if policy.inherits %}
<h5>Herda de</h5>
<ul>{% for pid in policy.inherits %}<li><code>{{ pid }}</code></li>{% endfor %}</ul>
{% endif %}
<div class="mt-3">
  <form method="post" action="/admin/policies/{{ policy.id }}/toggle" class="d-inline">
    <input type="hidden" name="enabled" value="{{ 'false' if policy.enabled else 'true' }}">
    <button class="btn btn-warning btn-sm">{{ "Desativar" if policy.enabled else "Ativar" }}</button>
  </form>
  <form method="post" action="/admin/policies/{{ policy.id }}/delete" class="d-inline ms-2"
        onsubmit="return confirm('Remover esta policy?')">
    <button class="btn btn-danger btn-sm">Remover</button>
  </form>
</div>
{% endblock %}
"""

    evaluate_html = """\
{% extends "base.html" %}
{% block title %}Avaliar Policy{% endblock %}
{% block content %}
<h2>Avaliar Policy</h2>
<div class="row">
  <div class="col-md-6">
    <form method="post" action="/admin/policies-evaluate">
      <div class="mb-2">
        <label class="form-label">Subject (JSON)</label>
        <textarea name="subject_json" class="form-control font-monospace" rows="5"
          placeholder='{"department":"sales","roles":["vendedor"],"user_level":3}'>{{ payload.subject | tojson if payload else "" }}</textarea>
      </div>
      <div class="row g-2 mb-2">
        <div class="col-6"><label class="form-label">Action</label>
          <input type="text" name="action" class="form-control"
                 value="{{ payload.action if payload else '' }}" placeholder="cotacao:create"></div>
        <div class="col-6"><label class="form-label">Resource</label>
          <input type="text" name="resource" class="form-control"
                 value="{{ payload.resource if payload else '' }}" placeholder="cotacao/123"></div>
        <div class="col-6"><label class="form-label">Tenant ID</label>
          <input type="text" name="tenant_id" class="form-control"
                 value="{{ payload.tenant_id if payload else '' }}"></div>
        <div class="col-6"><label class="form-label">Subject ID</label>
          <input type="text" name="subject_id" class="form-control"
                 value="{{ payload.subject_id if payload else '' }}"></div>
        <div class="col-12">
          <div class="form-check">
            <input class="form-check-input" type="checkbox" name="use_cache" value="on">
            <label class="form-check-label">Usar cache</label>
          </div>
        </div>
      </div>
      <button type="submit" class="btn btn-primary">Avaliar</button>
      <a href="/admin/policies" class="btn btn-outline-secondary ms-2">Policies</a>
    </form>
  </div>
  <div class="col-md-6">
    {% if result %}
    <div class="card {% if result.allowed is defined and result.allowed %}border-success{% else %}border-danger{% endif %}">
      <div class="card-header">
        {% if result.error is defined %}<span class="text-danger">Erro</span>
        {% elif result.allowed %}<span class="text-success">PERMITIDO</span>
        {% else %}<span class="text-danger">NEGADO</span>{% endif %}
      </div>
      <div class="card-body">
        {% if result.error is defined %}<pre class="text-danger">{{ result.error }}</pre>
        {% else %}
        <dl class="row mb-0 small">
          <dt class="col-4">Decision</dt><dd class="col-8"><code>{{ result.decision }}</code></dd>
          <dt class="col-4">Reason</dt><dd class="col-8">{{ result.reason }}</dd>
          <dt class="col-4">Policy</dt><dd class="col-8"><code>{{ result.matched_policy or "nenhuma" }}</code></dd>
          {% if result.failing_condition %}
          <dt class="col-4">Failing</dt><dd class="col-8 text-danger">{{ result.failing_condition }}</dd>
          {% endif %}
        </dl>
        {% endif %}
      </div>
    </div>
    {% endif %}
  </div>
</div>
{% endblock %}
"""

    audit_html = """\
{% extends "base.html" %}
{% block title %}Audit Trail Decisoes{% endblock %}
{% block content %}
<div class="d-flex justify-content-between align-items-center mb-3">
  <h2>Audit Trail - Decisoes de Policy</h2>
  <a href="/admin/policies" class="btn btn-outline-secondary btn-sm">Policies</a>
</div>
<form method="get" class="row g-2 mb-3">
  <div class="col-auto">
    <input type="text" name="tenant_id" class="form-control form-control-sm"
           placeholder="tenant_id" value="{{ tenant_id }}">
  </div>
  <div class="col-auto">
    <input type="text" name="subject_id" class="form-control form-control-sm"
           placeholder="subject_id" value="{{ subject_id }}">
  </div>
  <div class="col-auto">
    <select name="decision" class="form-select form-select-sm">
      <option value="">Todas</option>
      <option value="allow" {% if decision == "allow" %}selected{% endif %}>allow</option>
      <option value="deny" {% if decision == "deny" %}selected{% endif %}>deny</option>
      <option value="no_match" {% if decision == "no_match" %}selected{% endif %}>no_match</option>
    </select>
  </div>
  <div class="col-auto">
    <input type="number" name="limit" class="form-control form-control-sm"
           value="{{ limit }}" style="width:80px">
  </div>
  <div class="col-auto"><button class="btn btn-sm btn-outline-secondary">Filtrar</button></div>
</form>
<table class="table table-sm table-hover small">
  <thead><tr><th>Timestamp</th><th>Decision</th><th>Action</th><th>Resource</th>
    <th>Subject</th><th>Tenant</th><th>Policy</th><th>Reason</th></tr></thead>
  <tbody>
  {% for d in decisions %}
  <tr>
    <td><small>{{ d.timestamp[:19] }}</small></td>
    <td>{% if d.decision == "allow" %}<span class="badge bg-success">allow</span>
        {% elif d.decision == "deny" %}<span class="badge bg-danger">deny</span>
        {% else %}<span class="badge bg-secondary">no_match</span>{% endif %}</td>
    <td><code>{{ d.action }}</code></td>
    <td><small>{{ d.resource[:40] }}</small></td>
    <td><small>{{ (d.subject_id or "")[:20] }}</small></td>
    <td><small>{{ d.tenant_id or "global" }}</small></td>
    <td><small>{{ (d.matched_policy or "")[:16] }}</small></td>
    <td><small>{{ (d.reason or "")[:60] }}</small></td>
  </tr>
  {% else %}
  <tr><td colspan="8" class="text-center text-muted">Nenhuma decisao registrada.</td></tr>
  {% endfor %}
  </tbody>
</table>
{% endblock %}
"""

    write_file(base / "list.html", list_html)
    write_file(base / "detail.html", detail_html)
    write_file(base / "evaluate.html", evaluate_html)
    write_file(base / "audit.html", audit_html)



# ══════════════════════════════════════════════════════════════════════════════
# FIX 3 — Registrar rota de policies no webapp/main.py
# ══════════════════════════════════════════════════════════════════════════════

def fix_webapp_main():
    hdr("FIX 3 — Registrar policies no webapp/main.py")
    main_path = _HERE / "src" / "interface" / "webapp" / "main.py"
    if not main_path.exists():
        fail(f"webapp/main.py nao encontrado: {main_path}")
        return

    text = main_path.read_text(encoding="utf-8")

    # Adicionar import se nao existir
    import_line = "from src.interface.webapp.routes import user_types, user_levels, custom_entities, metrics"
    new_import   = (
        "from src.interface.webapp.routes import user_types, user_levels, custom_entities, metrics\n"
        "from src.interface.webapp.routes import policies as policies_route"
    )
    if "policies_route" not in text:
        text = text.replace(import_line, new_import)
        ok("Import de policies_route adicionado ao webapp/main.py")
    else:
        info("Import de policies_route ja existe no webapp/main.py")

    # Adicionar router no loop de inclusao
    old_routers = (
        "    user_types.router, user_levels.router, custom_entities.router, metrics.router,"
    )
    new_routers = (
        "    user_types.router, user_levels.router, custom_entities.router, metrics.router,\n"
        "    policies_route.router,"
    )
    if "policies_route.router" not in text:
        text = text.replace(old_routers, new_routers)
        ok("Router de policies_route adicionado ao webapp/main.py")
    else:
        info("Router de policies_route ja registrado no webapp/main.py")

    main_path.write_text(text, encoding="utf-8")
    ok("webapp/main.py atualizado")


# ══════════════════════════════════════════════════════════════════════════════
# FIX 4 — Adicionar link de Policies na sidebar do painel admin
# ══════════════════════════════════════════════════════════════════════════════

def fix_sidebar():
    hdr("FIX 4 — Adicionar Policies na sidebar")
    sidebar = _HERE / "src" / "interface" / "webapp" / "templates" / "partials" / "sidebar.html"
    if not sidebar.exists():
        info("sidebar.html nao encontrado, pulando")
        return

    text = sidebar.read_text(encoding="utf-8")
    if "/admin/policies" in text:
        info("Link de policies ja existe na sidebar")
        return

    # Insere antes do fechamento do nav ou antes de metrics/audit
    anchors = [
        ("/admin/metrics", "metrics"),
        ("/admin/audit",   "audit"),
        ("</ul>",          "fim da lista"),
        ("</nav>",         "fim do nav"),
    ]
    for anchor, label in anchors:
        if anchor in text:
            policies_link = (
                '\n    <li class="nav-item">'
                '\n      <a class="nav-link" href="/admin/policies">Policies DSL</a>'
                "\n    </li>"
            )
            text = text.replace(anchor, policies_link + "\n    " + anchor, 1)
            text_out = text
            sidebar.write_text(text_out, encoding="utf-8")
            ok(f"Link de Policies adicionado na sidebar (antes de '{label}')")
            return

    info("Nao foi possivel inserir link na sidebar automaticamente")



# ══════════════════════════════════════════════════════════════════════════════
# FIX 5 — Reescrever project-production-test.py com 100% de cobertura
# ══════════════════════════════════════════════════════════════════════════════

def fix_production_test():
    hdr("FIX 5 — Reescrever project-production-test.py")
    dest = _HERE / "project-production-test.py"
    write_file(dest, _PRODUCTION_TEST_CONTENT)


# ══════════════════════════════════════════════════════════════════════════════
# FIX 6 — Corrigir benchmark-stress.py
# ══════════════════════════════════════════════════════════════════════════════

def fix_benchmark_stress():
    hdr("FIX 6 — Corrigir benchmark-stress.py")
    dest = _HERE / "benchmark-stress.py"
    if not dest.exists():
        info("benchmark-stress.py nao encontrado, pulando")
        return
    text = dest.read_text(encoding="utf-8")
    # Garante que o diretorio de logs existe
    old = 'LOGS_DIR = os.path.join(_HERE, "benchmark-stress-logs")\nRUN_ID   = datetime.now().strftime("%Y%m%d_%H%M%S")\nos.makedirs(LOGS_DIR, exist_ok=True)'
    new = 'LOGS_DIR = os.path.join(_HERE, "benchmark-stress-logs")\nRUN_ID   = datetime.now().strftime("%Y%m%d_%H%M%S")\nos.makedirs(LOGS_DIR, exist_ok=True)\nos.makedirs(os.path.join(_HERE, "project-test-run-setup-logs"), exist_ok=True)'
    if "project-test-run-setup-logs" not in text:
        text = text.replace(old, new)
        dest.write_text(text, encoding="utf-8")
        ok("benchmark-stress.py: diretorio de logs garantido")
    else:
        info("benchmark-stress.py: diretorio de logs ja garantido")


