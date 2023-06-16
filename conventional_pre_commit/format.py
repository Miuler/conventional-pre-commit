import re

CONVENTIONAL_TYPES = ["feat", "fix"]
DEFAULT_TYPES = [
    "build",
    "chore",
    "ci",
    "docs",
    "feat",
    "fix",
    "perf",
    "refactor",
    "revert",
    "style",
    "test",
]
_DEFAULT_TYPES: list[tuple[list[str], str]] = [
    (["✨"], "build"),
    ([], "chore"),
    ([], "ci"),
    ([], "docs"),
    ([], "feat"),
    ([], "fix"),
    ([], "perf"),
    ([], "refactor"),
    ([], "revert"),
    ([], "style"),
    ([], "test"),
]


def r_types(types: list[str]) -> str:
    """Join types with pipe "|" to form regex ORs."""
    return "|".join(types)


def r_scope(optional: bool = True) -> str:
    """Regex str for an optional (scope)."""
    if optional:
        return r"(\([\w \/:-]+\))?"
    else:
        return r"(\([\w \/:-]+\))"


def r_delim() -> str:
    """Regex str for optional breaking change indicator and colon delimiter."""
    return r"!?:"


def r_subject() -> str:
    """Regex str for subject line, body, footer."""
    return r" .+"


def conventional_types(types: list[str] = []) -> list[str]:
    """Return a list of Conventional Commits types merged with the given types."""
    if set(types) & set(CONVENTIONAL_TYPES) == set():
        return CONVENTIONAL_TYPES + types
    return types


def is_conventional(input: str, types: list[str] = DEFAULT_TYPES, optional_scope: bool = True) -> bool:
    """
    Returns True if input matches Conventional Commits formatting
    https://www.conventionalcommits.org

    Optionally provide a list of additional custom types.
    """
    types = conventional_types(types)
    pattern = f"^({r_types(types)}){r_scope(optional_scope)}{r_delim()}{r_subject()}$"
    regex = re.compile(pattern, re.DOTALL)

    return bool(regex.match(input))
