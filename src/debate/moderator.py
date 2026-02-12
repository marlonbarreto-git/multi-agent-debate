"""Debate moderator - orchestrates multi-agent debates."""

from debate.agents import DebateAgent
from debate.models import DebateResult


class DebateModerator:
    def __init__(self, agents: list[DebateAgent], judge: DebateAgent, num_rounds: int = 3) -> None:
        self.agents = agents
        self.judge = judge
        self.num_rounds = num_rounds

    def run_debate(self, topic: str) -> DebateResult:
        result = DebateResult(topic=topic)
        all_arguments = []

        for round_num in range(1, self.num_rounds + 1):
            round_args = []
            for agent in self.agents:
                arg = agent.argue(topic, all_arguments, round_num)
                round_args.append(arg)
                all_arguments.append(arg)
            result.rounds.append(round_args)

        vote = self.judge.vote(topic, all_arguments)
        result.votes.append(vote)
        result.winner = vote.winner

        result.consensus = len(set(v.winner for v in result.votes)) == 1

        return result
