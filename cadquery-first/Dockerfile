FROM continuumio/miniconda3:latest

# Dependencies for glvnd and X11.
RUN apt-get update \
  && apt-get install -y -qq --no-install-recommends \
    libglvnd0 \
    libgl1 \
    libglx0 \
    libegl1 \
    libxext6 \
    libx11-6 \
  && rm -rf /var/lib/apt/lists/*
# Env vars for the nvidia-container-runtime.
ENV NVIDIA_VISIBLE_DEVICES all
ENV NVIDIA_DRIVER_CAPABILITIES graphics,utility,compute

RUN apt-get update \
  && apt-get install -y qt5-default

RUN conda install -c cadquery -c conda-forge cq-editor=master

RUN useradd -ms /bin/bash curt
USER curt

# docker build -t cqeditor .
# docker run --rm -it --gpus all -v /tmp/.X11-unix:/tmp/.X11-unix -e DISPLAY=$DISPLAY -e QT_X11_NO_MITSHM=1 cqeditor bash