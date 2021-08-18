class ConnectBoxError(Exception):
    """General Connect Box exception occurred."""


class InvalidCredentialError(ConnectBoxError):
    """Login credential is invalid."""
