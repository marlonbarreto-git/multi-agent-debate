from debate.models import Argument, DebateResult, Role, Vote


def test_role_enum_values():
    assert Role.PRO.value == "pro"
    assert Role.CON.value == "con"
    assert Role.JUDGE.value == "judge"


def test_argument_creation():
    arg = Argument(agent_name="Alice", role=Role.PRO, content="I agree", round_num=1)
    assert arg.agent_name == "Alice"
    assert arg.role == Role.PRO
    assert arg.content == "I agree"
    assert arg.round_num == 1


def test_vote_creation():
    vote = Vote(voter="Judge1", winner="Alice", reason="Better evidence")
    assert vote.voter == "Judge1"
    assert vote.winner == "Alice"
    assert vote.reason == "Better evidence"


def test_debate_result_defaults():
    result = DebateResult(topic="AI safety")
    assert result.topic == "AI safety"
    assert result.rounds == []
    assert result.votes == []
    assert result.winner == ""
    assert result.consensus is False


def test_debate_result_with_data():
    arg1 = Argument(agent_name="Alice", role=Role.PRO, content="Pro point", round_num=1)
    arg2 = Argument(agent_name="Bob", role=Role.CON, content="Con point", round_num=1)
    vote = Vote(voter="Judge1", winner="Alice", reason="Stronger arguments")

    result = DebateResult(
        topic="Climate policy",
        rounds=[[arg1, arg2]],
        votes=[vote],
        winner="Alice",
        consensus=True,
    )
    assert result.topic == "Climate policy"
    assert len(result.rounds) == 1
    assert len(result.rounds[0]) == 2
    assert result.rounds[0][0].agent_name == "Alice"
    assert result.votes[0].winner == "Alice"
    assert result.winner == "Alice"
    assert result.consensus is True
