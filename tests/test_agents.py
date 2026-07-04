"""Tests for identity_os.agents — Agentic AI collaboration layer."""

from __future__ import annotations

import pytest

from identity_os.agents import Agent, AgentLifecycle, Capability
from identity_os.identity import Identity, IdentityKind


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _human(name: str = "Alice") -> Identity:
    return Identity(name=name, kind=IdentityKind.HUMAN)


# ---------------------------------------------------------------------------
# AgentLifecycle transitions
# ---------------------------------------------------------------------------

class TestAgentLifecycle:
    def test_pending_can_activate(self):
        assert AgentLifecycle.PENDING.can_transition_to(AgentLifecycle.ACTIVE) is True

    def test_pending_can_revoke(self):
        assert AgentLifecycle.PENDING.can_transition_to(AgentLifecycle.REVOKED) is True

    def test_pending_cannot_suspend(self):
        assert AgentLifecycle.PENDING.can_transition_to(AgentLifecycle.SUSPENDED) is False

    def test_active_can_suspend(self):
        assert AgentLifecycle.ACTIVE.can_transition_to(AgentLifecycle.SUSPENDED) is True

    def test_active_can_revoke(self):
        assert AgentLifecycle.ACTIVE.can_transition_to(AgentLifecycle.REVOKED) is True

    def test_suspended_can_reactivate(self):
        assert AgentLifecycle.SUSPENDED.can_transition_to(AgentLifecycle.ACTIVE) is True

    def test_suspended_can_revoke(self):
        assert AgentLifecycle.SUSPENDED.can_transition_to(AgentLifecycle.REVOKED) is True

    def test_revoked_terminal(self):
        for target in AgentLifecycle:
            if target != AgentLifecycle.REVOKED:
                assert AgentLifecycle.REVOKED.can_transition_to(target) is False


# ---------------------------------------------------------------------------
# Agent
# ---------------------------------------------------------------------------

class TestAgent:
    def test_default_lifecycle_is_pending(self):
        agent = Agent(name="bot", owner=_human())
        assert agent.lifecycle == AgentLifecycle.PENDING

    def test_activate(self):
        agent = Agent(name="bot", owner=_human())
        agent.activate()
        assert agent.lifecycle == AgentLifecycle.ACTIVE

    def test_suspend(self):
        agent = Agent(name="bot", owner=_human())
        agent.activate()
        agent.suspend()
        assert agent.lifecycle == AgentLifecycle.SUSPENDED

    def test_reactivate_from_suspended(self):
        agent = Agent(name="bot", owner=_human())
        agent.activate()
        agent.suspend()
        agent.activate()
        assert agent.lifecycle == AgentLifecycle.ACTIVE

    def test_revoke(self):
        agent = Agent(name="bot", owner=_human())
        agent.activate()
        agent.revoke()
        assert agent.lifecycle == AgentLifecycle.REVOKED

    def test_invalid_transition_raises(self):
        agent = Agent(name="bot", owner=_human())
        with pytest.raises(ValueError, match="Cannot transition"):
            agent.suspend()  # PENDING → SUSPENDED is not allowed

    def test_identity_view_has_correct_kind(self):
        owner = _human()
        agent = Agent(name="research-bot", owner=owner)
        ident = agent.identity
        assert ident.kind == IdentityKind.AI_AGENT
        assert ident.id == agent.id
        assert ident.name == agent.name

    def test_identity_view_encodes_owner_id(self):
        owner = _human()
        agent = Agent(name="research-bot", owner=owner)
        assert agent.identity.metadata["owner_id"] == str(owner.id)


# ---------------------------------------------------------------------------
# Capability
# ---------------------------------------------------------------------------

class TestCapability:
    def test_grant_capability(self):
        owner = _human()
        agent = Agent(name="bot", owner=owner)
        agent.activate()
        cap = Capability(name="web_search", granted_by=owner)
        agent.grant_capability(cap)
        assert agent.has_capability("web_search") is True

    def test_has_capability_false_when_not_granted(self):
        agent = Agent(name="bot", owner=_human())
        assert agent.has_capability("file_write") is False

    def test_grant_capability_to_revoked_agent_raises(self):
        owner = _human()
        agent = Agent(name="bot", owner=owner)
        agent.activate()
        agent.revoke()
        cap = Capability(name="web_search", granted_by=owner)
        with pytest.raises(ValueError, match="revoked"):
            agent.grant_capability(cap)

    def test_multiple_capabilities(self):
        owner = _human()
        agent = Agent(name="bot", owner=owner)
        agent.activate()
        for cap_name in ["web_search", "file_read", "code_execute"]:
            agent.grant_capability(Capability(name=cap_name, granted_by=owner))
        assert len(agent.capabilities) == 3
        for cap_name in ["web_search", "file_read", "code_execute"]:
            assert agent.has_capability(cap_name) is True
