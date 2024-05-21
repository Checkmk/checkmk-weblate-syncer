from dataclasses import dataclass
from pathlib import Path
from subprocess import DEVNULL, PIPE, CalledProcessError
from subprocess import run as run_subprocess
from typing import assert_never

from git import Repo

from .config import PoFilePair, RepositoryConfig, UpdateTranslationsConfig
from .git import commit_and_push_files, repository_in_clean_state
from .html_tags import forbidden_tags
from .logging import LOGGER
from .portable_object import (
    remove_header,
    remove_last_translator,
    remove_source_string_locations,
)


@dataclass(frozen=True)
class _Success:
    path: Path


@dataclass(frozen=True)
class _Failure:
    error_message: str
    path: Path


def run(config: UpdateTranslationsConfig) -> int:
    checkmk_repo = repository_in_clean_state(config.checkmk_repository)
    repository_in_clean_state(config.locale_repository)

    failures: list[_Failure] = []
    successes: list[_Success] = []

    for file_pair in config.po_file_pairs:
        LOGGER.info("Processing %s, %s", file_pair.locale, file_pair.checkmk)
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
                    "Encountered an error while processing the .po file pair. "
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
    LOGGER.info("Checking for formatting errors in %s", locale_po_file)
    try:
        run_subprocess(
            ["msgfmt", "--check-format", "-o", "-", locale_po_file],
            check=True,
            stdout=DEVNULL,
            stderr=PIPE,
            encoding="UTF-8",
        )
    except CalledProcessError as e:
        return _Failure(
            error_message=f"Found formatting errors: {e.stderr}", path=locale_po_file
        )
    except IOError as e:
        return _Failure(error_message=str(e), path=locale_po_file)

    LOGGER.info("Reading %s", locale_po_file)
    try:
        po_file_content = locale_po_file.read_text()
    except IOError as e:
        return _Failure(
            error_message=f"Encountered error while reading file: {str(e)}",
            path=locale_po_file,
        )

    LOGGER.info("Checking HTML tags")
    if forbidden_html_tags := forbidden_tags(remove_header(po_file_content)):
        return _Failure(
            error_message=f"Found forbidden HTML tags: {', '.join(sorted(forbidden_html_tags))}",
            path=locale_po_file,
        )

    LOGGER.info("Stripping source string locations and Last-Translator")
    po_file_content = remove_source_string_locations(po_file_content)
    po_file_content = remove_last_translator(po_file_content)

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
