"""
    Authentication Pydantic Schemas

    Description:
    - This module contains all auth schemas used by API.

"""

# Importing Python Packages
from pydantic import BaseModel, Field

# Importing FastAPI Packages

# Importing Project Files
from apps.base.configuration import base_configuration
from apps.organization.schema import (
    OrganizationCreateSchema,
    OrganizationReadSchema,
)
from apps.user.schema import UserCreateSchema, UserReadSchema
from .configuration import auth_configuration


# -----------------------------------------------------------------------------


class RegisterAdminSchema(OrganizationCreateSchema, UserCreateSchema):
    """
    Register Admin Schema

    Description:
    - This schema is used to validate register admin data passed to API.

    """


class RegisterAdminReadSchema(OrganizationReadSchema, UserReadSchema):
    """
    Register Admin Read Schema

    Description:
    - This schema is used to validate register admin data returned from API.

    """


class LoginReadSchema(BaseModel):
    """
    Login Read Schema

    Description:
    - This schema is used to validate login data returned from API.

    """

    token_type: str = Field(example=auth_configuration.TOKEN_TYPE)
    access_token: str = Field(example=auth_configuration.ACCESS_TOKEN)
    refresh_token: str = Field(example=auth_configuration.REFRESH_TOKEN)
    role_id: int = Field(example=base_configuration.ID)


class RefreshToken(BaseModel):
    """
    Refresh Token Schema

    Description:
    - This schema is used to validate refresh token passed to API.

    """

    refresh_token: str = Field(example=auth_configuration.REFRESH_TOKEN)


class RefreshTokenReadSchema(BaseModel):
    """
    Refresh Token Read Schema

    Description:
    - This schema is used to validate refresh token data returned from API.

    """

    token_type: str = Field(example=auth_configuration.TOKEN_TYPE)
    access_token: str = Field(example=auth_configuration.ACCESS_TOKEN)
