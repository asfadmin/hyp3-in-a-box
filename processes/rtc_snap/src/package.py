import pathlib as pl
import zipfile as zf

from ordered_set import OrderedSet


def outputs(*, zip_name, working_dir, file_patterns):
    work_dir_path = pl.Path(working_dir)

    output_file_paths = find_output_files(
        work_dir_path,
        file_patterns
    )

    archive_paths = remove_working_dir_from(
        output_file_paths,
        work_dir_path
    )

    return create_archive(
        work_dir_path / zip_name,
        output_file_paths,
        archive_paths
    )


def find_output_files(work_dir_path, file_patterns):
    files_matching_pattern = [
        find_files_matching(pattern, work_dir_path)
        for pattern in file_patterns
    ]

    return sum(files_matching_pattern, [])


def find_files_matching(pattern, work_dir_path):
    return list(work_dir_path.glob(pattern))


def remove_working_dir_from(output_file_paths, work_dir_path):
    return [
        remove_working_dir_from_path(output_file_path, work_dir_path)
        for output_file_path in output_file_paths
    ]


def remove_working_dir_from_path(output_file_path, work_dir_path):
    work_dir_set, output_file_set = [
        make_ordered_set_from(path)
        for path in [work_dir_path, output_file_path]
    ]

    path_without_working_dir = work_dir_set ^ output_file_set

    return pl.Path(*path_without_working_dir)


def make_ordered_set_from(path):
    return OrderedSet(path.parts)


def create_archive(zip_path, output_paths, archive_paths):
    with zf.ZipFile(str(zip_path), 'w') as archive:
        add_files_to(archive, zip(output_paths, archive_paths))

    return zip_path


def add_files_to(archive, output_files):
    for output_path, archive_path in output_files:
        archive.write(output_path, arcname=archive_path)
