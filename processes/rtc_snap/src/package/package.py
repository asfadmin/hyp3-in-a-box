import pathlib as pl
import zipfile as zf
from typing import List

from ordered_set import OrderedSet

from outputs import ProcessOutputs, OutputPatterns


def outputs(
    *,
    archive_name: str,
    working_dir: str,
    output_patterns: OutputPatterns
) -> ProcessOutputs:
    work_dir_path = pl.Path(working_dir)

    output_file_paths = find_output_files(
        work_dir_path,
        output_patterns.archive
    )

    archive_paths = remove_working_dir_from(
        output_file_paths,
        work_dir_path
    )

    archive_path = create_archive(
        work_dir_path / f'{archive_name}.zip',
        output_file_paths,
        archive_paths
    )

    browse_path = find_browse_path(
        work_dir_path,
        output_patterns.browse
    )

    return ProcessOutputs(
        archive_path,
        browse_path
    )


def find_output_files(
    work_dir: pl.Path,
    file_patterns: List[str]
) -> List[pl.Path]:
    output_files: List[pl.Path] = []

    for pattern in file_patterns:
        paths_matching_pattern = find_files_matching(pattern, work_dir)

        if paths_matching_pattern == []:
            raise NoFilesFoundForOutputPattern(
                f"pattern '{pattern}' has no "
                f"matching files in working directory {work_dir}"
            )

        output_files.extend(paths_matching_pattern)

    return output_files


def find_files_matching(
    pattern: str,
    work_dir: pl.Path
) -> List[pl.Path]:
    return list(work_dir.glob(pattern))


def remove_working_dir_from(
    output_files: List[pl.Path],
    work_dir: pl.Path
) -> List[pl.Path]:
    return [
        remove_working_dir_from_path(output_file, work_dir)
        for output_file in output_files
    ]


def remove_working_dir_from_path(
    output_file: pl.Path,
    work_dir: pl.Path
) -> pl.Path:
    work_dir_set, output_file_set = [
        make_ordered_set_from(path)
        for path in [work_dir, output_file]
    ]

    path_without_working_dir = work_dir_set ^ output_file_set

    return pl.Path(*path_without_working_dir)


def make_ordered_set_from(path: pl.Path) -> OrderedSet:
    return OrderedSet(path.parts)


def create_archive(
    archive_path: pl.Path,
    output_paths: List[pl.Path],
    archive_paths: List[pl.Path]
) -> pl.Path:
    with zf.ZipFile(str(archive_path), 'w') as archive:
        add_files_to(archive, output_paths, archive_paths)

    return archive_path


def add_files_to(
    archive: zf.ZipFile,
    output_files: List[pl.Path],
    archive_names: List[pl.Path]
) -> None:
    for output_path, archive_path in zip(output_files, archive_names):
        archive.write(output_path, arcname=archive_path)


def find_browse_path(work_dir: pl.Path, browse_pattern: str):
    possible_browses = find_files_matching(
        browse_pattern,
        work_dir
    )

    try:
        browse = pl.Path(possible_browses[0])
    except IndexError:
        raise NoBrowseFound(
            f"Can't find browse with pattern '{browse_pattern}' "
            f"in dir '{work_dir}')"
        ) from None

    return browse


class NoBrowseFound(Exception):
    pass


class NoFilesFoundForOutputPattern(Exception):
    pass
