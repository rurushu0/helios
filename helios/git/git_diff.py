from collections import namedtuple
from helios.directory import Directory as Dir
from helios.directory import GitDirectory as GitDir
from helios.directory import TempDirectory as TempDir
from .repo import GitRepo
from helios.file import File
from helios.source.java import JavaSourceFile, JavaSourceFormatter

import os

GitInfo = namedtuple('GitInfo', ['remote_url', 'commit_id'])


def git_diff(info_1: GitInfo, info_2: GitInfo, output_path: str):
    name_repo1 = git_repo_name(info_1.remote_url)
    name_repo2 = git_repo_name(info_2.remote_url)
    if name_repo1 == name_repo2:
        name_repo1 += '_1'
        name_repo2 += '_2'

    with TempDir() as work_dir:
        Dir.remove(output_path)
        output_dir = Dir(output_path)

        repo_1 = GitRepo(os.path.join(
            work_dir.path, name_repo1), info_1.remote_url)
        repo_2 = GitRepo(os.path.join(
            work_dir.path, name_repo2), info_2.remote_url)
        repo_1.checkout(info_1.commit_id)
        repo_2.checkout(info_2.commit_id)

        dir_1 = GitDir(repo_1.local_path)
        dir_2 = GitDir(repo_2.local_path)

        java_files_1 = list(
            filter(lambda x: JavaSourceFile.is_java_file_name(x),
                   dir_1.file_list()))
        java_files_2 = list(
            filter(lambda x: JavaSourceFile.is_java_file_name(x),
                   dir_2.file_list()))
        JavaSourceFormatter.execute(java_files_1)
        JavaSourceFormatter.execute(java_files_2)

        diff_files = dir_1.diff_files(dir_2)

        for f in diff_files.both:
            f1 = File(os.path.join(repo_1.local_path, f))
            f2 = File(os.path.join(repo_2.local_path, f))
            f_output = File(os.path.join(output_dir.full_path, f + '.diff'))
            with open(f_output.full_path, 'w', encoding='utf-8') as fw:
                fw.write('\n'.join(f1.diff(f2)))
                fw.flush()


def git_repo_name(url: str) -> str:
    idx = url.rfind('/') + 1
    if idx <= 0:
        return ''
    return url[idx:].replace('.git', '')
