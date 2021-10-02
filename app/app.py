import boto3
import os
import subprocess

def handler(event, context):
    print('')
    print('########### PALMID-LAMBDA ###########')
    print('')
    print('## ENVIRONMENT VARIABLES')
    print(os.environ)
    print('')
    print('## EVENT')
    print('')
    print(event)
    print('')
    print('## CONTEXT')
    print('')
    print(context)
    print('')

    input_fasta = write_fasta(event['sequence'])

    upload_fasta = put_fasta_to_s3(event['hash'], input_fasta)

    result_html = analyze_sequence(input_fasta)

    report_filename = put_report_to_s3(event['hash'], result_html)

    return report_filename

def write_fasta(sequence):
    input_fasta = "/tmp/submission.fa"


    text_file = open(input_fasta, "w")
    text_file.write(sequence)
    text_file.close()

    return input_fasta

def put_fasta_to_s3(fahash, input_fasta):
    s3_input_filename = "input/" + fahash + '.fa'
    with open(input_fasta) as f:
        string = f.read()

    print("Uploading " + input_fasta + " to s3://openvirome.com/" + s3_input_filename)

    encoded_string = string.encode("utf-8")
    s3 = boto3.resource("s3")
    s3.Bucket('openvirome.com').put_object(Key=s3_input_filename, Body=encoded_string, ContentType='text/plain')
    return s3_input_filename


def analyze_sequence(input_fasta):
    print('')
    subprocess.call(['sh', '/home/palmid/palmid.sh', '-i', '/tmp/submission.fa', '-o', 'submission', '-d', '/tmp'])
    print('')

    result_html = "/tmp/submission.nb.html"
    return result_html


def put_report_to_s3(fahash, file):
    report_filename = fahash + '.html'
    with open(file) as f:
        string = f.read()

    print("Uploading " + file + " to s3://openvirome.com/" + report_filename)

    encoded_string = string.encode("utf-8")
    s3 = boto3.resource("s3")
    s3.Bucket('openvirome.com').put_object(Key=report_filename, Body=encoded_string, ContentType='text/html')
    return report_filename
