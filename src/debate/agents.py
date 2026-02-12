"""Debate agents."""

from typing import Callable, Optional

from debate.models import Argument, Role, Vote

VOTE_RESPONSE_MAX_PARTS = 2


class DebateAgent:
    """An agent that participates in debates by arguing and voting."""

    def __init__(
        self,
        name: str,
        role: Role,
        llm_fn: Optional[Callable[[str], str]] = None,
    ) -> None:
        self.name = name
        self.role = role
        self._llm_fn = llm_fn or self._default_respond

    def argue(
        self, topic: str, history: list[Argument], round_num: int
    ) -> Argument:
        """Generate an argument for the given topic and round.

        Args:
            topic: The debate topic.
            history: All arguments made so far.
            round_num: Current round number.

        Returns:
            An Argument with the agent's response.
        """
        prompt = self._build_prompt(topic, history, round_num)
        content = self._llm_fn(prompt)
        return Argument(
            agent_name=self.name,
            role=self.role,
            content=content,
            round_num=round_num,
        )

    def vote(self, topic: str, history: list[Argument]) -> Vote:
        """Cast a vote for the debate winner based on the argument history.

        Args:
            topic: The debate topic.
            history: All arguments from the debate.

        Returns:
            A Vote declaring the winner and reasoning.
        """
        prompt = self._build_vote_prompt(topic, history)
        response = self._llm_fn(prompt)
        lines = response.strip().split("\n", 1)
        winner = lines[0].strip()
        reason = lines[1].strip() if len(lines) > 1 else ""
        return Vote(voter=self.name, winner=winner, reason=reason)

    def _build_prompt(
        self, topic: str, history: list[Argument], round_num: int
    ) -> str:
        hist = "\n".join(f"[{a.agent_name}] {a.content}" for a in history)
        return f"Topic: {topic}\nYour role: {self.role.value}\nHistory:\n{hist}\nRound {round_num}: Make your argument."

    def _build_vote_prompt(
        self, topic: str, history: list[Argument]
    ) -> str:
        hist = "\n".join(f"[{a.agent_name}] {a.content}" for a in history)
        return f"Topic: {topic}\nDebate:\n{hist}\nWho won? First line: winner name. Second line: reason."

    @staticmethod
    def _default_respond(prompt: str) -> str:
        return "Default argument."
