FROM python:3.13-alpine

WORKDIR /usr/src/app

RUN apk update && \
    apk add --no-cache \
        build-base \
        python3-dev \
        linux-headers \
        gdal \
        gdal-dev \
        geos \
        geos-dev \
        proj \
        proj-dev \
        freetype \
        freetype-dev \
        jpeg \
        jpeg-dev \
        zlib \
        zlib-dev \
        libpng \
        libpng-dev \
        openblas \
        openblas-dev && \
    rm -rf /var/cache/apk/* 

COPY ./dash-t2/requirements.txt ./
RUN  pip install --no-cache-dir -r requirements.txt

COPY ./dash-t2 .

CMD [ "python", "./app.py" ]