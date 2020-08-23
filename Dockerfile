# pull official base image
# FROM python:3.7-alpine
FROM python:3.8-slim-buster as stage1

# set work directory
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBUG 1

#RUN apt-get update -y
#RUN apt-get -y install libc-dev
#RUN apt-get -y install build-essential

RUN apt-get update
RUN apt-get -y install make
# RUN pip install --upgrade pip
RUN python3 -m pip install torch==1.6.0+cpu torchvision==0.7.0+cpu -f https://download.pytorch.org/whl/torch_stable.html
# RUN python3 -m pip install fastai


COPY ./requirements.txt .
RUN python3 -m pip install -r requirements.txt

RUN make DESTDIR=/tmp install

# stage2
FROM python:3.7-alpine
# copy project
COPY --from=stage1 /tmp /app
ENTRYPOINT ["/app"]