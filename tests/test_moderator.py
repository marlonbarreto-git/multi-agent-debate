"""Tests for DebateModerator."""

from unittest.mock import MagicMock

from debate.agents import DebateAgent
from debate.models import Argument, DebateResult, Role, Vote
from debate.moderator import DebateModerator


def _make_agent(name: str, role: Role) -> MagicMock:
    agent = MagicMock(spec=DebateAgent)
    agent.name = name
    agent.role = role
    return agent


def _make_argument(agent_name: str, role: Role, round_num: int) -> Argument:
    return Argument(
        agent_name=agent_name,
        role=role,
        content=f"{agent_name} argument round {round_num}",
        round_num=round_num,
    )


def _make_vote(voter: str, winner: str) -> Vote:
    return Vote(voter=voter, winner=winner, reason="Good arguments")


class TestModeratorCreation:
    def test_moderator_creation(self):
        pro = _make_agent("pro_agent", Role.PRO)
        con = _make_agent("con_agent", Role.CON)
        judge = _make_agent("judge_agent", Role.JUDGE)

        moderator = DebateModerator(agents=[pro, con], judge=judge, num_rounds=5)

        assert moderator.agents == [pro, con]
        assert moderator.judge is judge
        assert moderator.num_rounds == 5


class TestRunDebate:
    def test_run_debate_correct_num_rounds(self):
        pro = _make_agent("pro_agent", Role.PRO)
        con = _make_agent("con_agent", Role.CON)
        judge = _make_agent("judge_agent", Role.JUDGE)

        pro.argue.side_effect = lambda topic, history, rn: _make_argument("pro_agent", Role.PRO, rn)
        con.argue.side_effect = lambda topic, history, rn: _make_argument("con_agent", Role.CON, rn)
        judge.vote.return_value = _make_vote("judge_agent", "pro_agent")

        moderator = DebateModerator(agents=[pro, con], judge=judge, num_rounds=2)
        result = moderator.run_debate("Test topic")

        assert len(result.rounds) == 2

    def test_run_debate_each_agent_argues_per_round(self):
        pro = _make_agent("pro_agent", Role.PRO)
        con = _make_agent("con_agent", Role.CON)
        judge = _make_agent("judge_agent", Role.JUDGE)

        pro.argue.side_effect = lambda topic, history, rn: _make_argument("pro_agent", Role.PRO, rn)
        con.argue.side_effect = lambda topic, history, rn: _make_argument("con_agent", Role.CON, rn)
        judge.vote.return_value = _make_vote("judge_agent", "pro_agent")

        moderator = DebateModerator(agents=[pro, con], judge=judge, num_rounds=3)
        moderator.run_debate("Test topic")

        assert pro.argue.call_count == 3
        assert con.argue.call_count == 3

    def test_run_debate_judge_votes(self):
        pro = _make_agent("pro_agent", Role.PRO)
        con = _make_agent("con_agent", Role.CON)
        judge = _make_agent("judge_agent", Role.JUDGE)

        pro.argue.side_effect = lambda topic, history, rn: _make_argument("pro_agent", Role.PRO, rn)
        con.argue.side_effect = lambda topic, history, rn: _make_argument("con_agent", Role.CON, rn)
        judge.vote.return_value = _make_vote("judge_agent", "con_agent")

        moderator = DebateModerator(agents=[pro, con], judge=judge, num_rounds=2)
        result = moderator.run_debate("Test topic")

        judge.vote.assert_called_once()
        assert result.winner == "con_agent"

    def test_run_debate_history_grows(self):
        pro = _make_agent("pro_agent", Role.PRO)
        con = _make_agent("con_agent", Role.CON)
        judge = _make_agent("judge_agent", Role.JUDGE)

        call_histories: list[list] = []

        def track_argue(agent_name, role):
            def _argue(topic, history, rn):
                call_histories.append(list(history))
                return _make_argument(agent_name, role, rn)
            return _argue

        pro.argue.side_effect = track_argue("pro_agent", Role.PRO)
        con.argue.side_effect = track_argue("con_agent", Role.CON)
        judge.vote.return_value = _make_vote("judge_agent", "pro_agent")

        moderator = DebateModerator(agents=[pro, con], judge=judge, num_rounds=2)
        moderator.run_debate("Test topic")

        # Round 1: pro gets empty history, con gets 1 arg (pro's)
        assert len(call_histories[0]) == 0  # pro round 1
        assert len(call_histories[1]) == 1  # con round 1
        # Round 2: pro gets 2 args (round 1), con gets 3 args
        assert len(call_histories[2]) == 2  # pro round 2
        assert len(call_histories[3]) == 3  # con round 2

    def test_run_debate_returns_complete_result(self):
        pro = _make_agent("pro_agent", Role.PRO)
        con = _make_agent("con_agent", Role.CON)
        judge = _make_agent("judge_agent", Role.JUDGE)

        pro.argue.side_effect = lambda topic, history, rn: _make_argument("pro_agent", Role.PRO, rn)
        con.argue.side_effect = lambda topic, history, rn: _make_argument("con_agent", Role.CON, rn)
        judge.vote.return_value = _make_vote("judge_agent", "pro_agent")

        moderator = DebateModerator(agents=[pro, con], judge=judge, num_rounds=2)
        result = moderator.run_debate("AI is beneficial")

        assert isinstance(result, DebateResult)
        assert result.topic == "AI is beneficial"
        assert len(result.rounds) == 2
        assert all(len(r) == 2 for r in result.rounds)
        assert len(result.votes) == 1
        assert result.winner == "pro_agent"

    def test_consensus_when_all_votes_same(self):
        pro = _make_agent("pro_agent", Role.PRO)
        con = _make_agent("con_agent", Role.CON)
        judge = _make_agent("judge_agent", Role.JUDGE)

        pro.argue.side_effect = lambda topic, history, rn: _make_argument("pro_agent", Role.PRO, rn)
        con.argue.side_effect = lambda topic, history, rn: _make_argument("con_agent", Role.CON, rn)
        judge.vote.return_value = _make_vote("judge_agent", "pro_agent")

        moderator = DebateModerator(agents=[pro, con], judge=judge, num_rounds=2)
        result = moderator.run_debate("Test topic")

        # Single judge always produces consensus
        assert result.consensus is True
