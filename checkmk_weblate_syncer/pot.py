import re
from pathlib import Path
from subprocess import CalledProcessError
from subprocess import run as run_subprocess

from .config import PotModeConfig
from .git import commit_and_push_files, repository_in_clean_state
from .logging import LOGGER


def run(config: PotModeConfig) -> int:
    repository_in_clean_state(config.checkmk_repository)
    locale_repo = repository_in_clean_state(config.locale_repository)

    LOGGER.info("Calling pot generation script")
    try:
        completed_pot_generation_process = run_subprocess(
            config.checkmk_repository.path / config.checkmk_pot_generation_script,
            check=True,
            capture_output=True,
            encoding="UTF-8",
        )
    except CalledProcessError as e:
        LOGGER.error(
            "Generating pot file failed.\n\nStdout:\n%s\n\nStderr:\n%s",
            e.stdout,
            e.stderr,
        )
        raise e
    except IOError as e:
        LOGGER.error("Generating pot file failed")
        raise e

    LOGGER.info("Making source string locations relative")
    pot_file_content = _make_soure_string_locations_relative(
        pot_file_content=completed_pot_generation_process.stdout,
        relative_to=config.checkmk_repository.path,
    )

    LOGGER.info("Writing pot file to locale repository")
    path_pot_file = config.locale_repository.path / config.locale_pot_path
    try:
        path_pot_file.write_text(pot_file_content)
    except IOError as e:
        LOGGER.error("Writing pot file failed")
        raise e

    LOGGER.info("Checking if pot file has changed in locale repository")
    try:
        if not locale_repo.is_dirty(untracked_files=True):
            LOGGER.info("No changes, exiting")
            return 0
    except Exception as e:
        LOGGER.error("Checking if pot file has changed failed")
        raise e

    LOGGER.info("Committing and pushing pot file to locale repository")
    commit_and_push_files(
        repo=locale_repo,
        files=[path_pot_file],
        commit_message=config.commit_message,
    )
    return 0


def _make_soure_string_locations_relative(
    pot_file_content: str,
    relative_to: Path,
) -> str:
    return re.sub(
        rf"^#: ({relative_to}\/)(.*?:\d+)\n",
        r"#: \g<2>\n",
        pot_file_content,
        flags=re.MULTILINE | re.DOTALL,
    )
