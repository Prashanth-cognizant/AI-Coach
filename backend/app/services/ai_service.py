"""Backward-compatible wrapper for the ai_service_v2 implementation.

Several modules previously imported from :mod:`app.services.ai_service`.
With the migration to ``ai_service_v2.py`` this module allows existing imports to continue
working by simply re-exporting the public API from the new file.
"""

from .ai_service_v2 import generate_mom, summarize_cohort_progress, generate_document

# expose the class as well if someone wants it
from .ai_service_v2 import AIService

__all__ = [
    "generate_mom",
    "summarize_cohort_progress",
    "generate_document",
    "AIService",
]
