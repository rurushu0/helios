import os
import git
from pathlib import Path
from git import Repo


class GitRepo:
    # ============================================================================
    #   1. Constructor, and Build-in Methods
    # ============================================================================
    def __init__(self, local_path: str, remote_url: str = ""):
        self._local_path = local_path
        self._remote_url = remote_url

        if not Path(local_path).exists():
            Path(local_path).mkdir(parents=True, exist_ok=True)

        path_git = os.path.join(self.local_path, '.git')

        if not remote_url:
            if not Path(path_git).exists():
                self._repo = GitRepo._local_git_init(local_path)
            else:
                self._repo = Repo(local_path)
        else:
            if not Path(path_git).exists():
                self._repo = GitRepo._clone_remote(local_path, remote_url)
            else:
                self._repo = Repo(local_path)

    # ============================================================================
    #   2. Static methods
    # ============================================================================
    @staticmethod
    def _clone_remote(local_path: str, remote_url: str) -> Repo:
        return Repo.clone_from(remote_url, local_path, branch="master")
# init_repo
    @staticmethod
    def _local_git_init(local_path: str) -> Repo:
        Path(local_path).mkdir(parents=True, exist_ok=True)
        repo = git.Repo.init(local_path)
        return repo

    @staticmethod
    def _init_repo_impl1(local_path: str, remote_url: str) -> Repo:
        Path(local_path).mkdir(parents=True, exist_ok=True)
        repo = git.Repo.init(local_path)
        origin = repo.create_remote('origin', remote_url)
        origin.fetch()
        # create local branch "master" from remote "master"
        repo.create_head('master', origin.refs.master)
        # set local "master" to track remote "master
        repo.heads.master.set_tracking_branch(origin.refs.master)
        repo.heads.master.checkout()
        return repo

    # ============================================================================
    #     6. Properties
    # ============================================================================
    @property
    def local_path(self) -> str:
        return self._local_path

    # ============================================================================
    #     7. Instance methods
    # ============================================================================
    def checkout(self, brunch: str):
        self._repo.git.checkout(brunch)

    def commit(self, comment: str):
        self._repo.index.add(['.'])
        self._repo.index.commit(comment)
