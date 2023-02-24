import sqlalchemy
from models.enums import RoleType
from db import metadata

user = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("email", sqlalchemy.String(120), unique=True),
    sqlalchemy.Column("password", sqlalchemy.String(225)),
    sqlalchemy.Column("first_name", sqlalchemy.String(200)),
    sqlalchemy.Column("last_name", sqlalchemy.String(200)),
    sqlalchemy.Column("phone_number", sqlalchemy.String(13), unique=True),
    sqlalchemy.Column(
        "role",
        sqlalchemy.Enum(RoleType),
        nullable=False,
        server_default=RoleType.complainer.name,
    ),
    sqlalchemy.Column("iban", sqlalchemy.String(200)),
)
