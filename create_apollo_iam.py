"""
APOLLO-IAM-ENGINE-API-SERVICE
Script de criação da estrutura completa do projeto.
Criado por O2 Data Solutions
"""

import os

BASE = "apollo-iam-engine-api-service"

STRUCTURE = {
    # ── raiz ──────────────────────────────────────────────────────────────────
    ".env.example": "",
    ".gitignore": "",
    "README.md": "",
    "pyproject.toml": "",
    "requirements.txt": "",
    "docker-compose.yml": "",
    "Dockerfile": "",
    "alembic.ini": "",

    # ── domínio ───────────────────────────────────────────────────────────────
    "src/__init__.py": "",
    "src/domain/__init__.py": "",

    # entidades
    "src/domain/entities/__init__.py": "",
    "src/domain/entities/user.py": "",
    "src/domain/entities/role.py": "",
    "src/domain/entities/permission.py": "",
    "src/domain/entities/group.py": "",
    "src/domain/entities/user_type.py": "",
    "src/domain/entities/user_level.py": "",
    "src/domain/entities/token.py": "",
    "src/domain/entities/audit_log.py": "",
    "src/domain/entities/rbac_attribute.py": "",

    # value objects
    "src/domain/value_objects/__init__.py": "",
    "src/domain/value_objects/username.py": "",
    "src/domain/value_objects/password.py": "",
    "src/domain/value_objects/email.py": "",
    "src/domain/value_objects/token_payload.py": "",

    # eventos de domínio
    "src/domain/events/__init__.py": "",
    "src/domain/events/user_created.py": "",
    "src/domain/events/user_updated.py": "",
    "src/domain/events/user_deleted.py": "",
    "src/domain/events/login_succeeded.py": "",
    "src/domain/events/login_failed.py": "",

    # exceções de domínio
    "src/domain/exceptions/__init__.py": "",
    "src/domain/exceptions/auth_exceptions.py": "",
    "src/domain/exceptions/user_exceptions.py": "",
    "src/domain/exceptions/rbac_exceptions.py": "",

    # portas (interfaces / contratos)
    "src/domain/ports/__init__.py": "",
    "src/domain/ports/user_repository.py": "",
    "src/domain/ports/role_repository.py": "",
    "src/domain/ports/permission_repository.py": "",
    "src/domain/ports/group_repository.py": "",
    "src/domain/ports/token_service.py": "",
    "src/domain/ports/password_hasher.py": "",
    "src/domain/ports/audit_logger.py": "",
    "src/domain/ports/rbac_attribute_repository.py": "",

    # ── aplicação ─────────────────────────────────────────────────────────────
    "src/application/__init__.py": "",

    # casos de uso – auth
    "src/application/use_cases/__init__.py": "",
    "src/application/use_cases/auth/__init__.py": "",
    "src/application/use_cases/auth/login.py": "",
    "src/application/use_cases/auth/refresh_token.py": "",
    "src/application/use_cases/auth/logout.py": "",
    "src/application/use_cases/auth/validate_token.py": "",

    # casos de uso – usuários
    "src/application/use_cases/users/__init__.py": "",
    "src/application/use_cases/users/create_user.py": "",
    "src/application/use_cases/users/update_user.py": "",
    "src/application/use_cases/users/delete_user.py": "",
    "src/application/use_cases/users/get_user.py": "",
    "src/application/use_cases/users/list_users.py": "",
    "src/application/use_cases/users/change_password.py": "",
    "src/application/use_cases/users/reset_password.py": "",
    "src/application/use_cases/users/toggle_user_status.py": "",

    # casos de uso – roles
    "src/application/use_cases/roles/__init__.py": "",
    "src/application/use_cases/roles/create_role.py": "",
    "src/application/use_cases/roles/update_role.py": "",
    "src/application/use_cases/roles/delete_role.py": "",
    "src/application/use_cases/roles/list_roles.py": "",
    "src/application/use_cases/roles/assign_role_to_user.py": "",
    "src/application/use_cases/roles/revoke_role_from_user.py": "",

    # casos de uso – permissões
    "src/application/use_cases/permissions/__init__.py": "",
    "src/application/use_cases/permissions/create_permission.py": "",
    "src/application/use_cases/permissions/update_permission.py": "",
    "src/application/use_cases/permissions/delete_permission.py": "",
    "src/application/use_cases/permissions/list_permissions.py": "",
    "src/application/use_cases/permissions/assign_permission_to_role.py": "",

    # casos de uso – grupos
    "src/application/use_cases/groups/__init__.py": "",
    "src/application/use_cases/groups/create_group.py": "",
    "src/application/use_cases/groups/update_group.py": "",
    "src/application/use_cases/groups/delete_group.py": "",
    "src/application/use_cases/groups/list_groups.py": "",
    "src/application/use_cases/groups/assign_user_to_group.py": "",

    # casos de uso – atributos RBAC dinâmicos
    "src/application/use_cases/rbac/__init__.py": "",
    "src/application/use_cases/rbac/create_attribute.py": "",
    "src/application/use_cases/rbac/update_attribute.py": "",
    "src/application/use_cases/rbac/delete_attribute.py": "",
    "src/application/use_cases/rbac/list_attributes.py": "",
    "src/application/use_cases/rbac/assign_attribute_to_user.py": "",

    # casos de uso – configurações
    "src/application/use_cases/settings/__init__.py": "",
    "src/application/use_cases/settings/get_settings.py": "",
    "src/application/use_cases/settings/update_settings.py": "",

    # DTOs
    "src/application/dtos/__init__.py": "",
    "src/application/dtos/auth_dto.py": "",
    "src/application/dtos/user_dto.py": "",
    "src/application/dtos/role_dto.py": "",
    "src/application/dtos/permission_dto.py": "",
    "src/application/dtos/group_dto.py": "",
    "src/application/dtos/rbac_dto.py": "",
    "src/application/dtos/settings_dto.py": "",
    "src/application/dtos/audit_dto.py": "",

    # serviços de aplicação
    "src/application/services/__init__.py": "",
    "src/application/services/auth_service.py": "",
    "src/application/services/user_service.py": "",
    "src/application/services/rbac_service.py": "",
    "src/application/services/settings_service.py": "",
    "src/application/services/audit_service.py": "",

    # ── infraestrutura ────────────────────────────────────────────────────────
    "src/infrastructure/__init__.py": "",

    # banco de dados
    "src/infrastructure/database/__init__.py": "",
    "src/infrastructure/database/connection.py": "",
    "src/infrastructure/database/base.py": "",
    "src/infrastructure/database/migrations/__init__.py": "",
    "src/infrastructure/database/migrations/env.py": "",

    # modelos ORM
    "src/infrastructure/database/models/__init__.py": "",
    "src/infrastructure/database/models/user_model.py": "",
    "src/infrastructure/database/models/role_model.py": "",
    "src/infrastructure/database/models/permission_model.py": "",
    "src/infrastructure/database/models/group_model.py": "",
    "src/infrastructure/database/models/user_type_model.py": "",
    "src/infrastructure/database/models/user_level_model.py": "",
    "src/infrastructure/database/models/rbac_attribute_model.py": "",
    "src/infrastructure/database/models/settings_model.py": "",
    "src/infrastructure/database/models/audit_log_model.py": "",
    "src/infrastructure/database/models/token_blacklist_model.py": "",

    # repositórios concretos
    "src/infrastructure/repositories/__init__.py": "",
    "src/infrastructure/repositories/user_repository_impl.py": "",
    "src/infrastructure/repositories/role_repository_impl.py": "",
    "src/infrastructure/repositories/permission_repository_impl.py": "",
    "src/infrastructure/repositories/group_repository_impl.py": "",
    "src/infrastructure/repositories/rbac_attribute_repository_impl.py": "",
    "src/infrastructure/repositories/audit_log_repository_impl.py": "",

    # adaptadores de segurança
    "src/infrastructure/security/__init__.py": "",
    "src/infrastructure/security/jwt_service.py": "",
    "src/infrastructure/security/password_hasher_impl.py": "",
    "src/infrastructure/security/token_blacklist.py": "",

    # logging
    "src/infrastructure/logging/__init__.py": "",
    "src/infrastructure/logging/console_logger.py": "",
    "src/infrastructure/logging/file_logger.py": "",
    "src/infrastructure/logging/log_formatter.py": "",

    # configurações
    "src/infrastructure/config/__init__.py": "",
    "src/infrastructure/config/settings.py": "",
    "src/infrastructure/config/constants.py": "",

    # seed / bootstrap
    "src/infrastructure/seed/__init__.py": "",
    "src/infrastructure/seed/seed_admin.py": "",
    "src/infrastructure/seed/seed_roles.py": "",
    "src/infrastructure/seed/seed_permissions.py": "",

    # ── interface – API FastAPI ───────────────────────────────────────────────
    "src/interface/__init__.py": "",
    "src/interface/api/__init__.py": "",
    "src/interface/api/main.py": "",
    "src/interface/api/dependencies.py": "",
    "src/interface/api/middleware/__init__.py": "",
    "src/interface/api/middleware/cors.py": "",
    "src/interface/api/middleware/logging_middleware.py": "",
    "src/interface/api/middleware/auth_middleware.py": "",

    # rotas públicas – auth / token
    "src/interface/api/routes/__init__.py": "",
    "src/interface/api/routes/auth.py": "",
    "src/interface/api/routes/token.py": "",

    # rotas de gestão (admin)
    "src/interface/api/routes/admin/__init__.py": "",
    "src/interface/api/routes/admin/users.py": "",
    "src/interface/api/routes/admin/roles.py": "",
    "src/interface/api/routes/admin/permissions.py": "",
    "src/interface/api/routes/admin/groups.py": "",
    "src/interface/api/routes/admin/rbac_attributes.py": "",
    "src/interface/api/routes/admin/settings.py": "",
    "src/interface/api/routes/admin/audit_logs.py": "",

    # schemas Pydantic
    "src/interface/api/schemas/__init__.py": "",
    "src/interface/api/schemas/auth_schema.py": "",
    "src/interface/api/schemas/user_schema.py": "",
    "src/interface/api/schemas/role_schema.py": "",
    "src/interface/api/schemas/permission_schema.py": "",
    "src/interface/api/schemas/group_schema.py": "",
    "src/interface/api/schemas/rbac_schema.py": "",
    "src/interface/api/schemas/settings_schema.py": "",
    "src/interface/api/schemas/audit_schema.py": "",
    "src/interface/api/schemas/common_schema.py": "",

    # ── interface – Web App ───────────────────────────────────────────────────
    "src/interface/webapp/__init__.py": "",
    "src/interface/webapp/main.py": "",
    "src/interface/webapp/dependencies.py": "",
    "src/interface/webapp/routes/__init__.py": "",
    "src/interface/webapp/routes/login.py": "",
    "src/interface/webapp/routes/dashboard.py": "",
    "src/interface/webapp/routes/users.py": "",
    "src/interface/webapp/routes/roles.py": "",
    "src/interface/webapp/routes/permissions.py": "",
    "src/interface/webapp/routes/groups.py": "",
    "src/interface/webapp/routes/rbac_attributes.py": "",
    "src/interface/webapp/routes/settings.py": "",
    "src/interface/webapp/routes/audit_logs.py": "",
    "src/interface/webapp/middleware/__init__.py": "",
    "src/interface/webapp/middleware/session_auth.py": "",

    # templates Jinja2
    "src/interface/webapp/templates/base.html": "",
    "src/interface/webapp/templates/login.html": "",
    "src/interface/webapp/templates/dashboard.html": "",
    "src/interface/webapp/templates/users/list.html": "",
    "src/interface/webapp/templates/users/form.html": "",
    "src/interface/webapp/templates/users/detail.html": "",
    "src/interface/webapp/templates/roles/list.html": "",
    "src/interface/webapp/templates/roles/form.html": "",
    "src/interface/webapp/templates/permissions/list.html": "",
    "src/interface/webapp/templates/permissions/form.html": "",
    "src/interface/webapp/templates/groups/list.html": "",
    "src/interface/webapp/templates/groups/form.html": "",
    "src/interface/webapp/templates/rbac/list.html": "",
    "src/interface/webapp/templates/rbac/form.html": "",
    "src/interface/webapp/templates/settings/index.html": "",
    "src/interface/webapp/templates/audit/list.html": "",
    "src/interface/webapp/templates/partials/navbar.html": "",
    "src/interface/webapp/templates/partials/sidebar.html": "",
    "src/interface/webapp/templates/partials/footer.html": "",
    "src/interface/webapp/templates/partials/alerts.html": "",
    "src/interface/webapp/templates/errors/404.html": "",
    "src/interface/webapp/templates/errors/403.html": "",
    "src/interface/webapp/templates/errors/500.html": "",

    # estáticos
    "src/interface/webapp/static/css/main.css": "",
    "src/interface/webapp/static/css/variables.css": "",
    "src/interface/webapp/static/js/main.js": "",
    "src/interface/webapp/static/js/api.js": "",
    "src/interface/webapp/static/img/.gitkeep": "",

    # ── testes ────────────────────────────────────────────────────────────────
    "tests/__init__.py": "",
    "tests/conftest.py": "",

    "tests/unit/__init__.py": "",
    "tests/unit/domain/__init__.py": "",
    "tests/unit/domain/test_user_entity.py": "",
    "tests/unit/domain/test_role_entity.py": "",
    "tests/unit/domain/test_permission_entity.py": "",
    "tests/unit/domain/test_value_objects.py": "",

    "tests/unit/application/__init__.py": "",
    "tests/unit/application/test_login_use_case.py": "",
    "tests/unit/application/test_create_user_use_case.py": "",
    "tests/unit/application/test_rbac_use_case.py": "",

    "tests/integration/__init__.py": "",
    "tests/integration/test_auth_api.py": "",
    "tests/integration/test_users_api.py": "",
    "tests/integration/test_roles_api.py": "",
    "tests/integration/test_permissions_api.py": "",
    "tests/integration/test_groups_api.py": "",
    "tests/integration/test_rbac_api.py": "",
    "tests/integration/test_settings_api.py": "",

    "tests/e2e/__init__.py": "",
    "tests/e2e/test_full_login_flow.py": "",
    "tests/e2e/test_admin_webapp.py": "",

    # ── logs (diretórios vazios) ───────────────────────────────────────────────
    "logs/.gitkeep": "",
    "logs/yaml/.gitkeep": "",
    "logs/json/.gitkeep": "",
    "logs/md/.gitkeep": "",

    # ── dados ─────────────────────────────────────────────────────────────────
    "data/.gitkeep": "",
}


