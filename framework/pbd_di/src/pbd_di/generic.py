from typing import TypeVar


SINGLETON = "singleton"
TRANSIENT = "transient"
SCOPED = "scoped"

VALID_SCOPES = [SINGLETON, TRANSIENT, SCOPED]


TDependency = TypeVar("TDependency")