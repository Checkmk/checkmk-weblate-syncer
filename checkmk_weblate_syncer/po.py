import re
from dataclasses import dataclass
from pathlib import Path
from subprocess import CalledProcessError
from subprocess import run as run_subprocess
from typing import assert_never

from git import Repo

from .config import PoFilePair, PoModeConfig, RepositoryConfig
from .git import commit_and_push_files, repository_in_clean_state
from .logging import LOGGER


@dataclass(frozen=True)
class _Success:
    path: Path


@dataclass(frozen=True)
class _Failure:
    error_message: str
    path: Path


def run(config: PoModeConfig) -> int:
    checkmk_repo = repository_in_clean_state(config.checkmk_repository)
    repository_in_clean_state(config.locale_repository)

    failures: list[_Failure] = []
    successes: list[_Success] = []

    for file_pair in config.po_file_pairs:
        match (
            result := _process_po_file_pair(
                file_pair=file_pair,
                checkmk_repo=config.checkmk_repository,
                locale_repo=config.locale_repository,
            )
        ):
            case _Success():
                successes.append(result)
            case _Failure():
                LOGGER.error(
                    "We encountered an error while processing the .po file. "
                    "See the logging output at the end for more information."
                )
                failures.append(result)
            case _:
                assert_never(result)

    LOGGER.info("Checking if any .po files changed in the checkmk repository")
    if _is_repo_dirty(checkmk_repo):
        LOGGER.info("Committing and pushing .po files to checkmk repository")
        commit_and_push_files(
            repo=checkmk_repo,
            files=[success.path for success in successes],
            commit_message=config.commit_message,
        )
    else:
        LOGGER.info("No changes in checkmk repository.")

    if not failures:
        return 0

    for failure in failures:
        LOGGER.error(
            "Encountered the following error while processing %s:\n%s",
            failure.path,
            failure.error_message,
        )
    return 1


def _process_po_file_pair(
    file_pair: PoFilePair,
    checkmk_repo: RepositoryConfig,
    locale_repo: RepositoryConfig,
) -> _Success | _Failure:
    checkmk_po_file = checkmk_repo.path / file_pair.checkmk
    locale_po_file = locale_repo.path / file_pair.locale
    LOGGER.info("Checking formatting errors in %s", locale_po_file)
    try:
        run_subprocess(
            ["msgfmt", "--check-format", "-o", "-", locale_po_file],
            check=True,
            capture_output=True,
            encoding="UTF-8",
        )
    except CalledProcessError as e:
        return _Failure(
            error_message=f"Found formatting errors: {e.stderr}", path=locale_po_file
        )
    except IOError as e:
        return _Failure(error_message=str(e), path=locale_po_file)

    LOGGER.info("Removing unwanted lines from %s", locale_po_file)
    if isinstance(po_file_content := _remove_unwanted_lines(locale_po_file), _Failure):
        return po_file_content

    LOGGER.info("Writing stripped .po file to checkmk repository: %s", checkmk_po_file)
    try:
        checkmk_po_file.write_text(po_file_content)
    except IOError as e:
        return _Failure(
            f"Encountered error while writing po file to checkmk repository: {e}",
            checkmk_po_file,
        )
    return _Success(checkmk_po_file)


def _is_repo_dirty(repo: Repo) -> bool:
    try:
        return repo.is_dirty(untracked_files=True)
    except Exception as e:
        LOGGER.error(
            "Checking if any .po files changed in the checkmk repository failed"
        )
        raise e


def _remove_unwanted_lines(file_path: Path) -> str | _Failure:
    LOGGER.info("Reading %s", file_path)
    try:
        po_file_content = file_path.read_text()
    except IOError as e:
        return _Failure(
            error_message=f"Encountered error while reading file: {str(e)}",
            path=file_path,
        )
    LOGGER.info("Removing code comments from %s", file_path)
    po_file_content = re.sub(r"^#.+\d\n", "", po_file_content, flags=re.DOTALL)

    LOGGER.info("Removing last translator information from %s", file_path)
    po_file_content = re.sub(
        r"\"Last-Translator:.+?\n", "", po_file_content, flags=re.DOTALL
    )
    return po_file_content
