from sqlalchemy.orm import Session
from src.infrastructure.database.models.user_model import UserModel
from src.infrastructure.database.models.role_model import RoleModel
from src.infrastructure.security.password_hasher_impl import BcryptPasswordHasher
from src.infrastructure.config.settings import get_settings
import uuid

settings = get_settings()
hasher = BcryptPasswordHasher()


def seed_admin(db: Session):
    existing = db.query(UserModel).filter_by(username=settings.admin_username).first()
    if existing:
        return
    role = db.query(RoleModel).filter_by(name="superadmin").first()
    admin = UserModel(
        id=str(uuid.uuid4()),
        username=settings.admin_username,
        email="admin@apollo.local",
        hashed_password=hasher.hash(settings.admin_password),
        full_name="Administrator",
        is_active=True,
        is_superuser=True,
    )
    if role:
        admin.roles.append(role)
    db.add(admin)
    db.commit()
