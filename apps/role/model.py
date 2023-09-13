"""
    Role Model

    Description:
    - This file contains model for role table.

"""

# Importing Python Packages
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

# Importing FastAPI Packages

# Importing Project Files
from database import BaseTable


# -----------------------------------------------------------------------------


class RoleTable(BaseTable):
    """
    Role Table

    Description:
    - This table is used to create role in database.

    """

    role_name: Mapped[str] = mapped_column(
        String(2_55), unique=True, nullable=False
    )
    role_description: Mapped[str] = mapped_column(String(2_55), nullable=False)

    # Relationship
    role_user = relationship("UserTable", back_populates="user_role")
