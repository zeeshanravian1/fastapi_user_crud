"""
    Subject Route Module

    Description:
    - This module is responsible for handling subject routes.
    - It is used to create, get, update, delete subject details.

"""

# Importing Python Packages
from sqlalchemy.ext.asyncio import AsyncSession

# Importing FastAPI Packages
from fastapi import APIRouter, Depends, Security, status
from fastapi.responses import JSONResponse

# Importing Project Files
from database.session import get_session
from core.security import get_current_user
from core.schema import CurrentUserReadSchema
from .response_message import subject_response_message
from .model import SubjectTable
from .schema import (
    SubjectCreateSchema,
    SubjectReadSchema,
    SubjectGradeReadSchema,
    SubjectUpdateSchema,
    SubjectPartialUpdateSchema,
)
from .view import subject_view

# Router Object to Create Routes
router = APIRouter(prefix="/subject", tags=["Subject"])


# -----------------------------------------------------------------------------


# Create a single subject route
@router.post(
    path="/",
    status_code=status.HTTP_201_CREATED,
    summary="Create a single subject",
    response_description="Subject created successfully",
)
async def create_subject(
    record: SubjectCreateSchema,
    db_session: AsyncSession = Depends(get_session),
    current_user: CurrentUserReadSchema = Security(get_current_user),
) -> SubjectReadSchema:
    """
    Create a single subject.

    Description:
    - This route is used to create a single subject.

    Parameter:
    Subject details to be created with following fields:
    - **subject_name** (STR): Name of subject. **(Required)**
    - **grade_level** (INT): Grade level of subject. **(Required)**

    Return:
    Subject details along with following information:
    - **id** (INT): Id of subject.
    - **subject_name** (STR): Name of subject.
    - **grade_level** (INT): Grade level of subject.
    - **created_at** (DATETIME): Datetime of subject creation.
    - **updated_at** (DATETIME): Datetime of subject updation.

    """
    print("Calling create_subject method")

    result: SubjectTable = await subject_view.create(
        db_session=db_session, record=record
    )

    if not isinstance(result, SubjectTable):
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={
                "detail": subject_response_message.SUBJECT_ALREADY_CREATED
            },
        )

    return SubjectReadSchema.model_validate(obj=result)


# Get a single subject by id route
@router.get(
    path="/{subject_id}/",
    status_code=status.HTTP_200_OK,
    summary="Get a single subject by providing id",
    response_description="Subject details fetched successfully",
)
async def get_subject_by_id(
    subject_id: int,
    db_session: AsyncSession = Depends(get_session),
    current_user: CurrentUserReadSchema = Security(get_current_user),
) -> SubjectReadSchema:
    """
    Get a single subject.

    Description:
    - This route is used to get a single subject by providing id.

    Parameter:
    - **subject_id** (INT): ID of subject to be fetched. **(Required)**

    Return:
    Get a single subject with following information:
    - **id** (INT): Id of subject.
    - **subject_name** (STR): Name of subject.
    - **grade_level** (INT): Grade level of subject.
    - **created_at** (DATETIME): Datetime of subject creation.
    - **updated_at** (DATETIME): Datetime of subject updation.

    """
    print("Calling get_subject_by_id method")

    result: SubjectTable = await subject_view.read_by_id(
        db_session=db_session, record_id=subject_id
    )

    if not result:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": subject_response_message.SUBJECT_NOT_FOUND},
        )

    return SubjectReadSchema.model_validate(obj=result)


# Get all subjects by grade level route
@router.get(
    path="/grade/{grade_level}/",
    status_code=status.HTTP_200_OK,
    summary="Get all subjects by providing grade level",
    response_description="All subjects fetched successfully",
)
async def get_all_subjects_by_grade_level(
    grade_level: int,
    db_session: AsyncSession = Depends(get_session),
    current_user: CurrentUserReadSchema = Security(get_current_user),
) -> SubjectGradeReadSchema:
    """
    Get all subjects by grade level.

    Description:
    - This route is used to get all subjects by providing grade level.

    Parameter:
    - **grade_level** (INT): Grade level of subjects to be fetched.
    **(Required)**

    Return:
    Get all subjects with following information:
    - **id** (INT): Id of subject.
    - **subject_name** (STR): Name of subject.
    - **grade_level** (INT): Grade level of subject.
    - **created_at** (DATETIME): Datetime of subject creation.
    - **updated_at** (DATETIME): Datetime of subject updation.

    """
    print("Calling get_all_subjects_by_grade_level method")

    result: dict = await subject_view.read_all_subjects_by_grade_level(
        grade_level=grade_level, db_session=db_session
    )

    if not result:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": subject_response_message.SUBJECT_NOT_FOUND},
        )

    return SubjectGradeReadSchema(records=result)


