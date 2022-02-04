FROM python:3.9.10

RUN apt update && apt install -y libeigen3-dev python3-pybind11
RUN git clone https://github.com/artivis/manif.git
RUN cd manif && pip install .
RUN pip install jupyter
RUN pip install numpy
WORKDIR /data

