import pathlib as pl
import zipfile as zf

from ordered_set import OrderedSet


def outputs_from(working_dir, file_patterns):
    work_dir_path = pl.Path(working_dir)
    zip_name = 'output.zip'

    output_file_paths = []
    for pattern in file_patterns:
        output_file_paths += list(work_dir_path.glob(pattern))

    with zf.ZipFile(zip_name, 'w') as output_zip:
        for output_file_path in output_file_paths:
            arc_path_name_parts = \
                OrderedSet(work_dir_path.parts).symmetric_difference(
                    OrderedSet(output_file_path.parts)
                )

            arc_path = pl.Path(*list(arc_path_name_parts))
            output_zip.write(output_file_path, arcname=arc_path)

    return zip_name
