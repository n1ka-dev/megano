FROM python:3.8-alpine
ENV PROJECT=megano
ENV CONTAINER_HOME=/django
ENV CONTAINER_PROJECT=$CONTAINER_HOME/$PROJECT

# Create application subdirectories
WORKDIR $CONTAINER_HOME
# Copy application source code to $CONTAINER_PROJECT
COPY . $CONTAINER_PROJECT

# Install Python dependencies
ENV PYTHONUNBUFFERED 1
RUN apk add --update --no-cache postgresql-client jpeg-dev
RUN apk add --update --no-cache --virtual .tmp-build-deps \
    gcc libc-dev linux-headers postgresql-dev musl-dev zlib zlib-dev
RUN pip3 install --upgrade pip && pip install -r $CONTAINER_PROJECT/requirements.txt
RUN apk del .tmp-build-deps

WORKDIR $CONTAINER_PROJECT