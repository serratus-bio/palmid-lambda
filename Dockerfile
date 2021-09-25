# Define function directory
ARG FUNCTION_DIR="/home/palmid/"

FROM python:buster as build-image

# Install aws-lambda-cpp build dependencies
RUN apt-get update && \
  apt-get install -y \
  g++ \
  make \
  cmake \
  unzip \
  libcurl4-openssl-dev

# Include global arg in this stage of the build
ARG FUNCTION_DIR
# Create function directory
RUN mkdir -p ${FUNCTION_DIR}

# Copy function code
COPY app/* ${FUNCTION_DIR}

# Install the runtime interface client
RUN pip install \
        --target ${FUNCTION_DIR} \
        awslambdaric

FROM serratusbio/palmid:latest

ARG FUNCTION_DIR
COPY --from=build-image ${FUNCTION_DIR} ${FUNCTION_DIR}

ENV LAMBDA_TASK_ROOT=./
ENV HOME=/tmp

RUN yum update -y && yum groupinstall -y "Development Tools" && \
  yum install -y \
  cmake3 \
  libcurl-devel \
  python3 \
  python3-devel \
  python3-pip \
  gzip \
  libstdc++ && \
  pip install awslambdaric

# Copy function code
COPY ./app/ ${LAMBDA_TASK_ROOT}

# Install the function's dependencies using file requirements.txt
# from your project folder.
ADD https://github.com/aws/aws-lambda-runtime-interface-emulator/releases/latest/download/aws-lambda-rie /usr/bin/aws-lambda-rie

COPY entry.sh /
COPY requirements.txt  .
RUN pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}" && \
    mkdir -p /tmp/data && mv /usr/bin/python /usr/bin/python2 && ln -sf /usr/bin/python3 /usr/bin/python && ln -sf /usr/bin/python3 /usr/local/bin/python && alias python=python3 && chmod 755 /usr/bin/aws-lambda-rie /entry.sh

ENTRYPOINT [ "/entry.sh" ]
#ENTRYPOINT [ "python3", "-m", "awslambdaric" ]
CMD [ "app.handler" ]