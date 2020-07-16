FROM python:3.7

WORKDIR /home

# django docker environment
RUN apt-get update
COPY requirements.txt /home/requirements.txt
RUN pip install -r requirements.txt

RUN apt install -y default-jre

RUN rm /bin/sh && ln -s /bin/bash /bin/sh
VOLUME ["/home"]
COPY . .

RUN chmod +x /home/entrypoint.sh

EXPOSE 8080
ENTRYPOINT [ "/home/entrypoint.sh" ]
