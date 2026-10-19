from dataclasses import dataclass


@dataclass(frozen=True)
class State:
    row: int
    column: int
    has_key: bool = False
