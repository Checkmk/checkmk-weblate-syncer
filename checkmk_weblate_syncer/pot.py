from subprocess import CalledProcessError
from subprocess import run as run_subprocess

from git import Repo

from .config import PotModeConfig, RepositoryConfig
from .git import repository_in_clean_state
from .logging import LOGGER


def run(config: PotModeConfig) -> None:
    _get_repository_in_clean_state_with_logging(
        config.checkmk_repository,
        "checkmk",
    )
    locale_repo = _get_repository_in_clean_state_with_logging(
        config.locale_repository,
        "locale",
    )

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
            return
    except Exception as e:
        LOGGER.error("Checking if pot file has changed failed")
        LOGGER.exception(e)
        raise e

    LOGGER.info("Committing and pushing pot file to locale repository")
    try:
        locale_repo.index.add([path_pot_file])
        locale_repo.index.commit("Update pot file")
        locale_repo.remotes.origin.push()
    except CalledProcessError as e:
        LOGGER.error("Committing and pushing pot file failed")
        LOGGER.exception(e)
        raise e


def _get_repository_in_clean_state_with_logging(
    repo_config: RepositoryConfig, repo_name: str
) -> Repo:
    LOGGER.info("Cleaning up and updating %s repository", repo_name)
    try:
        return repository_in_clean_state(
            repo_config.path,
            repo_config.branch,
        )
    except Exception as e:
        LOGGER.error("Error while cleaning up and updating %s repository", repo_name)
        LOGGER.exception(e)
        raise e
