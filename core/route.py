"""
    FastAPI Route module

    Description:
    - This module is used to create main route for application.

"""

# Importing Python Packages

# Importing FastAPI Packages
from fastapi import APIRouter

# Importing Project Files
from apps.auth.route import router as auth_router
from apps.organization.route import router as organization_router
from apps.role.route import router as role_router
from apps.subject.route import router as subject_router
from apps.user.route import router as user_router


# Router Object to Create Routes
router = APIRouter()


# -----------------------------------------------------------------------------


# Include all file routes
router.include_router(organization_router)
router.include_router(role_router)
router.include_router(subject_router)
router.include_router(user_router)
router.include_router(auth_router)
