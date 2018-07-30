import zipfile as zf


def outputs_from(working_dir, file_patterns):
    zip_name = 'output.zip'

    with zf.ZipFile(zip_name, 'w') as output_zip:
        output_zip.write(working_dir + '/hello.txt')

    return zip_name

