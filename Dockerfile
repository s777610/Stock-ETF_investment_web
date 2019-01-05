FROM ubuntu:latest
RUN apt-get update \
    && apt-get install -y python3-pip python3-dev \
    && cd /usr/local/bin \
    && ln -s /usr/bin/python3 python \
    && pip3 install --upgrade pip
ENV EMAIL_USERNAME=2018singcolor@gmail.com
ENV EMAIL_PASSWORD=singcolor2018
WORKDIR "/app"
COPY ./requirements.txt ./
RUN pip install -r requirements.txt
COPY ./.env ./
COPY src/ ./
EXPOSE 5000
CMD ["python", "application.py"]
