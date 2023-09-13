"""
    Token, Scopes, and Security

    Description:
    - This module is used to create a token for user and get current user.

"""

# Importing Python packages
import traceback
from datetime import datetime, timedelta
from jose import jwt, JWTError
from pydantic import ValidationError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine.result import ChunkedIteratorResult
from sqlalchemy.sql.selectable import Select


# Importing FastAPI packages
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

# Importing from project files
from database.session import get_session
from core import core_configuration
from apps.user.model import UserTable
from .schema import CurrentUserReadSchema


# -----------------------------------------------------------------------------


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login/")


def create_token(data: dict, token_type: str | None = None) -> str:
    """
    Create an access token from a user id and scopes

    Description:
    - This function is used to create an access token from a user id and
    scopes.

    Parameters:
    - **data**:Data to be used to create token. (DICT)
    - **token_type**: Type of token to be created. (STR)
        - **Allowed values:** "access", "refresh"

    Returns:
    - **access_token**: Access token. (STR)

    """
    print("Calling create_token method")

    to_encode = data.copy()

    if token_type == "access_token":
        expire = datetime.utcnow() + timedelta(
            minutes=core_configuration.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    elif token_type == "refresh_token":
        expire = datetime.utcnow() + timedelta(
            days=core_configuration.REFRESH_TOKEN_EXPIRE_MINUTES
        )

    to_encode.update({"exp": expire})

    return jwt.encode(
        to_encode,
        core_configuration.SECRET_KEY,
        algorithm=core_configuration.ALGORITHM,
    )


async def get_current_user(
    db_session: AsyncSession = Depends(get_session),
    access_token: str = Depends(oauth2_scheme),
) -> CurrentUserReadSchema:
    """
    Get current user.

    Description:
    - This function is used to get current user.

    Parameters:
    - **token**  (STR): Token to be used to get user.

    Returns:
    - **user** (CurrentUserReadSchema): User details.

    """
    print("Calling get_current_user method")

    authenticate_value = "Bearer"

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )

    try:
        payload = jwt.decode(
            token=access_token,
            key=core_configuration.SECRET_KEY,
            algorithms=[core_configuration.ALGORITHM],
        )
        user_id: str = payload.get("id")
        user_name: str = payload.get("username")
        user_email: str = payload.get("email")

        if user_name is None or user_email is None:
            raise credentials_exception

    except (JWTError, ValidationError) as err:
        raise credentials_exception from err

    except Exception as err:
        err_message = f"{traceback.format_exc()}\n\n{str(err)}"
        print("err_message --> ", err_message)

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong while getting current user",
        ) from err

    query: Select = select(UserTable).where(UserTable.id == user_id)
    result: ChunkedIteratorResult = await db_session.execute(statement=query)
    user_data: UserTable = result.scalars().first()

    if not user_data:
        raise credentials_exception

    return CurrentUserReadSchema(
        id=user_data.id,
        username=user_data.username,
        email=user_data.email,
        role_id=user_data.role_id,
        role_name=user_data.user_role.role_name,
        created_at=user_data.created_at,
        updated_at=user_data.updated_at,
    )

    # if user_data.is_super_user:
    #     return CurrentUserReadSchema(
    #         id=user_data.id,
    #         username=user_data.username,
    #         email=user_data.email,
    #         role_id=user_data.role_id,
    #         role_name=user_data.user_role.role_name,
    #         created_at=user_data.created_at,
    #         updated_at=user_data.updated_at,
    #     )

    # return CurrentUserReadSchema(
    #     id=user_data.id,
    #     username=user_data.username,
    #     email=user_data.email,
    #     role_id=user_data.role_id,
    #     role_name=user_data.user_role.role_name,
    #     organization_id=user_data.organization_id,
    #     organization_name=user_data.user_organization.organization_name,
    #     created_at=user_data.created_at,
    #     updated_at=user_data.updated_at,
    # )
