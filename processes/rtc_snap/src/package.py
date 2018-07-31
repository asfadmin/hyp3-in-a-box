import pathlib as pl
import zipfile as zf

from ordered_set import OrderedSet


def outputs_from(zip_name, working_dir, file_patterns):
    work_dir_path = pl.Path(working_dir)

    output_file_paths = find_output_file_paths(
        work_dir_path,
        file_patterns
    )

    archive_paths = remove_working_dir_from(
        output_file_paths,
        work_dir_path
    )

    with zf.ZipFile(zip_name, 'w') as archive:
        add_files_to(archive, output_file_paths, archive_paths)

    return zip_name


def find_output_file_paths(work_dir_path, file_patterns):
    output_file_paths = []

    for pattern in file_patterns:
        output_file_paths += list(work_dir_path.glob(pattern))

    return output_file_paths


def remove_working_dir_from(output_file_paths, work_dir_path):
    archive_paths = []

    for output_file_path in output_file_paths:
        arc_path_name_parts = \
            OrderedSet(work_dir_path.parts).symmetric_difference(
                OrderedSet(output_file_path.parts)
            )

        arc_path = pl.Path(*list(arc_path_name_parts))

        archive_paths.append(arc_path)

    return archive_paths


def add_files_to(archive, output_paths, archive_paths):
    for output_path, archive_path in zip(output_paths, archive_paths):
        archive.write(output_path, arcname=archive_path)
