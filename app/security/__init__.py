"""Security module for lavs API.

Provides API key authentication for protecting routes.
"""

from app.security.api_key import (
    API_KEY_ENV_VAR,
    API_KEY_HEADER,
    ApiKeyDep,
    get_api_key,
    get_configured_api_key,
    is_authentication_enabled,
)

__all__ = [
    "API_KEY_ENV_VAR",
    "API_KEY_HEADER",
    "ApiKeyDep",
    "get_api_key",
    "get_configured_api_key",
    "is_authentication_enabled",
]
