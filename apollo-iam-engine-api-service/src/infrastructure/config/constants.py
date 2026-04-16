DEFAULT_ROLES = ["superadmin", "admin", "operator", "viewer"]
DEFAULT_PERMISSIONS = [
    ("users:read",   "users",   "read"),
    ("users:write",  "users",   "write"),
    ("users:delete", "users",   "delete"),
    ("roles:read",   "roles",   "read"),
    ("roles:write",  "roles",   "write"),
    ("perms:read",   "permissions", "read"),
    ("perms:write",  "permissions", "write"),
    ("groups:read",  "groups",  "read"),
    ("groups:write", "groups",  "write"),
    ("rbac:read",    "rbac",    "read"),
    ("rbac:write",   "rbac",    "write"),
    ("settings:read",  "settings", "read"),
    ("settings:write", "settings", "write"),
    ("audit:read",   "audit",   "read"),
]
