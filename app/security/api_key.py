"""API key authentication module for lavs API.

This module provides API key-based authentication for protecting routes.
It supports optional authentication - when no API key is configured,
all requests are allowed through.
"""

import logging
import os
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader

logger = logging.getLogger("lavs-api")

# Header name for API key
API_KEY_HEADER = "X-API-Key"

# Environment variable name for API key
API_KEY_ENV_VAR = "LAVS_API_KEY"

# Header dependency for FastAPI
api_key_header = APIKeyHeader(name=API_KEY_HEADER, auto_error=False)


def get_configured_api_key() -> str | None:
    """Get the configured API key from environment variable.

    Returns:
        The API key string if configured, None otherwise.
    """
    return os.environ.get(API_KEY_ENV_VAR)


def is_authentication_enabled() -> bool:
    """Check if authentication is enabled (i.e., an API key is configured).

    Returns:
        True if API key is configured, False otherwise.
    """
    api_key = get_configured_api_key()
    return api_key is not None and api_key != ""


async def get_api_key(api_key: Annotated[str | None, Depends(api_key_header)] = None) -> str:
    """Validate the API key from the request header.

    This dependency can be used to protect routes. When authentication
    is disabled (no API key configured), any request is allowed through.

    Args:
        api_key: The API key from the request header, provided by FastAPI
                 dependency injection.

    Returns:
        The validated API key, or empty string if auth is disabled.

    Raises:
        HTTPException: If authentication is enabled and the provided
                       API key is invalid or missing.
    """
    # If no API key is configured, allow all requests (optional auth)
    if not is_authentication_enabled():
        logger.debug("Authentication disabled - allowing request")
        return api_key if api_key is not None else ""

    # Authentication is enabled - validate the API key
    configured_key = get_configured_api_key()

    if api_key is None:
        logger.warning("API key missing in request")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key is required. Provide it in the X-API-Key header.",
        )

    if api_key != configured_key:
        logger.warning("Invalid API key provided")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API key",
        )

    logger.debug("API key validated successfully")
    return api_key


# Type alias for dependency injection
ApiKeyDep = Annotated[str, Depends(get_api_key)]
