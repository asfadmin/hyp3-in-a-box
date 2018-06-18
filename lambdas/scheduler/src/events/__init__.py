"""
This module is to give communication between the hyp3 system functions some
amount of type safety.
"""

from .make import make_notify_events
from .send import send

__all__ = ['make_notify_events', 'send']
