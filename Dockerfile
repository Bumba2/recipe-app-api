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
#install PostgreSQL Client: It uses the package manager which comes with alpine, and it says this is the name of the package manager "apk", we are gonna add a package, update the registry before we add it, dont store the registry the registry index on our docker file
#We do this because best practice is to minimize the number of extra files and packages that are included in our docker container.
RUN apk add --update --no-cache postgresql-client
#add some temporary files (and delete them after we need them). "virtual" sets up an alias with name ".tmp-build-deps" => temporary build dependencies.
# \ => newline. And then list all temporary dependencies that are required for installing our python dependencies.
RUN apk add --update --no-cache --virtual .tmp-build-deps \
        gcc libc-dev linux-headers postgresql-dev
#Take the requirements.txt file that we copies before and install it using pip into the Docker image
RUN python3 -m pip install -r /requirements.txt
#delete the temporary requirements
RUN apk del

#Make a directory within our Docker image in which we store our application source code.
#Make an empty Folder app, switch to it as the default location and copy it to the Docker image
RUN mkdir /app
WORKDIR /app
COPY ./app /app

#Create a user wit the name user which is going to run the application. -D => user can run applications only.
RUN adduser -D user
#We switch to that user
USER user