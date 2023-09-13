"""
    Insert initial data in database.

    Description:
    - This module is responsible for inserting initial data in database.

"""

# Importing Python Packages
from passlib.hash import pbkdf2_sha256
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy.engine.result import ChunkedIteratorResult
from sqlalchemy.sql.selectable import Select

# Importing FastAPI Packages

# Importing Project Files
from apps.role.model import RoleTable
from apps.user.model import UserTable
from apps.subject.model import SubjectTable
from core import core_configuration


# -----------------------------------------------------------------------------


# Insert database data
async def insert_db_data(db_session: async_sessionmaker[AsyncSession]) -> None:
    """
    Insert Database Data

    Description:
    - This function is used to insert initial data in database.

    Parameter:
    - **db_session** (async_sessionmaker[AsyncSession]): Database session.

    Return:
    - **None**

    """
    print("Calling insert_db_data method")

    try:
        async with db_session() as session:
            async with session.begin():
                # Insert Roles in database
                session.add_all(
                    instances=[
                        RoleTable(
                            role_name=core_configuration.SUPERUSER_ROLE,
                            role_description="Super Admin Role Description",
                        ),
                        RoleTable(
                            role_name="admin",
                            role_description="Admin Role Description",
                        ),
                        RoleTable(
                            role_name="teacher",
                            role_description="Teacher Role Description",
                        ),
                        RoleTable(
                            role_name="student",
                            role_description="Student Role Description",
                        ),
                        RoleTable(
                            role_name="parent",
                            role_description="Parent Role Description",
                        ),
                    ]
                )

                # Insert Super Admin in database

                # Get role id of Super Admin
                query: Select = select(RoleTable).where(
                    RoleTable.role_name == core_configuration.SUPERUSER_ROLE
                )
                result: ChunkedIteratorResult = await session.execute(
                    statement=query
                )
                role: RoleTable = result.scalars().first()

                # Insert Super Admin
                session.add(
                    instance=UserTable(
                        username=core_configuration.SUPERUSER_USERNAME,
                        email=core_configuration.SUPERUSER_EMAIL,
                        password=pbkdf2_sha256.hash(
                            core_configuration.SUPERUSER_PASSWORD
                        ),
                        is_super_user=True,
                        role_id=role.id,
                    )
                )

                # Insert Subjects in database
                session.add_all(
                    instances=[
                        SubjectTable(
                            subject_name="Mathematics", grade_level=1
                        ),
                        SubjectTable(subject_name="English", grade_level=1),
                        SubjectTable(
                            subject_name="Mathematics", grade_level=2
                        ),
                        SubjectTable(subject_name="English", grade_level=2),
                        SubjectTable(
                            subject_name="Mathematics", grade_level=3
                        ),
                        SubjectTable(subject_name="English", grade_level=3),
                        SubjectTable(
                            subject_name="Mathematics", grade_level=4
                        ),
                        SubjectTable(subject_name="English", grade_level=4),
                        SubjectTable(
                            subject_name="Mathematics", grade_level=5
                        ),
                        SubjectTable(subject_name="English", grade_level=5),
                    ]
                )

                await session.commit()

    except Exception:
        pass
