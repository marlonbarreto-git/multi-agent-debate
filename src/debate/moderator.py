"""Debate moderator - orchestrates multi-agent debates."""

from debate.agents import DebateAgent
from debate.models import Argument, DebateResult

DEFAULT_NUM_ROUNDS = 3


class DebateModerator:
    """Orchestrates a multi-agent debate over a configurable number of rounds."""

    def __init__(
        self,
        agents: list[DebateAgent],
        judge: DebateAgent,
        num_rounds: int = DEFAULT_NUM_ROUNDS,
    ) -> None:
        self.agents = agents
        self.judge = judge
        self.num_rounds = num_rounds

    def run_debate(self, topic: str) -> DebateResult:
        """Execute a full debate on the given topic.

        Args:
            topic: The subject to debate.

        Returns:
            A DebateResult with all rounds, votes, and the winner.
        """
        result = DebateResult(topic=topic)
        all_arguments: list[Argument] = []

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
