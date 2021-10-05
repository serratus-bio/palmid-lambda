# app.py
import boto3
from botocore.exceptions import ClientError
import hashlib

s3 = boto3.resource('s3')
s3_client = boto3.client('s3')


# check if object with this name already exists in S3
def check(s3_client, bucket, key):
    try:
        s3_client.head_object(Bucket=bucket, Key=key)
    except ClientError as e:
        return int(e.response['Error']['Code']) != 404
    return True

#
# def get_report_from_S3(filename):
#     s3_object = s3.Object(bucket_name='openvirome.com',
#                           key=filename + '.html')
#     report = s3_object.get()['Body'].read()
#
#     return report


def get_report(event, context):
    # go to S3 and check if report with such name exists
    try:
        sequence = event["sequence"]
        filename = hashlib.sha1(sequence.encode()).hexdigest()

        check_results = check(s3_client, 'openvirome.com', filename + '.html')

        # send the report link to the user
        return {"url": "https://s3.amazonaws.com/openvirome.com/" + filename + ".html"}
    finally:

        if not check_results:
            # if no report is present in S3, go to lambda in AWS and make docker create the report

            pass
            report = None
            # wait till u get response from docker in form of the report