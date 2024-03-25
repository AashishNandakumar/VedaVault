import boto3
from django.conf import settings


class SMSClient:
    @staticmethod
    def send_otp_sms(**kwargs):
        try:
            phone_number = kwargs['phone_number']
            reason = kwargs['reason']
            otp = kwargs['otp']

            sns_client = boto3.client(
                'sns',
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                region_name=settings.AWS_S3_REGION_NAME
            )

            sns_client.publish(
                PhoneNumber=phone_number,
                Message=f"Your OTP by VedaVault for {reason} is : {otp}",
                MessageAttributes={
                    "AWS.SNS.SMS.SMSType": {
                        'DataType': 'String',
                        'StringValue': 'Transactional'
                    }
                }
            )
        except Exception as e:
            print("Error while sending otp through sms: ", e)
            return e

