# Multi-Agent Debate

System where multiple agents debate a topic from different perspectives, with voting and consensus detection.

## Overview

Multi-Agent Debate implements a structured argumentation system where agents with assigned roles (pro, con, judge) debate a topic over multiple rounds. Each agent builds arguments informed by the full debate history, and a judge agent votes on the winner after all rounds complete. The moderator orchestrates the debate flow and detects consensus among judges.

## Architecture

```
Topic
  |
  v
+-------------------+
| DebateModerator   |
| (round control,   |
|  vote collection, |
|  consensus check) |
+-------------------+
  |           |
  v           v
+--------+ +--------+
| Agent  | | Agent  |
| (PRO)  | | (CON)  |
+--------+ +--------+
  |           |
  v           v
Arguments (per round)
       |
       v
+--------+
| Judge  |
| (vote) |
+--------+
       |
       v
  DebateResult
  (rounds, votes, winner, consensus)
```

## Features

- Role-based agents (pro, con, judge)
- Multi-round debate with configurable round count
- Full debate history passed to each agent
- Judge voting with winner selection and reasoning
- Consensus detection across multiple judges
- Pluggable LLM function per agent
- Pydantic models for type-safe data flow

## Tech Stack

- Python 3.11+
- Pydantic (data validation and models)

## Quick Start

```bash
git clone https://github.com/marlonbarreto-git/multi-agent-debate.git
cd multi-agent-debate
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pytest
```

## Project Structure

```
src/debate/
  __init__.py
  models.py      # Role, Argument, Vote, DebateResult
  agents.py      # DebateAgent with argue and vote methods
  moderator.py   # DebateModerator orchestrator
tests/
  test_models.py
  test_agents.py
  test_moderator.py
```

## Testing

```bash
pytest -v --cov=src/debate
```

19 tests covering data models, agent argumentation, voting logic, and moderator orchestration.

## License

MIT
