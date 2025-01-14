import re

# keep in sync with tests/pylint/checker_localization.py:HTMLTagsChecker
_TAG_PATTERN = re.compile("<.*?>")
_ALLOWED_TAGS_PATTERN = re.compile(
    r"</?(h1|h2|b|tt|i|u|hr|br(?: /)?|nobr(?: /)?|pre|sup|p|li|ul|ol|a|(a.*? href=.*?))>",
)


def forbidden_tags(text: str) -> set[str]:
    return {
        tag
        for tag in re.findall(
            _TAG_PATTERN,
            text,
        )
        if not re.match(_ALLOWED_TAGS_PATTERN, tag)
    }
