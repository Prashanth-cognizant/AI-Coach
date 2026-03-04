"""Central import point for API route modules.

Importing here ensures that ``from app.routes import xyz`` works and avoids
import errors during hot reload while also keeping the modules in a
consistent namespace.

Each submodule should define a ``router`` object.
"""

from . import auth
from . import sessions
from . import progress
from . import chat
from . import cohorts
from . import evaluations
from . import documents
from . import progress_tracking
from . import reminders
from . import mentoring
from . import support
from . import compliance

__all__ = [
    "auth", "sessions", "progress", "chat", "cohorts", "evaluations",
    "documents", "progress_tracking", "reminders", "mentoring", "support",
    "compliance",
]
