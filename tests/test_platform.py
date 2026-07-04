"""Tests for identity_os.platform — Platform core and session management."""

from __future__ import annotations

import uuid

import pytest

from identity_os.agents import Agent, AgentLifecycle
from identity_os.identity import Identity, IdentityKind
from identity_os.platform import Platform, Session


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _human(name: str = "Alice") -> Identity:
    return Identity(name=name, kind=IdentityKind.HUMAN)


def _agent(name: str = "bot", owner: Identity | None = None) -> Agent:
    return Agent(name=name, owner=owner or _human())


# ---------------------------------------------------------------------------
# Platform enrolment
# ---------------------------------------------------------------------------

class TestPlatformEnrolment:
    def test_enrol_human(self):
        platform = Platform()
        human = _human()
        platform.enrol(human)
        assert human in platform.identities

    def test_enrol_agent_activates_pending_agent(self):
        platform = Platform()
        agent = _agent()
        assert agent.lifecycle == AgentLifecycle.PENDING
        platform.enrol(_human())
        platform.enrol(agent)
        assert agent.lifecycle == AgentLifecycle.ACTIVE
        assert agent in platform.agents

    def test_enrol_duplicate_human_raises(self):
        platform = Platform()
        human = _human()
        platform.enrol(human)
        with pytest.raises(ValueError, match="already enrolled"):
            platform.enrol(human)

    def test_enrol_duplicate_agent_raises(self):
        platform = Platform()
        agent = _agent()
        platform.enrol(agent)
        with pytest.raises(ValueError, match="already enrolled"):
            platform.enrol(agent)

    def test_unenrol_human(self):
        platform = Platform()
        human = _human()
        platform.enrol(human)
        platform.unenrol(human)
        assert human not in platform.identities

    def test_unenrol_agent_revokes_it(self):
        platform = Platform()
        agent = _agent()
        platform.enrol(agent)
        platform.unenrol(agent)
        assert agent not in platform.agents
        assert agent.lifecycle == AgentLifecycle.REVOKED

    def test_unenrol_unknown_human_raises(self):
        platform = Platform()
        human = _human()
        with pytest.raises(KeyError, match="not enrolled"):
            platform.unenrol(human)

    def test_unenrol_unknown_agent_raises(self):
        platform = Platform()
        agent = _agent()
        with pytest.raises(KeyError, match="not enrolled"):
            platform.unenrol(agent)


# ---------------------------------------------------------------------------
# Session management
# ---------------------------------------------------------------------------

class TestSessions:
    def test_create_session_returns_session(self):
        platform = Platform()
        human = _human()
        agent = _agent(owner=human)
        session = platform.create_session(participants=[human, agent], goal="Test goal")
        assert isinstance(session, Session)
        assert session.goal == "Test goal"
        assert len(session.participants) == 2

    def test_session_is_registered_on_platform(self):
        platform = Platform()
        session = platform.create_session(participants=[_human()])
        assert session in platform.sessions

    def test_get_session_by_id(self):
        platform = Platform()
        session = platform.create_session(participants=[_human()])
        retrieved = platform.get_session(session.id)
        assert retrieved is session

    def test_get_session_unknown_id_raises(self):
        platform = Platform()
        with pytest.raises(KeyError, match="No session found"):
            platform.get_session(uuid.uuid4())

    def test_session_has_creation_event(self):
        platform = Platform()
        session = platform.create_session(participants=[_human()], goal="Hello")
        assert any(e["kind"] == "session_created" for e in session.events)

    def test_multiple_sessions_tracked(self):
        platform = Platform()
        human = _human()
        s1 = platform.create_session(participants=[human], goal="Task 1")
        s2 = platform.create_session(participants=[human], goal="Task 2")
        assert len(platform.sessions) == 2
        assert s1 in platform.sessions
        assert s2 in platform.sessions


# ---------------------------------------------------------------------------
# Session lifecycle
# ---------------------------------------------------------------------------

class TestSessionLifecycle:
    def test_session_is_active_initially(self):
        session = Session(participants=[_human()])
        assert session.is_active is True

    def test_close_session(self):
        session = Session(participants=[_human()])
        session.close()
        assert session.is_active is False
        assert session.ended_at is not None

    def test_close_already_closed_raises(self):
        session = Session(participants=[_human()])
        session.close()
        with pytest.raises(ValueError, match="already closed"):
            session.close()

    def test_log_event(self):
        session = Session(participants=[_human()])
        session.log_event("message_sent", {"content": "hello"})
        assert any(e["kind"] == "message_sent" for e in session.events)
        event = next(e for e in session.events if e["kind"] == "message_sent")
        assert event["data"]["content"] == "hello"
