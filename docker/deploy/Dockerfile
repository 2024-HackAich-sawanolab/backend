FROM python:3.8

RUN apt update \
    && apt install -y default-mysql-client \
    && apt install --no-install-recommends -y tzdata \
    && apt clean

WORKDIR /usr/src
COPY app /usr/src/app
COPY db /usr/src/db 
COPY scripts /usr/src/scripts

COPY docker/deploy/requirements.txt /usr/src/app/requirements.txt

WORKDIR /usr/src/app
ADD docker/deploy/requirements.txt .
RUN pip install -U pip \
    && pip install --trusted-host pypi.python.org -r requirements.txt

ENV PYTHONPATH=/usr/src/app

# run Scripts/run.sh
CMD ["sh", "/usr/src/scripts/run.sh"]

