"""Debate agents."""

from debate.models import Argument, Role, Vote


class DebateAgent:
    def __init__(self, name: str, role: Role, llm_fn=None):
        self.name = name
        self.role = role
        self._llm_fn = llm_fn or self._default_respond

    def argue(self, topic: str, history: list[Argument], round_num: int) -> Argument:
        prompt = self._build_prompt(topic, history, round_num)
        content = self._llm_fn(prompt)
        return Argument(agent_name=self.name, role=self.role, content=content, round_num=round_num)

    def vote(self, topic: str, history: list[Argument]) -> Vote:
        prompt = self._build_vote_prompt(topic, history)
        response = self._llm_fn(prompt)
        lines = response.strip().split("\n", 1)
        winner = lines[0].strip()
        reason = lines[1].strip() if len(lines) > 1 else ""
        return Vote(voter=self.name, winner=winner, reason=reason)

    def _build_prompt(self, topic, history, round_num):
        hist = "\n".join(f"[{a.agent_name}] {a.content}" for a in history)
        return f"Topic: {topic}\nYour role: {self.role.value}\nHistory:\n{hist}\nRound {round_num}: Make your argument."

    def _build_vote_prompt(self, topic, history):
        hist = "\n".join(f"[{a.agent_name}] {a.content}" for a in history)
        return f"Topic: {topic}\nDebate:\n{hist}\nWho won? First line: winner name. Second line: reason."

    @staticmethod
    def _default_respond(prompt: str) -> str:
        return "Default argument."
