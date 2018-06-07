from template import t

from troposphere import s3

print('adding s3_buckets')

previous_time_bucket = t.add_resource(s3.Bucket("S3Bucket"))

