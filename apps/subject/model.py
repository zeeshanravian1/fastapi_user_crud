"""
    Subject Model

    Description:
    - This file contains model for subject table.

"""

# Importing Python Packages
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

# Importing FastAPI Packages

# Importing Project Files
from database import BaseTable


# -----------------------------------------------------------------------------


class SubjectTable(BaseTable):
    """
    Subject Table

    Description:
    - This table is used to create subject in database.

    """

    subject_name: Mapped[str] = mapped_column(String(2_55), nullable=False)
    grade_level: Mapped[int] = mapped_column(Integer, nullable=False)

    # Relationship
    subject_generalplan = relationship(
        "GeneralPlanTable", back_populates="generalplan_subject"
    )
