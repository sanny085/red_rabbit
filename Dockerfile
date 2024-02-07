FROM python:3.7-alpine
RUN apk add -u zlib-dev jpeg-dev gcc musl-dev linux-headers
RUN python3 -m pip install --upgrade pip
RUN  apk add libffi-dev
RUN apk update
ENV PIP_ROOT_USER_ACTION=ignore
RUN pip3 install --upgrade pip
RUN pip3 install --root-user-action=ignore requests
RUN  pip3 install pika
RUN  pip3 install Flask
RUN  pip3 install pillow
RUN pip3 install pymongo
RUN pip3 install python-dotenv
RUN ln -s /usr/bin/  /usr/bin/python
EXPOSE 5009
EXPOSE 27019
COPY main.py /app/

# COPY segmentation.py /app/
WORKDIR /go/src/zeppelin/app
