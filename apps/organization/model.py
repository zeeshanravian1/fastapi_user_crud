"""
    Organization Model

    Description:
    - This file contains model for organization table.

"""

# Importing Python Packages
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

# Importing FastAPI Packages

# Importing Project Files
from database import BaseTable


# -----------------------------------------------------------------------------


class OrganizationTable(BaseTable):
    """
    Organization Table

    Description:
    - This table is used to create organization in database.

    """

    organization_name: Mapped[str] = mapped_column(
        String(2_55), unique=True, nullable=False
    )
    organization_description: Mapped[str] = mapped_column(
        String(2_55), nullable=True
    )

    # Relationship
    organization_user = relationship(
        "UserTable", back_populates="user_organization"
    )
