"""
    User Pydantic Schemas

    Description:
    - This module contains all user schemas used by API.

"""

# Importing Python Packages
from pydantic import BaseModel, Field, EmailStr

# Importing FastAPI Packages

# Importing Project Files
from apps.base import BaseReadSchema, BasePaginationReadSchema
from .configuration import user_configuration


# -----------------------------------------------------------------------------


class UserBaseSchema(BaseModel):
    """
    User Base Schema

    Description:
    - This schema is used to validate user base data passed to API.

    """

    username: str | None = Field(
        default=None, example=user_configuration.USERNAME
    )
    email: EmailStr | None = Field(
        default=None, example=user_configuration.EMAIL
    )
    role_id: int | None = Field(
        default=None, example=user_configuration.ROLE_ID
    )

    class Config:
        """
        Pydantic Config

        Description:
        - This class is used to configure Pydantic schema.

        """

        str_strip_whitespace = True
        from_attributes = True
        str_to_lower = True


class UserCreateSchema(UserBaseSchema):
    """
    User create Schema

    Description:
    - This schema is used to validate user creation data passed to API.

    """

    username: str = Field(example=user_configuration.USERNAME)
    email: EmailStr = Field(example=user_configuration.EMAIL)
    password: str = Field(
        min_length=8,
        max_length=1_00,
        example=user_configuration.PASSWORD,
    )
    role_id: int = Field(example=user_configuration.ROLE_ID)


class UserReadSchema(UserBaseSchema, BaseReadSchema):
    """
    User Read Schema

    Description:
    - This schema is used to validate user data returned from API.

    """


class UserReadNameSchema(BaseModel):
    """
    User Read Name Schema

    Description:
    - This schema is used to validate user name data returned from API.

    """

    username: str = Field(example=user_configuration.USERNAME)

    class Config:
        """
        Pydantic Config

        Description:
        - This class is used to configure Pydantic schema.

        """

        str_strip_whitespace = True
        from_attributes = True
        str_to_lower = True


class UserPaginationReadSchema(BasePaginationReadSchema):
    """
    User Pagination Read Schema

    Description:
    - This schema is used to validate user pagination data returned from API.

    """

    records: list[UserReadSchema]


class UserUpdateSchema(BaseModel):
    """
    User Update Schema

    Description:
    - This schema is used to validate user update data passed to API.

    """

    username: str = Field(example=user_configuration.USERNAME)
    email: EmailStr = Field(example=user_configuration.EMAIL)
    role_id: int = Field(example=user_configuration.ROLE_ID)

    class Config:
        """
        Pydantic Config

        Description:
        - This class is used to configure Pydantic schema.

        """

        str_strip_whitespace = True
        from_attributes = True
        str_to_lower = True


class UserPartialUpdateSchema(UserBaseSchema):
    """
    User Update Schema

    Description:
    - This schema is used to validate user update data passed to API.

    """


class PasswordChangeSchema(BaseModel):
    """
    Change Password Schema

    Description:
    - This schema is used to validate change password data passed to API.

    """

    old_password: str = Field(
        min_length=8, max_length=1_00, example=user_configuration.PASSWORD
    )
    new_password: str = Field(
        min_length=8, max_length=1_00, example=user_configuration.PASSWORD
    )

    class Config:
        """
        Pydantic Config

        Description:
        - This class is used to configure Pydantic schema.

        """

        str_strip_whitespace = True
        from_attributes = True
        str_to_lower = True
