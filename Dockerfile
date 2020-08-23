# pull official base image
# FROM python:3.7-alpine
FROM python:3.8-slim-buster

# set work directory
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBUG 0

RUN apt-get update -y
RUN apt-get -y install libc-dev
RUN apt-get -y install build-essential

RUN pip install --upgrade pip
RUN python3 -m pip install scikit-learn
RUN python3 -m pip install numpy scipy pandas matplotlib

RUN python3 -m pip install torch==1.6.0+cpu torchvision==0.7.0+cpu -f https://download.pytorch.org/whl/torch_stable.html

#RUN python3 -m pip install --pre torch torchvision -f https://download.pytorch.org/whl/nightly/cpu/torch_nightly.html
RUN python3 -m pip install fastai


COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy project
COPY . .

CMD gunicorn --chdir ./foodie foodie.wsgi --bind 0.0.0.0:$PORT