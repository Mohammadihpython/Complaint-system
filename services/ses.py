import boto3

from config import settings


class S3SService:
    def __init__(self):
        self.key = settings.AWS_ACCESS_KEY
        self.secret = settings.AWS_SECRET
        self.ses = boto3.client("ses",
                                region_name=settings.AWS_REGION,
                                aws_access_key_id=self.key,
                                aws_secret_access_key=self.secret,
                                endpoint_url=settings.LOCALSTACK_URL,
                                )

    def send_mail(self, subject, to_addresses, text_data):
        body = {
            "Text": {"data": text_data, "Charset": "UTF-8"}
        }
        self.ses.send_email(
            Source=settings.EMAIL,
            Destination={"TOAddresses": to_addresses,
                         "CcAddresses": [],
                         "BccAddresses": []
                         },
            Message={"Subject": {"data": subject, "Charset": "UTF-8"}, "Body": body}
        )
