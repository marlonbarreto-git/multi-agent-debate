from debate.agents import DebateAgent
from debate.models import Argument, Role


def test_agent_creation():
    agent = DebateAgent(name="Alice", role=Role.PRO)
    assert agent.name == "Alice"
    assert agent.role == Role.PRO


def test_argue_returns_argument():
    def mock_llm(prompt):
        return "My argument"
    agent = DebateAgent(name="Alice", role=Role.PRO, llm_fn=mock_llm)
    result = agent.argue(topic="AI safety", history=[], round_num=1)
    assert isinstance(result, Argument)
    assert result.agent_name == "Alice"
    assert result.role == Role.PRO
    assert result.content == "My argument"
    assert result.round_num == 1


def test_argue_includes_history_in_prompt():
    captured = {}

    def mock_llm(prompt):
        captured["prompt"] = prompt
        return "response"

    history = [
        Argument(agent_name="Bob", role=Role.CON, content="I disagree", round_num=1),
    ]
    agent = DebateAgent(name="Alice", role=Role.PRO, llm_fn=mock_llm)
    agent.argue(topic="AI safety", history=history, round_num=2)
    assert "[Bob] I disagree" in captured["prompt"]


def test_argue_correct_round_num():
    def mock_llm(prompt):
        return "Round 3 arg"
    agent = DebateAgent(name="Alice", role=Role.PRO, llm_fn=mock_llm)
    result = agent.argue(topic="AI safety", history=[], round_num=3)
    assert result.round_num == 3


def test_vote_returns_vote():
    def mock_llm(prompt):
        return "Alice\nBetter points"
    agent = DebateAgent(name="Judge1", role=Role.JUDGE, llm_fn=mock_llm)
    vote = agent.vote(topic="AI safety", history=[])
    assert vote.voter == "Judge1"
    assert vote.winner == "Alice"
    assert vote.reason == "Better points"


def test_vote_no_reason():
    def mock_llm(prompt):
        return "Bob"
    agent = DebateAgent(name="Judge1", role=Role.JUDGE, llm_fn=mock_llm)
    vote = agent.vote(topic="AI safety", history=[])
    assert vote.voter == "Judge1"
    assert vote.winner == "Bob"
    assert vote.reason == ""


def test_default_respond():
    agent = DebateAgent(name="Alice", role=Role.PRO)
    result = agent.argue(topic="AI safety", history=[], round_num=1)
    assert result.content == "Default argument."
