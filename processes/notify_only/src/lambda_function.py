import boto3

import map_viz


def lambda_handler(event, context):
    png = map_viz.plot_on_map()
    file_path, key = str(png), str(png.name)

    boto3.Bucket('hyp3-in-a-box-lambdas') \
        .upload_file(file_path, key)
