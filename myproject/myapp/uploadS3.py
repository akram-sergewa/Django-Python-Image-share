import boto
from boto.s3.connection import S3Connection
from django.conf import settings
import os


class UploadToS3:

    def uploadFile(self, fileName, path):
        AWS_ACCESS_KEY_ID = settings.AWS_ACCESS_KEY_ID
        AWS_SECRET_ACCESS_KEY = settings.AWS_SECRET_ACCESS_KEY
        AWS_STORAGE_BUCKET_NAME = settings.AWS_STORAGE_BUCKET_NAME

        bucket_name = AWS_STORAGE_BUCKET_NAME
        conn = S3Connection(settings.AWS_ACCESS_KEY_ID,
                settings.AWS_SECRET_ACCESS_KEY)


        import boto.s3
        bucket = conn.get_bucket(bucket_name)

        testfile = fileName
        print 'Uploading %s to Amazon S3 bucket %s' % \
           (testfile, bucket_name)

        import sys
        def percent_cb(complete, total):
            sys.stdout.write('.')
            sys.stdout.flush()

        from boto.s3.key import Key
        key_name = fileName
        full_key_name = os.path.join(path, key_name)
        k = bucket.new_key(full_key_name)
        k.set_contents_from_filename(testfile, cb=percent_cb, num_cb=10)

        # k = Key(bucket)
        # k.key = 'my test file'
        # k.set_contents_from_filename(testfile,
            # cb=percent_cb, num_cb=10)