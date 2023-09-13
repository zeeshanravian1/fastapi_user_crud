"""
    User Model

    Description:
    - This file contains model for user table.

"""

# Importing Python Packages
from sqlalchemy import Boolean, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

# Importing FastAPI Packages

# Importing Project Files
from database import BaseTable
from apps.organization.model import OrganizationTable
from apps.role.model import RoleTable


# -----------------------------------------------------------------------------


class UserTable(BaseTable):
    """
    User Table

    Description:
    - This table is used to create user in database.

    """

    username: Mapped[str] = mapped_column(
        String(2_55), unique=True, nullable=False
    )
    email: Mapped[str] = mapped_column(
        String(2_55), unique=True, nullable=False
    )
    password: Mapped[str] = mapped_column(String(2_55), nullable=False)
    is_super_user: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False, server_default="false"
    )
    is_admin: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False, server_default="false"
    )
    role_id: Mapped[int] = mapped_column(
        ForeignKey(RoleTable.id), nullable=False
    )
    organization_id: Mapped[int] = mapped_column(
        ForeignKey(OrganizationTable.id), nullable=True
    )

    # Relationship
    user_role = relationship(
        "RoleTable", back_populates="role_user", lazy="joined"
    )
    user_organization = relationship(
        "OrganizationTable", back_populates="organization_user", lazy="joined"
    )
