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
        LOGGER.exception(e)
        raise e
    except Exception as e:
        LOGGER.error("Generating pot file failed")
        LOGGER.exception(e)
        raise e

    LOGGER.info("Writing pot file to locale repository")
    path_pot_file = config.locale_repository.path / config.locale_pot_path
    try:
        path_pot_file.write_text(completed_pot_generation_process.stdout)
    except Exception as e:
        LOGGER.error("Writing pot file failed")
        LOGGER.exception(e)
        raise e

    LOGGER.info("Checking if pot file has changed in locale repository")
    try:
        if not locale_repo.is_dirty(untracked_files=True):
            LOGGER.info("No changes, exiting")
            return 0
    except Exception as e:
        LOGGER.error("Checking if pot file has changed failed")
        LOGGER.exception(e)
        raise e

    LOGGER.info("Committing and pushing pot file to locale repository")
    commit_and_push_files(
        repo=locale_repo,
        files_to_push_to_repo=[path_pot_file],
    )
    return 0
