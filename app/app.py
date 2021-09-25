import sys
import os
import subprocess
import base64
import json


def handler(event, context):
    print('## ENVIRONMENT VARIABLES')
    print(os.environ)
    print('## EVENT')
    print(event)
    print('## CONTEXT')
    print(context)

    text_file = open("./waxsys.fa", "w")
    text_file.write(event['sequence'])
    text_file.close()
    try:
        os.makedirs('./data')
    except OSError:
        pass

    subprocess.call(['sh', '/home/palmid/palmid.sh', '-i', './waxsys.fa', '-o', './data'])
    html_report = open("./data/waxsys_geo.html", "rb").read()
    return base64.b64encode(html_report)
