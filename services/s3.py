import boto3

from config import settings


class S3Service:
    def __init__(self):
        self.key = settings.AWS_ACCESS_KEY
        self.secret = settings.AWS_SECRET
        self.s3 = boto3.client("s3", aws_access_key_id=self.key,
                               aws_secret_access_key=self.secret,
                               endpoint_url=settings.LOCALSTACK_URL
                               )
        self.bucket = settings.AWS_BUCKET_NAME

    def upload(self, path, key, ext):
        self.s3.upload_file(
            path,
            self.bucket,
            key,
            ExtraArgs={"ACL": "public-read", "ContentType": f"image/{ext}"}
        )
        return f"http://localhost:4566/{self.bucket}/{key}"
