#A Dockerfile is a file that contains a list of instructions for Docker to build our Docker image
#You describe all your dependencies that you need for your project in your Docker file
#1.Line: Image our Image is based on
FROM python:3.7-alpine
#2. Line: Who is the Maintainer of the image? => optional
MAINTAINER Bumba2

#Set the PythonUnbuffered-Environment Variable
#Here = 1 => it tells Python to run in unbuffered mode, which is recommended when running python within docker containers
#It doesnt allow python to buffer the outputs, but print them directly which avoid some complications with the Docker image
ENV PYTHONUNBUFFERED 1

#Store dependencies in a requirements.txt file. Copy it to the Docker image
COPY ./requirements.txt /requirements.txt
#Take the requirements.txt file that we copies before and install it using pip into the Docker image
RUN python3 -m pip install -r /requirements.txt

#Make a directory within our Docker image in which we store our application source code.
#Make an empty Folder app, switch to it as the default location and copy it to the Docker image
RUN mkdir /app
WORKDIR /app
COPY ./app /app

#Create a user wit the name user which is going to run the application. -D => user can run applications only.
RUN adduser -D user
#We switch to that user
USER user