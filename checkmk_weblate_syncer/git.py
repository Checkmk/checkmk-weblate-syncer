from collections.abc import Sequence
from pathlib import Path
from subprocess import CalledProcessError

from git import Repo

from .config import RepositoryConfig
from .logging import LOGGER


def repository_in_clean_state(
    repo_config: RepositoryConfig,
) -> Repo:
    LOGGER.info("Cleaning up and updating %s repository", repo_config.path)
    try:
        return _repository_in_clean_state(
            repo_config.path,
            repo_config.branch,
        )
    except Exception as e:
        LOGGER.error(
            "Error while cleaning up and updating %s repository", repo_config.path
        )
        raise e


def _repository_in_clean_state(path: Path, branch: str) -> Repo:
    repo = Repo(path)
    repo.git.reset("--hard")
    repo.remotes.origin.fetch()
    repo.git.checkout(branch)
    repo.git.reset("--hard", f"origin/{branch}")
    return repo


def commit_and_push_files(
    repo: Repo,
    files_to_push_to_repo: Sequence[Path],
) -> None:
    try:
        repo.index.add(files_to_push_to_repo)
        repo.index.commit("Updating files")
        repo.remotes.origin.push()
    except CalledProcessError as e:
        LOGGER.error(
            "Committing and pushing files for repository %s failed", repo.working_dir
        )
        raise e
    LOGGER.info(
        "Committing and pushing files for repository %s succeeded", repo.working_dir
    )
