"""
    Base Configuration Module

    Description:
    - This module is responsible for base routes configuration.

"""

# Importing Python Packages
from datetime import datetime

# Importing FastAPI Packages

# Importing Project Files


# -----------------------------------------------------------------------------


class BaseConfiguration:
    """
    Base Settings Class

    Description:
    - This class is used to define base configurations.

    """

    ID: int = 1
    CREATED_AT: datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    UPDATED_AT: datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    TOTAL_RECORDS: int = 1
    PAGE: int = 1
    LIMIT: int = 10


base_configuration = BaseConfiguration()
