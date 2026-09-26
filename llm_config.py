"""Model access configuration: every model goes through an OpenAI-compatible chat
completions interface.

The code has only two kinds of model call: a text-only LLM and an image-understanding VLM.
The text LLM is further split by role into two sets of credentials, for the agent under test
and the user simulator, so the two can point at different providers. Each set of credentials
is three variables, BASE_URL + API_KEY + MODEL, corresponding to one section of .env.example.
"""

import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()

# role -> .env variable prefix
ROLE_ENV_PREFIXES = {
    "agent": "AGENT_LLM",
    "user": "USER_LLM",
    "vlm": "VLM",
}


@dataclass(frozen=True)
class LLMConfig:
    base_url: str
    api_key: str
    model: str


def resolve_model_name(role: str, model: str = "") -> str:
    """Return the model id this role actually uses; an explicitly passed model wins over the
    .env default."""
    return model or os.getenv(f"{_prefix(role)}_MODEL", "")


def get_llm_config(role: str, model: str = "") -> LLMConfig:
    """Read a role's access configuration, erroring immediately on a missing variable rather
    than waiting for the API to return 401."""
    prefix = _prefix(role)
    config = LLMConfig(
        base_url=os.getenv(f"{prefix}_BASE_URL", ""),
        api_key=os.getenv(f"{prefix}_API_KEY", ""),
        model=resolve_model_name(role, model),
    )
    missing = [
        f"{prefix}_{name}"
        for name, value in (
            ("BASE_URL", config.base_url),
            ("API_KEY", config.api_key),
            ("MODEL", config.model),
        )
        if not value
    ]
    if missing:
        raise ValueError(
            f"missing environment variables {', '.join(missing)}; please fill in .env following .env.example."
        )
    return config


def _prefix(role: str) -> str:
    try:
        return ROLE_ENV_PREFIXES[role]
    except KeyError:
        raise ValueError(
            f"unknown model role {role!r}, available: {sorted(ROLE_ENV_PREFIXES)}"
        ) from None
