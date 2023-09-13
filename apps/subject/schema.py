"""
    Subject Pydantic Schemas

    Description:
    - This module contains all subject schemas used by API.

"""

# Importing Python Packages
from pydantic import BaseModel, Field

# Importing FastAPI Packages

# Importing Project Files
from apps.base import BaseReadSchema
from .configuration import subject_configuration


# -----------------------------------------------------------------------------


class SubjectBaseSchema(BaseModel):
    """
    Subject Base Schema

    Description:
    - This schema is used to validate subject base data passed to API.

    """

    subject_name: str | None = Field(
        default=None, example=subject_configuration.SUBJECT
    )
    grade_level: int | None = Field(
        default=None, example=subject_configuration.GRADE
    )

    class Config:
        """
        Pydantic Config

        Description:
        - This class is used to configure Pydantic schema.

        """

        str_strip_whitespace = True
        from_attributes = True


class SubjectCreateSchema(SubjectBaseSchema):
    """
    Subject create Schema

    Description:
    - This schema is used to validate subject creation data passed to API.

    """

    subject_name: str = Field(
        min_length=1,
        max_length=2_55,
        example=subject_configuration.SUBJECT,
    )
    grade_level: int = Field(ge=1, le=12, example=subject_configuration.GRADE)


class SubjectReadSchema(SubjectCreateSchema, BaseReadSchema):
    """
    Subject Read Schema

    Description:
    - This schema is used to validate subject data returned from API.

    """


class SubjectGradeReadSchema(BaseModel):
    """
    Subject Pagination Read Schema

    Description:
    - This schema is used to validate subject pagination data returned from
    API.

    """

    records: list[SubjectReadSchema]


class SubjectUpdateSchema(SubjectCreateSchema):
    """
    Subject Update Schema

    Description:
    - This schema is used to validate subject update data passed to API.

    """


class SubjectPartialUpdateSchema(SubjectBaseSchema):
    """
    Subject Update Schema

    Description:
    - This schema is used to validate subject update data passed to API.

    """
