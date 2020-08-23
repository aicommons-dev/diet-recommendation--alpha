# pull official base image
# FROM python:3.7-alpine
FROM python:3.8-slim-buster

# set work directory
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBUG 0

# install psycopg2
# RUN apk update \
    # && apk --no-cache add musl-dev linux-headers g++
    # build-essential make automake gcc subversion python3-dev libc-dev \
    # && apk add --virtual build-deps gcc python3-dev musl-dev \
    #&& apk add postgresql-dev \
    # && pip install -U pip
    # && pip install psycopg2 \
    #&& apk del build-essential

RUN apt-get update -y \
    && apt-get install --virtual build-deps gcc python3-dev musl-dev py3-zipp \
#    && pip install psycopg2 \
    && apt-get install jpeg-dev zlib-dev libjpeg \
    && pip install Pillow \
    && apt-get del build-deps

RUN pip install --upgrade pip
RUN echo "http://dl-8.alpinelinux.org/alpine/edge/community" >> /etc/apk/repositories
RUN apt-get --no-cache --update-cache add gcc gfortran python3 python3-dev py-pip build-base wget freetype-dev libpng-dev openblas-dev
RUN ln -s /usr/include/locale.h /usr/include/xlocale.h
RUN python3 -m pip install scikit-learn
RUN python3 -m pip install numpy scipy pandas matplotlib

#RUN pip install torch torchvision
# RUN python3 -m pip install torch==1.6.0+cpu torchvision==0.7.0+cpu -f https://download.pytorch.org/whl/torch_stable.html


# RUN python3 -m pip install numpy
RUN python3 -m pip install --pre torch torchvision -f https://download.pytorch.org/whl/nightly/cpu/torch_nightly.html
RUN python3 -m pip install fastai

#RUN apt-get -y install libc-dev
#RUN apt-get -y install build-essential
#RUN pip install -U pip
# install dependencies
# RUN pip install --upgrade numpy
# RUN pip install fastai
COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy project
COPY . .