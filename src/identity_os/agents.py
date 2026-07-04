"""Agentic AI collaboration layer for the Identity Operating System."""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any

from identity_os.identity import Identity, IdentityKind


class AgentLifecycle(str, Enum):
    """State machine for an :class:`Agent`.

    Allowed transitions::

        PENDING → ACTIVE → SUSPENDED → ACTIVE
                         → REVOKED  (terminal)
    """

    PENDING = "pending"
    ACTIVE = "active"
    SUSPENDED = "suspended"
    REVOKED = "revoked"

    # Valid forward transitions
    _TRANSITIONS: dict[str, list[str]] = {}  # populated below

    def can_transition_to(self, target: AgentLifecycle) -> bool:
        """Return ``True`` if transitioning from *self* to *target* is allowed."""
        allowed: dict[AgentLifecycle, list[AgentLifecycle]] = {
            AgentLifecycle.PENDING: [AgentLifecycle.ACTIVE, AgentLifecycle.REVOKED],
            AgentLifecycle.ACTIVE: [AgentLifecycle.SUSPENDED, AgentLifecycle.REVOKED],
            AgentLifecycle.SUSPENDED: [AgentLifecycle.ACTIVE, AgentLifecycle.REVOKED],
            AgentLifecycle.REVOKED: [],
        }
        return target in allowed.get(self, [])


@dataclass
class Capability:
    """A declared action or resource scope an agent is designed to exercise.

    Capabilities must be explicitly granted by the owning human identity before
    the agent may exercise them.

    Attributes:
        name: Short label, e.g. ``"web_search"`` or ``"file_read"``.
        description: Human-readable explanation of what the capability does.
        granted_by: The identity that authorised this capability.
        granted_at: When the grant occurred.
    """

    name: str
    description: str = ""
    granted_by: Identity | None = None
    granted_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class Agent:
    """An AI agent identity.

    An :class:`Agent` is an :class:`~identity_os.identity.Identity` of kind
    :attr:`~identity_os.identity.IdentityKind.AI_AGENT`.  It carries extra
    metadata about its model provider, its owning human identity, and the
    capabilities it is permitted to exercise.

    Attributes:
        name: Human-readable name for the agent.
        owner: The :class:`~identity_os.identity.Identity` (typically a human)
            who registered and is responsible for this agent.
        model_provider: The AI model provider powering this agent
            (e.g. ``"openai"``, ``"anthropic"``).
        capabilities: Capabilities that have been granted to this agent.
        lifecycle: Current lifecycle state.
        id: Globally unique identifier (auto-generated if not supplied).
        created_at: When the agent was registered.
        metadata: Arbitrary key/value metadata.
    """

    name: str
    owner: Identity
    model_provider: str = "unknown"
    capabilities: list[Capability] = field(default_factory=list)
    lifecycle: AgentLifecycle = AgentLifecycle.PENDING
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: dict[str, Any] = field(default_factory=dict)

    # ------------------------------------------------------------------
    # Identity bridge
    # ------------------------------------------------------------------

    @property
    def identity(self) -> Identity:
        """Return an :class:`~identity_os.identity.Identity` view of this agent."""
        return Identity(
            name=self.name,
            kind=IdentityKind.AI_AGENT,
            id=self.id,
            created_at=self.created_at,
            metadata={"owner_id": str(self.owner.id), **self.metadata},
        )

    # ------------------------------------------------------------------
    # Lifecycle management
    # ------------------------------------------------------------------

    def activate(self) -> None:
        """Transition the agent to :attr:`AgentLifecycle.ACTIVE`."""
        self._transition(AgentLifecycle.ACTIVE)

    def suspend(self) -> None:
        """Transition the agent to :attr:`AgentLifecycle.SUSPENDED`."""
        self._transition(AgentLifecycle.SUSPENDED)

    def revoke(self) -> None:
        """Permanently transition the agent to :attr:`AgentLifecycle.REVOKED`."""
        self._transition(AgentLifecycle.REVOKED)

    def _transition(self, target: AgentLifecycle) -> None:
        if not self.lifecycle.can_transition_to(target):
            raise ValueError(
                f"Cannot transition agent {self.name!r} from "
                f"{self.lifecycle.value!r} to {target.value!r}."
            )
        self.lifecycle = target

    # ------------------------------------------------------------------
    # Capabilities
    # ------------------------------------------------------------------

    def grant_capability(self, capability: Capability) -> None:
        """Grant *capability* to this agent.

        Raises:
            ValueError: If the agent has been revoked.
        """
        if self.lifecycle == AgentLifecycle.REVOKED:
            raise ValueError(
                f"Cannot grant capabilities to revoked agent {self.name!r}."
            )
        self.capabilities.append(capability)

    def has_capability(self, name: str) -> bool:
        """Return ``True`` if the agent holds a capability with *name*."""
        return any(c.name == name for c in self.capabilities)

    # ------------------------------------------------------------------
    # Representation
    # ------------------------------------------------------------------

    def __repr__(self) -> str:  # pragma: no cover
        return (
            f"Agent(id={self.id!s:.8}, name={self.name!r}, "
            f"owner={self.owner.name!r}, lifecycle={self.lifecycle.value})"
        )