# Update a single subject route
@router.put(
    path="/{subject_id}/",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Update a single subject by providing id",
    response_description="Subject updated successfully",
)
async def update_subject(
    subject_id: int,
    record: SubjectUpdateSchema,
    db_session: AsyncSession = Depends(get_session),
    current_user: CurrentUserReadSchema = Security(get_current_user),
) -> SubjectReadSchema:
    """
    Update a single subject.

    Description:
    - This route is used to update a single subject by providing id.

    Parameter:
    - **subject_id** (INT): ID of subject to be updated. **(Required)**
    Subject details to be updated with following fields:
    - **subject_name** (STR): Name of subject. **(Required)**
    - **grade_level** (INT): Grade level of subject. **(Required)**

    Return:
    Subject details along with following information:
    - **id** (INT): Id of subject.
    - **subject_name** (STR): Name of subject.
    - **grade_level** (INT): Grade level of subject.
    - **created_at** (DATETIME): Datetime of subject creation.
    - **updated_at** (DATETIME): Datetime of subject updation.

    """
    print("Calling update_subject method")

    result: SubjectTable = await subject_view.update(
        db_session=db_session, record_id=subject_id, record=record
    )

    if not result:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": subject_response_message.SUBJECT_NOT_FOUND},
        )

    return SubjectReadSchema.model_validate(obj=result)


# Partial update a single subject route
@router.patch(
    path="/{subject_id}/",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Partial update a single subject by providing id",
    response_description="Subject updated successfully",
)
async def partial_update_subject(
    subject_id: int,
    record: SubjectPartialUpdateSchema,
    db_session: AsyncSession = Depends(get_session),
    current_user: CurrentUserReadSchema = Security(get_current_user),
) -> SubjectReadSchema:
    """
    Partial update a single subject.

    Description:
    - This route is used to partial update a single subject by providing id.

    Parameter:
    - **subject_id**: ID of subject to be updated. (INT) **(Required)**
    Subject details to be updated with following fields:
    - **subject_name**: Name of subject. (STR) **(Optional)**
    - **grade_level** (INT): Grade level of subject. **(Optional)**

    Return:
    Subject details along with following information:
    - **id** (INT): Id of subject.
    - **subject_name** (STR): Name of subject.
    - **grade_level** (INT): Grade level of subject.
    - **created_at** (DATETIME): Datetime of subject creation.
    - **updated_at** (DATETIME): Datetime of subject updation.

    """
    print("Calling partial_update_subject method")

    result: SubjectTable = await subject_view.update(
        db_session=db_session, record_id=subject_id, record=record
    )

    if not result:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": subject_response_message.SUBJECT_NOT_FOUND},
        )

    return SubjectReadSchema.model_validate(obj=result)


# Delete a single subject
@router.delete(
    path="/{grade_level}/",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete all subject by providing grade level",
    response_description="Subjects deleted successfully",
)
async def delete_subject_by_grade_level(
    grade_level: int,
    db_session: AsyncSession = Depends(get_session),
    current_user: CurrentUserReadSchema = Security(get_current_user),
) -> None:
    """
    Delete all subjects by grade level.

    Description:
    - This route is used to delete all subjects by providing grade level.

    Parameter:
    - **grade_level** (INT): Grade level of subjects to be deleted.
    **(Required)**

    Return:
    - **None**

    """
    print("Calling delete_subject_by_grade_level method")

    result: list = await subject_view.delete_by_grade_level(
        db_session=db_session, grade_level=grade_level
    )

    if not result:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": subject_response_message.SUBJECT_NOT_FOUND},
        )
