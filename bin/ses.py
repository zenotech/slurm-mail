import boto3
from boto3.session import Session
from botocore.exceptions import ClientError


class SesSendMail(object):

    def __init__(self, region, role_arn = None):
        self._region = region
        if role_arn is not None:
            client = boto3.client('sts', region_name=self._region)
            response = client.assume_role(RoleArn=role_arn, RoleSessionName="slurm_mail_session")
            credentials = response['Credentials']
            session = Session(aws_access_key_id=credentials['AccessKeyId'],
                              aws_secret_access_key=credentials['SecretAccessKey'],
                              aws_session_token=credentials['SessionToken'])
            self._client = session.client('ses',region_name=self._region)
        else:
            self._client  = boto3.client('ses',region_name=self._region)


    def sendmail(self, emailFromUserAddress, emailToUserAddress, subject, msg_html, msg_txt, msg_charset = "UTF-8"):
        try:
            response = self._client.send_email(
                            Destination={
                                'ToAddresses': [
                                    emailToUserAddress,
                                ],
                            },
                            Message={
                                'Body': {
                                    'Html': {
                                        'Charset': msg_charset,
                                        'Data': msg_html,
                                    },
                                    'Text': {
                                        'Charset': msg_charset,
                                        'Data': msg_txt,
                                    },
                                },
                                'Subject': {
                                    'Charset': msg_charset,
                                    'Data': subject,
                                },
                            },
                            Source=emailFromUserAddress,
            )
        except ClientError as e:
            print("Error sending slurm email")
            print(e.response['Error']['Message'])