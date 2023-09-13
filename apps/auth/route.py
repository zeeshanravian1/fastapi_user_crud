"""
    Authentication Route Module

    Description:
    - This module is responsible for handling auth routes.
    - It is used to login, refresh token, logout user.

"""

# Importing Python Packages
from sqlalchemy.ext.asyncio import AsyncSession

# Importing FastAPI Packages
from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse

# Importing Project Files
from database import get_session
from .response_message import auth_response_message
from .schema import (
    RegisterAdminSchema,
    RegisterAdminReadSchema,
    LoginReadSchema,
    RefreshToken,
    RefreshTokenReadSchema,
)
from .view import auth_view


# Router Object to Create Routes
router = APIRouter(prefix="/auth", tags=["Authentication"])


# -----------------------------------------------------------------------------


# Create a single admin user route
@router.post(
    path="/register/",
    status_code=status.HTTP_201_CREATED,
    summary="Create a single admin user",
    response_description="Admin user created successfully",
)
async def register_admin_user(
    record: RegisterAdminSchema,
    db_session: AsyncSession = Depends(get_session),
) -> RegisterAdminReadSchema:
    """
    Register a single admin user.

    Description:
    - This method is used to create a single admin user for an organization.

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
    print("Calling register_admin_user method")

    result = await auth_view.register_admin_user(
        db_session=db_session, record=record
    )

    if (
        result.get("detail")
        == auth_response_message.ORGANIZATION_ALREADY_EXISTS
    ):
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={
                "detail": auth_response_message.ORGANIZATION_ALREADY_EXISTS
            },
        )

    if result.get("detail") == auth_response_message.USERNAME_ALREADY_EXISTS:
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"detail": auth_response_message.USERNAME_ALREADY_EXISTS},
        )

    if result.get("detail") == auth_response_message.EMAIL_ALREADY_EXISTS:
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"detail": auth_response_message.EMAIL_ALREADY_EXISTS},
        )

    return RegisterAdminReadSchema.model_validate(obj=result)


# Login route
@router.post(
    path="/login/",
    status_code=status.HTTP_200_OK,
    summary="Perform Authentication",
    response_description="User logged in successfully",
)
async def login(
    db_session: AsyncSession = Depends(get_session),
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> LoginReadSchema:
    """
    Login.

    Description:
    - This route is used to login user.

    Parameter:
    - **email or username** (STR): Email or username of user. **(Required)**
    - **password** (STR): Password of user. **(Required)**

    Return:
    - **token_type** (STR): Token type of user.
    - **access_token** (STR): Access token of user.
    - **refresh_token** (STR): Refresh token of user.
    - **role_id** (INT): Role ID of user.

    """
    print("Calling login method")

    result = await auth_view.login(db_session=db_session, form_data=form_data)

    if result.get("detail") == auth_response_message.USER_NOT_FOUND:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": auth_response_message.USER_NOT_FOUND},
        )

    if result.get("detail") == auth_response_message.INCORRECT_PASSWORD:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": auth_response_message.INCORRECT_PASSWORD},
        )

    return LoginReadSchema.model_validate(obj=result)


# Refresh token route
@router.post(
    path="/refresh/",
    status_code=status.HTTP_200_OK,
    summary="Refreshes Authentication Token",
    response_description="Token refreshed successfully",
)
async def refresh_token(
    record: RefreshToken, db_session: AsyncSession = Depends(get_session)
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
    print("Calling refresh_token method")

    result = await auth_view.refresh_token(
        db_session=db_session, record=record
    )

    if result.get("detail") == auth_response_message.USER_NOT_FOUND:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": auth_response_message.USER_NOT_FOUND},
        )

    return RefreshTokenReadSchema.model_validate(obj=result)
