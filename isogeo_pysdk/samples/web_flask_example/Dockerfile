FROM python:3.6
ENV PYTHONUNBUFFERED 1

MAINTAINER Julien M. "julien.moura@isogeo.fr"
LABEL Name="Isogeo oAuth2 User Sample web"
LABEL Description="Image to demonstrate user authentication (oAuth2) mecanism to Isogeo API."
LABEL Vendor="Isogeo"

# Update the default application repository sources list
RUN apt-get update && apt-get upgrade -y

# APP FILES
RUN mkdir /app
COPY . /app
WORKDIR /app

# APP PREREQUISITES
RUN pip install --upgrade -r requirements.txt

# SET ENV VAR
ENV DOCKER_CONTAINER=1

# RUN
CMD ["python",  "runserver.py"]
