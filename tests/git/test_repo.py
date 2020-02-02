from helios.directory import TempDirectory as TempDir
from helios.git import GitRepo

REMOTE_URL = "https://github.com/rurushu0/helios.git"


def test_gitrepo():
    with TempDir() as tmp_dir:
        repo = GitRepo(local_path=tmp_dir.path, remote_url=REMOTE_URL)
        assert tmp_dir.path == repo.local_path
