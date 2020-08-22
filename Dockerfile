# pull official base image
FROM python:3.7-alpine

# set work directory
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBUG 0

# install psycopg2
RUN apk update \
    && apk --no-cache add musl-dev linux-headers g++ \
    # build-essential make automake gcc subversion python3-dev libc-dev \
    # && apk add --virtual build-deps gcc python3-dev musl-dev \
    #&& apk add postgresql-dev \
    && pip install -U pip
    # && pip install psycopg2 \
    #&& apk del build-essential

RUN echo "http://dl-8.alpinelinux.org/alpine/edge/community" >> /etc/apk/repositories
RUN apk --no-cache --update-cache add gcc gfortran python3 python3-dev py-pip build-base wget freetype-dev libpng-dev openblas-dev
RUN ln -s /usr/include/locale.h /usr/include/xlocale.h
RUN pip install numpy scipy pandas matplotlib
RUN pip install torch torchvision
RUN pip install fastai



#RUN apt-get -y install libc-dev
#RUN apt-get -y install build-essential
#RUN pip install -U pip
# install dependencies
# RUN pip install --upgrade numpy
# RUN pip install torch==1.6.0+cpu torchvision==0.7.0+cpu -f https://download.pytorch.org/whl/torch_stable.html
# RUN pip install fastai
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . .

RUN ls foodie/foodie