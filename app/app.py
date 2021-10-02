import boto3
import os
import subprocess

def handler(event, context):
    print('## ENVIRONMENT VARIABLES')
    print(os.environ)
    print('## EVENT')
    print(event)
    print('## CONTEXT')
    print(context)

    result_file = analyze_sequence(event['sequence'], event['hash'])

    result_filename = put_report_to_s3(event['hash'], result_file)

    return result_filename


def analyze_sequence(sequence, fahash):
    text_file = open("/tmp/submission.fa", "w")
    text_file.write(sequence)
    text_file.close()

    # Copy input file to S3
    result_filename = 'input/' + fahash + '.fa'
    with open("/tmp/submission.fa") as f:
        string = f.read()

    encoded_string = string.encode("utf-8")
    s3 = boto3.resource("s3")
    s3.Bucket('openvirome.com').put_object(Key=result_filename, Body=encoded_string, ContentType='text/html')

    # Run palmID container
    subprocess.call(['sh', '/home/palmid/palmid.sh', '-i', '/tmp/submission.fa', '-o', 'submission', '-d', '/tmp'])

    result_html = "/tmp/submission.nb.html"
    return result_html


def put_report_to_s3(fahash, file):
    result_filename = fahash + '.html'
    with open(file) as f:
        string = f.read()

    encoded_string = string.encode("utf-8")
    s3 = boto3.resource("s3")
    s3.Bucket('openvirome.com').put_object(Key=result_filename, Body=encoded_string, ContentType='text/html')
    return result_filename
