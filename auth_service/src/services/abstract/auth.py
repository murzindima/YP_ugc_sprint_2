from abc import ABC, abstractmethod

from fastapi import Request


class AuthAbstractService[M](ABC):
    """Abstract base class defining authentication service methods."""

    @abstractmethod
    async def login(self, login: str, password: str, request: Request) -> M | None:
        """Authenticate a user."""

    @abstractmethod
    async def logout(self, request: Request) -> None:
        """Log out the user."""


class OAuthAbstractService(ABC):
    @abstractmethod
    async def initiate_login_flow(self, request: Request) -> str:
        """Generate the URL to redirect the user to the OAuth provider's login page."""

    @abstractmethod
    async def process_callback(self, request: Request) -> dict:
        """Process the callback from the OAuth provider and return user information."""
