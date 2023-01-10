# Realtime Object Detection App

## 1. Install

### Build docker image

You can use `Docker` to install all the needed packages and libraries easily. Two Dockerfiles are provided for both CPU and GPU support.

- **CPU:**

```bash
$ docker build -t rt_obj_detect_webapp --build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g) -f docker/Dockerfile .
```

- **GPU:**

```bash
$ docker build -t rt_obj_detect_webapp --build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g) -f docker/Dockerfile_gpu .
```

## 2. Start Web Application

- **CPU:**

```bash
$ docker run --rm --net host -it -v "$(pwd)/src":/home/app/src --workdir /home/app/src rt_obj_detect_webapp
```

- **GPU:**

```bash
$ docker run --rm --gpus all -it -p 127.0.0.1:8080:5000 -v "$(pwd)/src":/home/app/src --workdir /home/app/src rt_obj_detect_webapp
```

This web application gets video feed from client's camera and runs yolov5 object detection at 1 FPS rate.