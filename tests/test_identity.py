"""Tests for identity_os.identity — core Identity primitives."""

from __future__ import annotations

import uuid
from datetime import datetime, timedelta, timezone

import pytest

from identity_os.identity import Credential, Identity, IdentityKind, TrustAssertion


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


# ---------------------------------------------------------------------------
# Credential
# ---------------------------------------------------------------------------

class TestCredential:
    def test_valid_credential_no_expiry(self):
        cred = Credential(kind="email_verified", value="alice@example.com")
        assert cred.is_valid() is True

    def test_valid_credential_within_expiry(self):
        future = _utcnow() + timedelta(hours=1)
        cred = Credential(kind="email_verified", value="alice@example.com", expires_at=future)
        assert cred.is_valid() is True

    def test_expired_credential(self):
        past = _utcnow() - timedelta(seconds=1)
        cred = Credential(kind="email_verified", value="alice@example.com", expires_at=past)
        assert cred.is_valid() is False

    def test_is_valid_at_custom_time(self):
        expiry = _utcnow() + timedelta(hours=1)
        cred = Credential(kind="email_verified", value="alice@example.com", expires_at=expiry)
        # Check validity far in the future — should be False
        far_future = _utcnow() + timedelta(days=365)
        assert cred.is_valid(at=far_future) is False


# ---------------------------------------------------------------------------
# Identity
# ---------------------------------------------------------------------------

class TestIdentity:
    def test_default_kind_is_human(self):
        identity = Identity(name="Alice")
        assert identity.kind == IdentityKind.HUMAN

    def test_auto_generated_uuid(self):
        a = Identity(name="A")
        b = Identity(name="B")
        assert a.id != b.id
        assert isinstance(a.id, uuid.UUID)

    def test_explicit_kind(self):
        org = Identity(name="Acme Corp", kind=IdentityKind.ORGANISATION)
        assert org.kind == IdentityKind.ORGANISATION

    def test_add_credential(self):
        identity = Identity(name="Alice")
        cred = Credential(kind="email_verified", value="alice@example.com")
        identity.add_credential(cred)
        assert len(identity.credentials) == 1

    def test_valid_credentials_excludes_expired(self):
        identity = Identity(name="Alice")
        valid_cred = Credential(kind="email_verified", value="alice@example.com")
        expired_cred = Credential(
            kind="phone_verified",
            value="+1234",
            expires_at=_utcnow() - timedelta(seconds=1),
        )
        identity.add_credential(valid_cred)
        identity.add_credential(expired_cred)
        valid = identity.valid_credentials()
        assert valid_cred in valid
        assert expired_cred not in valid

    def test_metadata(self):
        identity = Identity(name="Alice", metadata={"department": "engineering"})
        assert identity.metadata["department"] == "engineering"

    def test_all_kinds_supported(self):
        for kind in IdentityKind:
            identity = Identity(name=f"test-{kind.value}", kind=kind)
            assert identity.kind == kind


# ---------------------------------------------------------------------------
# TrustAssertion
# ---------------------------------------------------------------------------

class TestTrustAssertion:
    def _make_pair(self):
        grantor = Identity(name="Alice")
        grantee = Identity(name="Bob")
        return grantor, grantee

    def test_valid_assertion_no_expiry(self):
        grantor, grantee = self._make_pair()
        assertion = TrustAssertion(grantor=grantor, grantee=grantee, actions=["read"])
        assert assertion.is_valid() is True

    def test_valid_assertion_within_expiry(self):
        grantor, grantee = self._make_pair()
        future = _utcnow() + timedelta(hours=1)
        assertion = TrustAssertion(
            grantor=grantor, grantee=grantee, actions=["read"], expires_at=future
        )
        assert assertion.is_valid() is True

    def test_expired_assertion(self):
        grantor, grantee = self._make_pair()
        past = _utcnow() - timedelta(seconds=1)
        assertion = TrustAssertion(
            grantor=grantor, grantee=grantee, actions=["write"], expires_at=past
        )
        assert assertion.is_valid() is False

    def test_assertion_stores_actions(self):
        grantor, grantee = self._make_pair()
        actions = ["read", "write", "execute"]
        assertion = TrustAssertion(grantor=grantor, grantee=grantee, actions=actions)
        assert assertion.actions == actions
