import pytest

from checkmk_weblate_syncer.html_tags import ForbiddenTag, forbidden_tags


@pytest.mark.parametrize(
    ("text", "expected_result"),
    [
        pytest.param(
            "abc123",
            frozenset(),
        ),
        pytest.param(
            "<tt>bold</tt>",
            frozenset(),
        ),
        pytest.param(
            '* ? <a href="%s">%s</a>',
            frozenset(),
        ),
        pytest.param(
            '&copy; <a target="_blank" href="https://checkmk.com">Checkmk GmbH</a>',
            frozenset(),
        ),
        pytest.param(
            "123 <script>injection</script>",
            frozenset(
                {
                    ForbiddenTag(line=1, tag="<script>"),
                    ForbiddenTag(line=1, tag="</script>"),
                },
            ),
        ),
        pytest.param(
            "ok line\nbad <foo> line\nanother bad <bar> line",
            frozenset(
                {
                    ForbiddenTag(line=2, tag="<foo>"),
                    ForbiddenTag(line=3, tag="<bar>"),
                },
            ),
        ),
        pytest.param(
            '"<br><b>Hinweis</>: trailing"',
            frozenset({ForbiddenTag(line=1, tag="</>")}),
        ),
        pytest.param(
            # pylint: disable=line-too-long
            """#: /home/weblate/checkmk_weblate_sync/git/checkmk/cmk/gui/wato/pages/host_rename.py:640
#, python-format
msgid " (%d times)"
msgstr ""

#: /home/weblate/checkmk_weblate_sync/git/checkmk/cmk/gui/visuals/_page_edit_visual.py:137
msgid " (Copy)"
msgstr ""

#: /home/weblate/checkmk_weblate_sync/git/checkmk/cmk/gui/nodevis/topology.py:1814
msgid " (Data incomplete, maximum number of nodes reached)"
msgstr ""

#: /home/weblate/checkmk_weblate_sync/git/checkmk/cmk/gui/backup/handler.py:969
#, python-format
msgid " (Duration: %s)"
msgstr ""
""",
            frozenset(),
        ),
    ],
)
def test_html_tags_checker(
    text: str,
    expected_result: frozenset[ForbiddenTag],
) -> None:
    assert forbidden_tags(text) == expected_result
