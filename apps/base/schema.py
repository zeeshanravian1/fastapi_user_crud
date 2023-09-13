"""
    Base Read Pydantic Schema

    Description:
    - This module contains base read schema used by API.

"""

# Importing Python Packages
from datetime import datetime
from pydantic import BaseModel, Field

# Importing FastAPI Packages

# Importing Project Files
from .configuration import base_configuration


# -----------------------------------------------------------------------------


class BaseReadSchema(BaseModel):
    """
    Base Read Schema

    Description:
    - This schema is used to validate base data returned from API.

    """

    id: int = Field(example=base_configuration.ID)
    created_at: datetime = Field(example=base_configuration.CREATED_AT)
    updated_at: datetime = Field(example=base_configuration.UPDATED_AT)


class BasePaginationReadSchema(BaseModel):
    """
    Base Pagination Read Schema

    Description:
    - This schema is used to validate base pagination data returned from API.

    """

    total_records: int = Field(example=base_configuration.TOTAL_RECORDS)
    page: int = Field(example=base_configuration.PAGE)
    limit: int = Field(example=base_configuration.LIMIT)
    records: list = Field(example=[])
