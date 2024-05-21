import re
from pathlib import Path


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
