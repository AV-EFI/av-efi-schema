"""Field length limits enforced when checking AVefi records.

The limits are part of the submission rules rather than of the schema
proper: the schema states the maximum lengths of its data types, while
these are the limits a submission is checked against before it is
registered. Callers may override them.

"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Limits:
    """Maximum lengths of a title line and a note."""

    line_limit: int = 250
    text_limit: int = 8192


DEFAULT_LIMITS = Limits()
