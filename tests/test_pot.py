from pathlib import Path

from checkmk_weblate_syncer.pot import _make_soure_string_locations_relative


def test_make_soure_string_locations_relative() -> None:
    assert (
        _make_soure_string_locations_relative(
            """# Copyright (C) 2019 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

msgid ""
msgstr ""
"Project-Id-Version: Checkmk user interface translation 0.1\n"
"Report-Msgid-Bugs-To: feedback@checkmk.com\n"
"POT-Creation-Date: 2011-05-13 09:42+0200\n"
"PO-Revision-Date: YEAR-MO-DA HO:MI+ZONE\n"
"Last-Translator: FULL NAME <EMAIL@ADDRESS>\n"
"Language-Team: LANGUAGE <LL@li.org>\n"
"Language: LANGUAGE \n"
"MIME-Version: 1.0\n"
"Content-Type: text/plain; charset=utf-8\n"
"Content-Transfer-Encoding: 8bit\n"

#: /home/weblate/checkmk_weblate_sync/git/checkmk/cmk/gui/wato/pages/host_rename.py:640
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
            Path("/home/weblate/checkmk_weblate_sync/git/checkmk"),
        )
        == """# Copyright (C) 2019 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

msgid ""
msgstr ""
"Project-Id-Version: Checkmk user interface translation 0.1\n"
"Report-Msgid-Bugs-To: feedback@checkmk.com\n"
"POT-Creation-Date: 2011-05-13 09:42+0200\n"
"PO-Revision-Date: YEAR-MO-DA HO:MI+ZONE\n"
"Last-Translator: FULL NAME <EMAIL@ADDRESS>\n"
"Language-Team: LANGUAGE <LL@li.org>\n"
"Language: LANGUAGE \n"
"MIME-Version: 1.0\n"
"Content-Type: text/plain; charset=utf-8\n"
"Content-Transfer-Encoding: 8bit\n"

#: cmk/gui/wato/pages/host_rename.py:640
#, python-format
msgid " (%d times)"
msgstr ""

#: cmk/gui/visuals/_page_edit_visual.py:137
msgid " (Copy)"
msgstr ""

#: cmk/gui/nodevis/topology.py:1814
msgid " (Data incomplete, maximum number of nodes reached)"
msgstr ""

#: cmk/gui/backup/handler.py:969
#, python-format
msgid " (Duration: %s)"
msgstr ""
"""
    )
