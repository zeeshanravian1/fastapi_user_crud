"""
    Authentication View Module

    Description:
    - This module is responsible for auth views.

"""

# Importing Python Packages
from jose import jwt
from passlib.hash import pbkdf2_sha256
from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine.result import ChunkedIteratorResult
from sqlalchemy.sql.selectable import Select

# Importing FastAPI Packages
from fastapi.security import OAuth2PasswordRequestForm

# Importing Project Files
from core import core_configuration
from core.security import create_token
from apps.organization.model import OrganizationTable
from apps.user.model import UserTable
from .configuration import auth_configuration
from .response_message import auth_response_message
from .schema import (
    RegisterAdminSchema,
    RegisterAdminReadSchema,
    LoginReadSchema,
    RefreshToken,
    RefreshTokenReadSchema,
)


# -----------------------------------------------------------------------------


# Authentication class
class AuthView:
    """
    Authentication View Class

    Description:
    - This class is responsible for auth views.

    """

    async def register_admin_user(
        self, db_session: AsyncSession, record=RegisterAdminSchema
    ) -> RegisterAdminReadSchema:
        """
        Register a single admin user.

        Description:
        - This method is used to create a single admin user for an
        organization.

        Parameter:
        Admin user details to be created with following fields:
        - **username** (STR): Username of user. **(Required)**
        - **email** (STR): Email of user. **(Required)**
        - **password** (STR): Password of user. **(Required)**
        - **role_id** (INT): Role ID of user. **(Required)**
        - **organization_name** (STR): Name of organization. **(Required)**
        - **organization_description** (STR): Description of organization.
        **(Optional)**

        Returns:
        Admin user details along with following information:
        - **id** (INT): Id of user.
        - **username** (STR): Username of user.
        - **email** (STR): Email of user.
        - **role_id** (INT): Role ID of user.
        - **organization_name** (STR): Name of organization.
        - **organization_description** (STR): Description of organization.
        - **created_at** (DATETIME): Datetime of user creation.
        - **updated_at** (DATETIME): Datetime of user updation.

        """

        # Verify if organization or Admin already created
        query: Select = select(OrganizationTable).where(
            OrganizationTable.organization_name == record.organization_name
        )
        result: ChunkedIteratorResult = await db_session.execute(
            statement=query
        )
        organization_data: UserTable = result.scalars().first()

        if organization_data:
            return {
                "detail": auth_response_message.ORGANIZATION_ALREADY_EXISTS
            }

        query: Select = select(UserTable).where(
            or_(
                UserTable.username == record.username,
                UserTable.email == record.email,
            )
        )
        result: ChunkedIteratorResult = await db_session.execute(
            statement=query
        )
        user_data: UserTable = result.scalars().first()

        if user_data:
            if user_data.username == record.username:
                return {
                    "detail": auth_response_message.USERNAME_ALREADY_EXISTS
                }

            if user_data.email == record.email:
                return {"detail": auth_response_message.EMAIL_ALREADY_EXISTS}

        # Create Organization
        organization_record: OrganizationTable = OrganizationTable(
            organization_name=record.organization_name,
            organization_description=record.organization_description,
        )
        db_session.add(instance=organization_record)
        await db_session.commit()
        await db_session.refresh(instance=organization_record)

        # Create Admin User
        user_record: UserTable = UserTable(
            username=record.username,
            email=record.email,
            password=pbkdf2_sha256.hash(record.password),
            is_admin=True,
            role_id=record.role_id,
            organization_id=organization_record.id,
        )

        db_session.add(instance=user_record)
        await db_session.commit()
        await db_session.refresh(instance=user_record)

        return {
            "id": user_record.id,
            "username": record.username,
            "email": record.email,
            "role_id": record.role_id,
            "organization_name": record.organization_name,
            "organization_description": record.organization_description,
            "created_at": user_record.created_at,
            "updated_at": user_record.updated_at,
        }

    async def login(
        self, db_session: AsyncSession, form_data: OAuth2PasswordRequestForm
    ) -> LoginReadSchema:
        """
        Login.

        Description:
        - This route is used to login user.

        Parameter:
        - **username** (STR): Email or username of user. **(Required)**
        - **password** (STR): Password of user. **(Required)**

        Return:
        - **token_type** (STR): Token type of user.
        - **access_token** (STR): Access token of user.
        - **refresh_token** (STR): Refresh token of user.

        """

        form_data.username = form_data.username.lower()
        form_data.password = form_data.password.lower()

        query: Select = select(UserTable).where(
            or_(
                UserTable.username == form_data.username,
                UserTable.email == form_data.username,
            )
        )
        result: ChunkedIteratorResult = await db_session.execute(
            statement=query
        )
        user_data: UserTable = result.scalars().first()

        if not user_data:
            return {"detail": auth_response_message.USER_NOT_FOUND}

        if not pbkdf2_sha256.verify(form_data.password, user_data.password):
            return {"detail": auth_response_message.INCORRECT_PASSWORD}

        data = {
            "id": user_data.id,
            "username": user_data.username,
            "email": user_data.email,
        }

        return {
            "token_type": auth_configuration.TOKEN_TYPE,
            "access_token": create_token(
                data=data, token_type=auth_configuration.ACCESS_TOKEN
            ),
            "refresh_token": create_token(
                data=data, token_type=auth_configuration.REFRESH_TOKEN
            ),
            "role_id": user_data.role_id,
        }

    async def refresh_token(
        self, db_session: AsyncSession, record: RefreshToken
    ) -> RefreshTokenReadSchema:
        """
        Refresh Token.

        Description:
        - This route is used to refresh token.

        Parameter:
        - **record** (STR): Refresh token of user. **(Required)**

        Return:
        - **token_type** (STR): Token type of user.
        - **access_token** (STR): Access token of user.

        """

        data = jwt.decode(
            token=record.refresh_token,
            key=core_configuration.SECRET_KEY,
            algorithms=[core_configuration.ALGORITHM],
        )

        query: Select = select(UserTable).where(
            UserTable.username == data.get("username"),
            UserTable.email == data.get("email"),
        )
        result: ChunkedIteratorResult = await db_session.execute(
            statement=query
        )
        user_data: UserTable = result.scalars().first()

        if not user_data:
            return {"detail": auth_response_message.USER_NOT_FOUND}

        return {
            "token_type": auth_configuration.TOKEN_TYPE,
            "access_token": create_token(
                data=data, token_type=auth_configuration.ACCESS_TOKEN
            ),
        }


auth_view = AuthView()
