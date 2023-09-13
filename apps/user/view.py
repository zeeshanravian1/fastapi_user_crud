"""
    User View Module

    Description:
    - This module is responsible for user views.

"""

# Importing Python Packages
from passlib.hash import pbkdf2_sha256
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update
from sqlalchemy.sql.dml import Update

# Importing FastAPI Packages

# Importing Project Files
from apps.base import BaseView
from .response_message import user_response_message
from .model import UserTable
from .schema import UserCreateSchema, UserUpdateSchema, PasswordChangeSchema


# -----------------------------------------------------------------------------


# User class
class UserView(
    BaseView[
        UserTable,
        UserCreateSchema,
        UserUpdateSchema,
    ]
):
    """
    User View Class

    Description:
    - This class is responsible for user views.

    """

    def __init__(
        self,
        model: UserTable,
    ):
        """
        User View Class Initialization

        Description:
        - This method is responsible for initializing class.

        Parameter:
        - **model** (UserTable): User Database Model.

        """

        super().__init__(model=model)

    async def create(
        self, db_session: AsyncSession, record: UserCreateSchema
    ) -> UserTable:
        """
        Create User

        Description:
        - This method is responsible for creating user.

        Parameter:
        - **db_session** (Session): Database session.
        - **record** (UserCreateSchema): User create schema.

        Return:
        - **UserTable**: User database model.

        """

        record.password = pbkdf2_sha256.hash(record.password)

        return await super().create(db_session=db_session, record=record)

    async def change_password(
        self,
        db_session: AsyncSession,
        record_id: int,
        record: PasswordChangeSchema,
    ) -> dict:
        """
        Change Password

        Description:
        - This method is responsible for changing user password.

        Parameter:
        - **db_session** (Session): Database session.
        - **record** (PasswordChangeSchema): Password change schema.

        Return:
        - **None**

        """

        result = await super().read_by_id(
            db_session=db_session, record_id=record_id
        )

        if not result:
            return {"detail": user_response_message.USER_NOT_FOUND}

        if not pbkdf2_sha256.verify(record.old_password, result.password):
            return {"detail": user_response_message.INCORRECT_PASSWORD}

        query: Update = (
            update(self.model)
            .where(self.model.id == record_id)
            .values({"password": pbkdf2_sha256.hash(record.new_password)})
        )
        await db_session.execute(statement=query)
        await db_session.commit()

        return {"detail": user_response_message.PASSWORD_CHANGED}


user_view = UserView(model=UserTable)
