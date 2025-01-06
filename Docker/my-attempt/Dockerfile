# All below links reference code that was used to help build al docker related files
#https://github.com/jgeorg02/docker-raspbian-picamera2
#https://www.prefect.io/blog/dockerizing-python-applications
#https://raspberrytips.com/docker-on-raspberry-pi/
#Base image to use
FROM navikey/raspbian-bullseye:latest

#Directory created inside container
RUN mkdir /usr/src/app

#Updating packages and then install dependenices for python library picamera2
RUN apt-get update && \
    apt-get install -y \
    python3 \
    python3-pip \
    && pip install --upgrade pip \
    && apt install -y python3-picamera2 --no-install-recommends \
    # gcc \
    # build-essential \
    # libcap-dev \
    # libcamera-dev \
    # meson \
    # ninja-build \
    # git \
    && rm -rf /var/lib/apt/lists/*

#Copies everything into the directory inside of the container
COPY . /usr/src/app

#Directory container is looking at when created
WORKDIR /usr/src/app

#Installing python dependencies
#RUN pip install --no-cache-dir -r requirements.txt

#Execute the file from inside of the container.
#CMD ["python", "./camera_photo.py"]
