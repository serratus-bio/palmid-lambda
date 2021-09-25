FROM serratusbio/palmid:latest

ENV LAMBDA_TASK_ROOT=./

# Copy function code
COPY ./app/app.py ${LAMBDA_TASK_ROOT}

# Install the function's dependencies using file requirements.txt
# from your project folder.

COPY requirements.txt  .
RUN pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}" && \
    mkdir -p /tmp/data

CMD [ "app.handler" ]