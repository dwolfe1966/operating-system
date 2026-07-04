"""Core identity primitives for the Identity Operating System."""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any


class IdentityKind(str, Enum):
    """The kind of an :class:`Identity`."""

    HUMAN = "human"
    ORGANISATION = "organisation"
    AI_AGENT = "ai_agent"
    SERVICE = "service"


@dataclass
class Credential:
    """A verifiable assertion about an :class:`Identity`.

    Examples include a verified email address, domain ownership, or
    organisational affiliation.

    Attributes:
        kind: Short label for the credential type (e.g. ``"email_verified"``).
        value: The asserted value (e.g. ``"alice@example.com"``).
        issued_at: When the credential was issued.
        expires_at: Optional expiry; ``None`` means the credential does not
            expire.
    """

    kind: str
    value: str
    issued_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    expires_at: datetime | None = None

    def is_valid(self, at: datetime | None = None) -> bool:
        """Return ``True`` if the credential is valid at *at* (default: now)."""
        now = at or datetime.now(timezone.utc)
        if self.expires_at is not None and now > self.expires_at:
            return False
        return True


@dataclass
class TrustAssertion:
    """A time-bounded, contextual trust statement.

    Expresses that *grantor* trusts *grantee* to perform *actions* within
    *context*.

    Attributes:
        grantor: The identity granting trust.
        grantee: The identity receiving trust.
        actions: A list of permitted action labels.
        context: Optional free-form context description.
        expires_at: When this assertion expires.
    """

    grantor: Identity
    grantee: Identity
    actions: list[str]
    context: str = ""
    expires_at: datetime | None = None

    def is_valid(self, at: datetime | None = None) -> bool:
        """Return ``True`` if the assertion is still valid at *at*."""
        now = at or datetime.now(timezone.utc)
        if self.expires_at is not None and now > self.expires_at:
            return False
        return True


@dataclass
class Identity:
    """The atomic unit of trust in the Identity Operating System.

    Attributes:
        name: Human-readable name.
        kind: What type of participant this identity represents.
        id: Globally unique identifier (auto-generated if not supplied).
        credentials: Verifiable assertions attached to this identity.
        created_at: When the identity was created.
        metadata: Arbitrary key/value metadata.
    """

    name: str
    kind: IdentityKind = IdentityKind.HUMAN
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    credentials: list[Credential] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: dict[str, Any] = field(default_factory=dict)

    # ------------------------------------------------------------------
    # Credentials
    # ------------------------------------------------------------------

    def add_credential(self, credential: Credential) -> None:
        """Attach *credential* to this identity."""
        self.credentials.append(credential)

    def valid_credentials(self, at: datetime | None = None) -> list[Credential]:
        """Return credentials that are currently valid."""
        return [c for c in self.credentials if c.is_valid(at=at)]

    # ------------------------------------------------------------------
    # Representation
    # ------------------------------------------------------------------

    def __repr__(self) -> str:  # pragma: no cover
        return f"Identity(id={self.id!s:.8}, name={self.name!r}, kind={self.kind.value})"
