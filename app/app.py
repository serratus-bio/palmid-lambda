# from flask import Flask
#
# app = Flask(__name__)
#
# @app.route('/')
# def hello_world():
#     return 'Hello World!'
#
# if __name__ == '__main__':
#     app.run()

import sys
import os
import subprocess

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
    dirlist = os.listdir("./data")

    return 'Hello from AWS Lambda using Python' + sys.version + '! '+dirlist