import re

CONVENTIONAL_TYPES = ["feat", "fix"]
DEFAULT_TYPES_WITH_EMOJI: dict = {
    "build": ["🏗️"],
    "chore": [],
    "ci": ["👷"],
    "docs": ["📝"],
    "feat": ["✨", "🚩"],
    "fix": ["🐛", "🚑️", "🚨", "🩹"],
    "perf": ["⚡️", "⚗️", "🗃️"],
    "refactor": ["♻️"],
    "revert": ["⏪️"],
    "style": ["💄"],
    "test": ["✅", "🧪"],
}
DEFAULT_TYPES: list[str] = list(DEFAULT_TYPES_WITH_EMOJI.keys())


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


def is_conventional(input: str,
                    types: list[str] = DEFAULT_TYPES,
                    optional_scope: bool = True) -> bool:
    """
    Returns True if input matches Conventional Commits formatting
    https://www.conventionalcommits.org

    Optionally provide a list of additional custom types.
    """
    types = conventional_types(types)
    emoji = (" |".join(list(map(lambda _type: " |".join(DEFAULT_TYPES_WITH_EMOJI[_type]), DEFAULT_TYPES))) + "|").replace("| |", "|")
    pattern = f"^({emoji})({r_types(types)}){r_scope(optional_scope)}{r_delim()}{r_subject()}$".replace("| |", "|")
    regex = re.compile(pattern, re.DOTALL)

    return bool(regex.match(input))
