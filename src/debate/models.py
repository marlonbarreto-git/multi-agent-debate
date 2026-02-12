"""Debate data models - minimal stubs for moderator development."""

from enum import Enum

from pydantic import BaseModel, Field


class Role(str, Enum):
    PRO = "pro"
    CON = "con"
    JUDGE = "judge"


class Argument(BaseModel):
    agent_name: str
    role: Role
    content: str
    round_num: int


class Vote(BaseModel):
    voter: str
    winner: str
    reason: str


class DebateResult(BaseModel):
    topic: str
    rounds: list[list[Argument]] = Field(default_factory=list)
    votes: list[Vote] = Field(default_factory=list)
    winner: str = ""
    consensus: bool = False
