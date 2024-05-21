from pathlib import Path

from checkmk_weblate_syncer.portable_object import (
    make_soure_string_locations_relative,
    remove_last_translator,
    remove_source_string_locations,
)


def test_make_soure_string_locations_relative() -> None:
    assert (
        make_soure_string_locations_relative(
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


def test_remove_source_string_locations() -> None:
    assert (
        remove_source_string_locations(
            """# Copyright (C) 2019 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

msgid ""
msgstr ""
"Project-Id-Version: Checkmk user interface translation 0.1\n"
"Report-Msgid-Bugs-To: someone@checkmk.com\n"
"POT-Creation-Date: 2011-05-13 09:42+0200\n"
"PO-Revision-Date: 2024-05-15 06:43+0000\n"
"Last-Translator: Employee <employee@checkmk.com>\n"
"Language-Team: German <https://translate.checkmk.com/projects/checkmk/"
"software/de/>\n"
"Language: de\n"
"MIME-Version: 1.0\n"
"Content-Type: text/plain; charset=UTF-8\n"
"Content-Transfer-Encoding: 8bit\n"
"Plural-Forms: nplurals=2; plural=n != 1;\n"
"X-Generator: Weblate 5.0.2\n"

#: cmk/gui/cee/sla/_sla_painter/_service_outage_count.py:31
#, python-format
msgid " %s, outage duration %s"
msgstr " %s, Dauer des Ausfalls %s"

#: cmk/gui/wato/pages/host_rename.py:628
#, python-format
msgid " (%d times)"
msgstr " (%d mal)"

#: cmk/gui/visuals/_page_edit_visual.py:137
msgid " (Copy)"
msgstr " (Kopie)"
"""
        )
        == """# Copyright (C) 2019 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

msgid ""
msgstr ""
"Project-Id-Version: Checkmk user interface translation 0.1\n"
"Report-Msgid-Bugs-To: someone@checkmk.com\n"
"POT-Creation-Date: 2011-05-13 09:42+0200\n"
"PO-Revision-Date: 2024-05-15 06:43+0000\n"
"Last-Translator: Employee <employee@checkmk.com>\n"
"Language-Team: German <https://translate.checkmk.com/projects/checkmk/"
"software/de/>\n"
"Language: de\n"
"MIME-Version: 1.0\n"
"Content-Type: text/plain; charset=UTF-8\n"
"Content-Transfer-Encoding: 8bit\n"
"Plural-Forms: nplurals=2; plural=n != 1;\n"
"X-Generator: Weblate 5.0.2\n"

#, python-format
msgid " %s, outage duration %s"
msgstr " %s, Dauer des Ausfalls %s"

#, python-format
msgid " (%d times)"
msgstr " (%d mal)"

msgid " (Copy)"
msgstr " (Kopie)"
"""
    )


def test_remove_last_translator() -> None:
    assert (
        remove_last_translator(
            """# Copyright (C) 2019 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

msgid ""
msgstr ""
"Project-Id-Version: Checkmk user interface translation 0.1\n"
"Report-Msgid-Bugs-To: someone@checkmk.com\n"
"POT-Creation-Date: 2011-05-13 09:42+0200\n"
"PO-Revision-Date: 2024-05-15 06:43+0000\n"
"Last-Translator: Employee <employee@checkmk.com>\n"
"Language-Team: German <https://translate.checkmk.com/projects/checkmk/"
"software/de/>\n"
"Language: de\n"
"MIME-Version: 1.0\n"
"Content-Type: text/plain; charset=UTF-8\n"
"Content-Transfer-Encoding: 8bit\n"
"Plural-Forms: nplurals=2; plural=n != 1;\n"
"X-Generator: Weblate 5.0.2\n"

#: cmk/gui/cee/sla/_sla_painter/_service_outage_count.py:31
#, python-format
msgid " %s, outage duration %s"
msgstr " %s, Dauer des Ausfalls %s"

#: cmk/gui/wato/pages/host_rename.py:628
#, python-format
msgid " (%d times)"
msgstr " (%d mal)"

#: cmk/gui/visuals/_page_edit_visual.py:137
msgid " (Copy)"
msgstr " (Kopie)"
"""
        )
        == """# Copyright (C) 2019 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

msgid ""
msgstr ""
"Project-Id-Version: Checkmk user interface translation 0.1\n"
"Report-Msgid-Bugs-To: someone@checkmk.com\n"
"POT-Creation-Date: 2011-05-13 09:42+0200\n"
"PO-Revision-Date: 2024-05-15 06:43+0000\n"
"Language-Team: German <https://translate.checkmk.com/projects/checkmk/"
"software/de/>\n"
"Language: de\n"
"MIME-Version: 1.0\n"
"Content-Type: text/plain; charset=UTF-8\n"
"Content-Transfer-Encoding: 8bit\n"
"Plural-Forms: nplurals=2; plural=n != 1;\n"
"X-Generator: Weblate 5.0.2\n"

#: cmk/gui/cee/sla/_sla_painter/_service_outage_count.py:31
#, python-format
msgid " %s, outage duration %s"
msgstr " %s, Dauer des Ausfalls %s"

#: cmk/gui/wato/pages/host_rename.py:628
#, python-format
msgid " (%d times)"
msgstr " (%d mal)"

#: cmk/gui/visuals/_page_edit_visual.py:137
msgid " (Copy)"
msgstr " (Kopie)"
"""
    )
