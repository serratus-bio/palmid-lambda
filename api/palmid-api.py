# palmid-api Lambda Function
import json
import hashlib
import urllib.request
import json
import boto3
from botocore.exceptions import ClientError

# Ping for S3 object
s3 = boto3.resource('s3')
s3_client = boto3.client('s3')

def check(s3_client, bucket, key):
    try:
        s3_client.head_object(Bucket=bucket, Key=key)
    except ClientError as e:
        return int(e.response['Error']['Code']) != 404
    return True

def lambda_handler(event, context):
    # API receieves fasta sequence
    body = json.loads(event['body'])
    sequence = body['sequence']

    # SHA1 hash sequence to generate Report ID
    sequence_hash = hashlib.sha1(sequence.encode("utf-8")).hexdigest()

    # Cloudwatch Log
    print(sequence)
    print(sequence_hash)

    # Check if report exists already
    report_exists = check(s3_client, 'openvirome.com', sequence_hash + '.html')

    if report_exists:
        print('Report hash already exists')

    else:
        # Initiate `palmid-lambda` service
        data = json.dumps({"sequence": sequence, "hash": sequence_hash}).encode("utf-8")
        url = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

        response = urllib.request.urlopen(url, data)

        print(response.info())

    # API returns sequence hash
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
        'body': sequence_hash
    }
