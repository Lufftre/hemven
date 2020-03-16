FROM ubuntu
WORKDIR /app
COPY src ./
RUN apt-get update
RUN apt-get -y install curl
CMD [ "bash", "download_slutpris.sh" ]