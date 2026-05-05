import re
from dataclasses import dataclass

# keep in sync with tests/pylint/checker_localization.py:HTMLTagsChecker
_TAG_PATTERN = re.compile("<.*?>")
_ALLOWED_TAGS_PATTERN = re.compile(
    r"</?(h1|h2|b|tt|i|u|hr|br(?: /)?|nobr(?: /)?|pre|sup|p|li|ul|ol|a|(a.*? href=.*?))>",
)


@dataclass(frozen=True)
class ForbiddenTag:
    line: int
    tag: str


def forbidden_tags(text: str) -> frozenset[ForbiddenTag]:
    return frozenset(
        ForbiddenTag(
            line=text.count("\n", 0, match.start()) + 1,
            tag=match.group(),
        )
        for match in _TAG_PATTERN.finditer(text)
        if not _ALLOWED_TAGS_PATTERN.match(match.group())
    )
