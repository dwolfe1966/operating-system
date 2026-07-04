"""Platform core — registry, session management, and orchestration."""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Union

from identity_os.agents import Agent, AgentLifecycle
from identity_os.identity import Identity


# A participant in a session can be a raw Identity or an Agent.
Participant = Union[Identity, Agent]


@dataclass
class Session:
    """A bounded collaboration context.

    A :class:`Session` records a set of participating identities (human and/or
    AI agents) collaborating toward a declared *goal*.  It tracks the
    participants, the start/end times, and a simple event log of noteworthy
    moments during the session.

    Attributes:
        participants: Identities participating in this session.
        goal: A human-readable description of what the session aims to achieve.
        id: Globally unique session identifier.
        started_at: When the session began.
        ended_at: When the session ended, or ``None`` if still active.
        events: Ordered log of session events.
    """

    participants: list[Participant]
    goal: str = ""
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    started_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    ended_at: datetime | None = None
    events: list[dict] = field(default_factory=list)

    # ------------------------------------------------------------------
    # Lifecycle helpers
    # ------------------------------------------------------------------

    @property
    def is_active(self) -> bool:
        """Return ``True`` if the session has not yet ended."""
        return self.ended_at is None

    def close(self) -> None:
        """Mark the session as ended."""
        if not self.is_active:
            raise ValueError(f"Session {self.id} is already closed.")
        self.ended_at = datetime.now(timezone.utc)
        self._log_event("session_closed")

    # ------------------------------------------------------------------
    # Event log
    # ------------------------------------------------------------------

    def log_event(self, kind: str, data: dict | None = None) -> None:
        """Append an event to the session log.

        Args:
            kind: Short label for the event (e.g. ``"message_sent"``).
            data: Optional extra data to store alongside the event.
        """
        self._log_event(kind, data)

    def _log_event(self, kind: str, data: dict | None = None) -> None:
        self.events.append(
            {
                "kind": kind,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "data": data or {},
            }
        )

    # ------------------------------------------------------------------
    # Representation
    # ------------------------------------------------------------------

    def __repr__(self) -> str:  # pragma: no cover
        status = "active" if self.is_active else "closed"
        return (
            f"Session(id={self.id!s:.8}, goal={self.goal!r}, "
            f"participants={len(self.participants)}, status={status})"
        )


class Platform:
    """The Identity Operating System platform.

    :class:`Platform` is the central orchestrator.  It maintains a registry of
    enrolled identities and agents, and provides factory methods for creating
    collaboration sessions.

    Example::

        platform = Platform()
        human = Identity(name="Alice", kind=IdentityKind.HUMAN)
        agent = Agent(name="helper", owner=human)

        platform.enrol(human)
        platform.enrol(agent)

        session = platform.create_session(
            participants=[human, agent],
            goal="Draft a product brief",
        )
    """

    def __init__(self) -> None:
        self._identities: dict[uuid.UUID, Identity] = {}
        self._agents: dict[uuid.UUID, Agent] = {}
        self._sessions: dict[uuid.UUID, Session] = {}

    # ------------------------------------------------------------------
    # Enrolment
    # ------------------------------------------------------------------

    def enrol(self, participant: Participant) -> None:
        """Register *participant* on the platform.

        An :class:`~identity_os.agents.Agent` is activated automatically
        when enrolled (transitioning it from ``PENDING`` → ``ACTIVE``).

        Args:
            participant: The identity or agent to enrol.

        Raises:
            ValueError: If the participant is already enrolled.
        """
        if isinstance(participant, Agent):
            if participant.id in self._agents:
                raise ValueError(
                    f"Agent {participant.name!r} is already enrolled."
                )
            if participant.lifecycle == AgentLifecycle.PENDING:
                participant.activate()
            self._agents[participant.id] = participant
        else:
            if participant.id in self._identities:
                raise ValueError(
                    f"Identity {participant.name!r} is already enrolled."
                )
            self._identities[participant.id] = participant

    def unenrol(self, participant: Participant) -> None:
        """Remove *participant* from the platform registry.

        Agents are revoked before being removed.

        Args:
            participant: The identity or agent to remove.

        Raises:
            KeyError: If the participant is not enrolled.
        """
        if isinstance(participant, Agent):
            if participant.id not in self._agents:
                raise KeyError(
                    f"Agent {participant.name!r} is not enrolled on this platform."
                )
            if participant.lifecycle != AgentLifecycle.REVOKED:
                participant.revoke()
            del self._agents[participant.id]
        else:
            if participant.id not in self._identities:
                raise KeyError(
                    f"Identity {participant.name!r} is not enrolled on this platform."
                )
            del self._identities[participant.id]

    # ------------------------------------------------------------------
    # Sessions
    # ------------------------------------------------------------------

    def create_session(
        self,
        participants: list[Participant],
        goal: str = "",
    ) -> Session:
        """Create and register a new :class:`Session`.

        Args:
            participants: Identities/agents that will participate.
            goal: Human-readable description of the session goal.

        Returns:
            The newly created :class:`Session`.
        """
        session = Session(participants=list(participants), goal=goal)
        self._sessions[session.id] = session
        session._log_event(
            "session_created",
            {
                "participants": [
                    str(p.id) for p in participants
                ],
                "goal": goal,
            },
        )
        return session

    def get_session(self, session_id: uuid.UUID) -> Session:
        """Return the :class:`Session` identified by *session_id*.

        Raises:
            KeyError: If no session with that ID exists.
        """
        try:
            return self._sessions[session_id]
        except KeyError:
            raise KeyError(f"No session found with id {session_id}.") from None

    # ------------------------------------------------------------------
    # Registry accessors
    # ------------------------------------------------------------------

    @property
    def identities(self) -> list[Identity]:
        """All enrolled human/org/service identities."""
        return list(self._identities.values())

    @property
    def agents(self) -> list[Agent]:
        """All enrolled AI agents."""
        return list(self._agents.values())

    @property
    def sessions(self) -> list[Session]:
        """All sessions (active and closed)."""
        return list(self._sessions.values())

    def __repr__(self) -> str:  # pragma: no cover
        return (
            f"Platform(identities={len(self._identities)}, "
            f"agents={len(self._agents)}, "
            f"sessions={len(self._sessions)})"
        )
