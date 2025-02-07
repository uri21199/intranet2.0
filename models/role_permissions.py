from sqlalchemy import Table, Column, Integer, ForeignKey
from config import Base

role_permissions = Table(
    "role_permissions",
    Base.metadata,
    Column("role_id", Integer, ForeignKey("general.roles.id"), primary_key=True),
    Column("permission_id", Integer, ForeignKey("general.permissions.id"), primary_key=True),
    schema="general"
)
