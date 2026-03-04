"""Package-level imports for the application's ORM models.

This module gathers all significant model classes in one place so that callers can
import directly from ``app.models`` rather than drilling into individual files.
It also ensures that the package is recognized as a regular package instead of a
namespace package, which helps avoid subtle import issues during live
reloading.
"""

from .cohort import Cohort, Trainee, CohortStatus
from .progress import Progress, Attendance, ProgressLog
from .user import User
from .session import Session as SessionModel, SessionAttendee, MoM, SessionType
# other model imports can be added here when needed

__all__ = [
    "Cohort", "Trainee", "CohortStatus",
    "Progress", "Attendance", "ProgressLog",
    "User",
    "SessionModel", "SessionAttendee", "MoM", "SessionType",
]
