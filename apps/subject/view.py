"""
    Subject View Module

    Description:
    - This module is responsible for subject views.

"""

# Importing Python Packages
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine.result import ChunkedIteratorResult
from sqlalchemy.sql.selectable import Select
from sqlalchemy.sql.dml import Delete

# Importing FastAPI Packages

# Importing Project Files
from apps.base import BaseView
from .response_message import subject_response_message
from .model import SubjectTable
from .schema import (
    SubjectCreateSchema,
    SubjectUpdateSchema,
)


# -----------------------------------------------------------------------------


# Subject class
class SubjectView(
    BaseView[
        SubjectTable,
        SubjectCreateSchema,
        SubjectUpdateSchema,
    ]
):
    """
    Subject View Class

    Description:
    - This class is responsible for subject views.

    """

    def __init__(
        self,
        model: SubjectTable,
    ):
        """
        Subject View Class Initialization

        Description:
        - This method is responsible for initializing class.

        Parameter:
        - **model** (SubjectTable): Subject Database Model.

        """

        super().__init__(model=model)

    async def create(
        self, db_session: AsyncSession, record: SubjectCreateSchema
    ) -> SubjectTable:
        """
        Create Method

        Description:
        - This method is responsible for creating a single subject.

        Parameter:
        - **db_session** (Session): Database session. **(Required)**
        - **record** (CreateSchema): Create Schema. **(Required)**

        Return:
        - **record** (SubjectTable): SubjectTable Model Object.

        """

        query: Select = select(SubjectTable).where(
            SubjectTable.subject_name == record.subject_name,
            SubjectTable.grade_level == record.grade_level,
        )
        result: ChunkedIteratorResult = await db_session.execute(
            statement=query
        )

        if result.scalars().first():
            return {"detail": subject_response_message.SUBJECT_ALREADY_CREATED}

        record: SubjectTable = SubjectTable(**record.model_dump())
        db_session.add(instance=record)
        await db_session.commit()
        await db_session.refresh(instance=record)

        return record

    async def read_all_subjects_by_grade_level(
        self,
        grade_level: int,
        db_session: AsyncSession,
    ) -> list[SubjectTable]:
        """
        Read All Method

        Description:
        - This method is responsible for reading all subjects of single grade
        level.

        Parameter:
        - **grade_level** (INT): Grade level of subject. **(Required)**
        - **db_session** (Session): Database session. **(Required)**

        Return:
        - **records** (LIST): List of subjects.

        """

        query: Select = (
            select(self.model)
            .where(self.model.grade_level == grade_level)
            .order_by(self.model.id)
        )
        result: ChunkedIteratorResult = await db_session.execute(
            statement=query
        )

        return result.scalars().all()

    async def delete_by_grade_level(
        self, grade_level: int, db_session: AsyncSession
    ) -> SubjectTable:
        """
        Delete Method

        Description:
        - This method is responsible for deleting a record.

        Parameter:
        - **db_session** (Session): Database session. **(Required)**
        - **grade_level** (INT): Grade level of subject. **(Required)**

        Return:
        - **record** (Model): SqlAlchemy Model Object.

        """

        result: SubjectTable = await self.read_all_subjects_by_grade_level(
            grade_level=grade_level, db_session=db_session
        )

        if not result:
            return None

        query: Delete = delete(self.model).where(
            self.model.grade_level == grade_level
        )
        await db_session.execute(statement=query)
        await db_session.commit()

        return result


subject_view = SubjectView(model=SubjectTable)
