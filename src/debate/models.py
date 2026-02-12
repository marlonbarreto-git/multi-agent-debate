"""Debate data models - minimal stubs for moderator development."""

from enum import Enum

from pydantic import BaseModel, Field


class Role(str, Enum):
    """Roles that agents can assume during a debate."""

    PRO = "pro"
    CON = "con"
    JUDGE = "judge"


class Argument(BaseModel):
    """A single argument made by an agent in a debate round."""

    agent_name: str = Field(description="Name of the agent making the argument")
    role: Role = Field(description="Role of the agent (pro, con, or judge)")
    content: str = Field(description="Text content of the argument")
    round_num: int = Field(description="Debate round in which the argument was made")


class Vote(BaseModel):
    """A judge's vote declaring the winner of a debate."""

    voter: str = Field(description="Name of the voting agent")
    winner: str = Field(description="Name of the agent declared as winner")
    reason: str = Field(description="Justification for the vote")


class DebateResult(BaseModel):
    """Final result of a completed debate, including all rounds and votes."""

    topic: str = Field(description="The debate topic")
    rounds: list[list[Argument]] = Field(
        default_factory=list, description="Arguments grouped by round"
    )
    votes: list[Vote] = Field(
        default_factory=list, description="Votes cast by judges"
    )
    winner: str = Field(default="", description="Name of the debate winner")
    consensus: bool = Field(
        default=False, description="Whether all judges agreed on the winner"
    )
