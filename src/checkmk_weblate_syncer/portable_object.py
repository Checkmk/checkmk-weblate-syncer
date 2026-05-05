import re
from collections.abc import Iterable
from pathlib import Path

from .html_tags import ForbiddenTag

_SOURCE_REFERENCE_PATTERN = re.compile(r"^#: (.+?:\d+)$")


def remove_header(portable_object_content: str) -> tuple[str, int]:
    lines = portable_object_content.splitlines()
    index_first_source_string_location = 0
    for index, line in enumerate(lines):
        if _SOURCE_REFERENCE_PATTERN.match(line):
            index_first_source_string_location = index
            break
    body = "\n".join(lines[index_first_source_string_location:]) + (
        "\n" if portable_object_content.endswith("\n") else ""
    )
    return body, index_first_source_string_location


def source_references_at(content: str, line: int) -> tuple[str, ...]:
    lines = content.splitlines()
    if not 1 <= line <= len(lines):
        return ()
    block_start = 0
    for i in range(line - 1, -1, -1):
        if lines[i] == "":
            block_start = i + 1
            break
    return tuple(
        match.group(1)
        for line_text in lines[block_start:line]
        if (match := _SOURCE_REFERENCE_PATTERN.match(line_text))
    )


def format_forbidden_tags_error(
    portable_object_content: str,
    header_line_count: int,
    tags: Iterable[ForbiddenTag],
) -> str:
    formatted: list[str] = []
    for tag in sorted(tags, key=lambda t: (t.line, t.tag)):
        absolute_line = header_line_count + tag.line
        references = source_references_at(portable_object_content, absolute_line)
        suffix = f" ({', '.join(references)})" if references else ""
        formatted.append(f"  line {absolute_line}: {tag.tag!r}{suffix}")
    return "Found forbidden HTML tags:\n" + "\n".join(formatted)


def make_soure_string_locations_relative(
    portable_object_content: str,
    relative_to: Path,
) -> str:
    return re.sub(
        rf"^#: ({relative_to}\/)(.*?:\d+)\n",
        r"#: \g<2>\n",
        portable_object_content,
        flags=re.MULTILINE | re.DOTALL,
    )


def remove_source_string_locations(portable_object_content: str) -> str:
    return re.sub(
        r"^#: .*?:\d+\n",
        "",
        portable_object_content,
        flags=re.MULTILINE | re.DOTALL,
    )


def remove_last_translator(portable_object_content: str) -> str:
    return re.sub(
        r"^\"Last-Translator:.*?\"\n",
        "",
        portable_object_content,
        flags=re.MULTILINE | re.DOTALL,
    )
