"""
    Core Pydantic Schemas

    Description:
    - This module contains all core schemas used by API.

"""

# Importing Python Packages
from pydantic import Field

# Importing FastAPI Packages

# Importing Project Files
from apps.base.configuration import base_configuration
from apps.organization.configuration import organization_configuration
from apps.organization.schema import (
    OrganizationReadSchema,
)
from apps.role.configuration import role_configuration
from apps.user.schema import UserReadSchema


# -----------------------------------------------------------------------------


class CurrentUserReadSchema(OrganizationReadSchema, UserReadSchema):
    """
    Current User Read Schema

    Description:
    - This schema is used to validate current user data.

    """

    role_name: str = Field(example=role_configuration.ROLE)
    organization_id: int | None = Field(
        default=None, example=base_configuration.ID
    )
    organization_name: str | None = Field(
        default=None, example=organization_configuration.ORGANIZATION
    )
