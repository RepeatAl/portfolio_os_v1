"""Typed actor identity model for governance audit trail attribution.

Provides formal typing for mutation actors so that audit ledger entries
clearly identify who or what performed each change. Supports environment
detection, factory methods for common actor types, and round-trip
serialization to/from dict for YAML persistence.

Requirements: 33.1, 33.2, 33.3, 33.4, 33.5, 33.6
"""

from __future__ import annotations

import os
import subprocess
from dataclasses import dataclass, field
from enum import StrEnum


class ActorType(StrEnum):
    """Classification of the entity performing a governance mutation.

    Each actor type represents a distinct source of changes in the system:
    - SYSTEM: Internal governance operations with no specific human trigger
    - CI: GitHub Actions or other CI pipeline operations
    - USER: Human-initiated changes (git commits, manual edits)
    - ENGINE: Pipeline engine artifact production
    - MIGRATION: Schema or data migration operations
    - RUNTIME: Runtime system operations (state model, orchestrator)
    - HOT_RELOAD: Live configuration reload during execution
    """

    SYSTEM = "SYSTEM"
    CI = "CI"
    USER = "USER"
    ENGINE = "ENGINE"
    MIGRATION = "MIGRATION"
    RUNTIME = "RUNTIME"
    HOT_RELOAD = "HOT_RELOAD"


@dataclass
class ActorIdentity:
    """Structured identity for audit trail attribution.

    Attributes:
        actor_type: The classification of this actor.
        actor_id: A human-readable identifier for the specific actor instance.
        context: Optional key-value metadata providing additional attribution
                 details (e.g., git_author, commit_sha, workflow_run_id).
        is_fallback: True when identity could not be fully resolved and a
                     fallback was used. Flags entries for later identity
                     resolution.
    """

    actor_type: ActorType
    actor_id: str
    context: dict = field(default_factory=dict)
    is_fallback: bool = False

    @classmethod
    def from_environment(cls) -> ActorIdentity:
        """Detect actor identity from the current environment.

        Resolution priority:
        1. CI environment (GITHUB_ACTIONS or CI env var) -> CI actor
        2. Git user info (git config user.name/email) -> USER actor
        3. $USER environment variable -> USER actor with is_fallback=True
        4. Final fallback -> SYSTEM actor with is_fallback=True
        """
        # Priority 1: CI environment detection
        if os.environ.get("GITHUB_ACTIONS") == "true" or os.environ.get("CI") == "true":
            workflow_run_id = os.environ.get("GITHUB_RUN_ID", "unknown_run")
            context = {}
            if os.environ.get("GITHUB_WORKFLOW"):
                context["workflow"] = os.environ["GITHUB_WORKFLOW"]
            if os.environ.get("GITHUB_SHA"):
                context["commit_sha"] = os.environ["GITHUB_SHA"]
            if os.environ.get("GITHUB_REF"):
                context["ref"] = os.environ["GITHUB_REF"]
            if os.environ.get("GITHUB_ACTOR"):
                context["github_actor"] = os.environ["GITHUB_ACTOR"]
            return cls(
                actor_type=ActorType.CI,
                actor_id=workflow_run_id,
                context=context,
                is_fallback=False,
            )

        # Priority 2: Git user info
        git_user = _get_git_user_info()
        if git_user is not None:
            name, email = git_user
            actor_id = name if name else email
            context = {}
            if name and email:
                context["git_author"] = f"{name} <{email}>"
            elif email:
                context["git_author"] = email
            return cls(
                actor_type=ActorType.USER,
                actor_id=actor_id,
                context=context,
                is_fallback=False,
            )

        # Priority 3: $USER environment variable
        env_user = os.environ.get("USER") or os.environ.get("USERNAME")
        if env_user:
            return cls(
                actor_type=ActorType.USER,
                actor_id=env_user,
                context={},
                is_fallback=True,
            )

        # Priority 4: Final fallback
        return cls(
            actor_type=ActorType.SYSTEM,
            actor_id="unknown_actor",
            context={},
            is_fallback=True,
        )

    @classmethod
    def ci_actor(cls, workflow_run_id: str) -> ActorIdentity:
        """Create a CI actor identity for a specific workflow run.

        Args:
            workflow_run_id: The CI workflow run identifier (e.g., GitHub run ID).
        """
        return cls(
            actor_type=ActorType.CI,
            actor_id=workflow_run_id,
            context={},
            is_fallback=False,
        )

    @classmethod
    def engine_actor(cls, engine_id: str) -> ActorIdentity:
        """Create an ENGINE actor identity for a pipeline engine.

        Args:
            engine_id: The engine identifier (e.g., "allocation_engine",
                       "report_engine").
        """
        return cls(
            actor_type=ActorType.ENGINE,
            actor_id=engine_id,
            context={},
            is_fallback=False,
        )

    def to_dict(self) -> dict:
        """Serialize to a dict suitable for YAML persistence.

        Returns:
            A dictionary with keys: actor_type, actor_id, context, is_fallback.
        """
        return {
            "actor_type": str(self.actor_type),
            "actor_id": self.actor_id,
            "context": dict(self.context),
            "is_fallback": self.is_fallback,
        }

    @classmethod
    def from_dict(cls, data: dict) -> ActorIdentity:
        """Deserialize from a dict (e.g., loaded from YAML).

        Args:
            data: Dictionary with keys actor_type, actor_id, and optionally
                  context and is_fallback.

        Returns:
            An ActorIdentity instance.

        Raises:
            ValueError: If actor_type is not a valid ActorType value.
            KeyError: If required keys (actor_type, actor_id) are missing.
        """
        actor_type = ActorType(data["actor_type"])
        actor_id = data["actor_id"]
        context = dict(data.get("context", {}))
        is_fallback = bool(data.get("is_fallback", False))
        return cls(
            actor_type=actor_type,
            actor_id=actor_id,
            context=context,
            is_fallback=is_fallback,
        )


def _get_git_user_info() -> tuple[str, str] | None:
    """Attempt to retrieve git user.name and user.email from git config.

    Returns:
        A tuple of (name, email) if at least one is available, or None
        if git is not available or no user info is configured.
    """
    try:
        name = subprocess.run(
            ["git", "config", "user.name"],
            capture_output=True,
            text=True,
            timeout=5,
        ).stdout.strip()

        email = subprocess.run(
            ["git", "config", "user.email"],
            capture_output=True,
            text=True,
            timeout=5,
        ).stdout.strip()

        if name or email:
            return (name, email)
        return None
    except (subprocess.SubprocessError, FileNotFoundError, OSError):
        return None