def create_structure():
    from colorama import init, Fore, Style
    from rich.console import Console
    from rich.panel import Panel
    from rich.progress import track

    init(autoreset=True)
    console = Console()

    console.print(Panel.fit(
        "[bold orange1]🚀 APOLLO-IAM-ENGINE-API-SERVICE[/bold orange1]\n"
        "[dim]Criando estrutura do projeto...[/dim]\n"
        "[dim]O2 Data Solutions[/dim]",
        border_style="orange1"
    ))

    items = list(STRUCTURE.items())

    for rel_path, content in track(items, description="[orange1]Criando arquivos...[/orange1]"):
        full_path = os.path.join(BASE, rel_path)
        dir_path = os.path.dirname(full_path)

        if dir_path:
            os.makedirs(dir_path, exist_ok=True)

        if not os.path.exists(full_path):
            with open(full_path, "w", encoding="utf-8") as f:
                f.write(content)
            console.print(f"  [green]✅[/green] {rel_path}")
        else:
            console.print(f"  [yellow]⚠️  já existe:[/yellow] {rel_path}")

    console.print(Panel.fit(
        f"[bold green]✅ Estrutura criada em:[/bold green] [cyan]{BASE}/[/cyan]\n"
        "[dim]Próximo passo: execute o script de população dos arquivos.[/dim]",
        border_style="green"
    ))


if __name__ == "__main__":
    create_structure()
