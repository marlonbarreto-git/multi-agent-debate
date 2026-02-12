"""Multi-Agent Debate System."""

__all__ = [
    "Argument",
    "DebateAgent",
    "DebateModerator",
    "DebateResult",
    "Role",
    "Vote",
]

from .agents import DebateAgent
from .models import Argument, DebateResult, Role, Vote
from .moderator import DebateModerator
