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

    result_file = analyze_sequence(event['sequence'])

    result_filename = put_report_to_s3(event['hash'], result_file)

    return result_filename


def analyze_sequence(sequence):
    text_file = open("/tmp/waxsys.fa", "w")
    text_file.write(sequence)
    text_file.close()

    subprocess.call(['sh', '/home/palmid/palmid.sh', '-i', '/tmp/waxsys.fa', '-o', 'waxsys', '-d', '/tmp/data'])

    result_html = "/tmp/data/waxsys.nb.html"
    return result_html


def put_report_to_s3(filename, file):
    result_filename = filename + '.html'
    with open(file) as f:
        string = f.read()

    encoded_string = string.encode("utf-8")
    s3 = boto3.resource("s3")
    s3.Bucket('openvirome.com').put_object(Key=result_filename, Body=encoded_string, ContentType='text/html')
    return result_filename
