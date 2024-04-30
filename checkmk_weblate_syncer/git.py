from pathlib import Path

from git import Repo


def repository_in_clean_state(path: Path, branch: str) -> Repo:
    repo = Repo(path)
    repo.git.clean("-fd")
    repo.git.reset("--hard")
    repo.remotes.origin.fetch()
    repo.git.checkout(branch)
    repo.git.reset("--hard", "origin")
    repo.remotes.origin.pull()
    return repo
