FROM pytorch/pytorch:1.6.0-cuda10.1-cudnn7-devel

ARG DEBIAN_FRONTEND=noninteractive

# our binary versions where applicable
ENV USD_VERSION="21.05"

# Update the environment path
ENV USD_BUILD_PATH="/usr/src/app/xrutils/usd"
ENV USD_PLUGIN_PATH="/usr/src/app/xrutils/usd/plugin/usd"
ENV USD_BIN_PATH="${USD_BUILD_PATH}/bin"
ENV USD_LIB_PATH="${USD_BUILD_PATH}/lib"
ENV PATH="${PATH}:${USD_BIN_PATH}"
ENV LD_LIBRARY_PATH="${LD_LIBRARY_PATH}:${USD_LIB_PATH}"
ENV PYTHONPATH="${PYTHONPATH}:${USD_LIB_PATH}/python"

WORKDIR /usr/src/app

# Required for compiling the USD source
RUN apt-get update && apt-get install -y --no-install-recommends \
	git \
	build-essential \
	nasm \
	libglew-dev \
	libxrandr-dev \
	libxcursor-dev \
	libxinerama-dev \
	libxi-dev \
	zlib1g-dev \
	wget 

RUN apt-get install -y libssl-dev

RUN wget -q https://cmake.org/files/v3.16/cmake-3.16.2.tar.gz && \
    tar -xvzf cmake-3.16.2.tar.gz && \
    cd cmake-3.16.2 && \
    ./bootstrap --prefix=/usr/local && \
    make -j && \
    make install 

RUN rm -rf /var/lib/apt/lists/* && \
	# this is needed for generating usdGenSchema
	pip install -U Jinja2 && \
	# Clone, setup and compile the Pixar USD Converter. This is required
	# for converting GLTF2->USDZ
	# More info @ https://github.com/PixarAnimationStudios/USD
	mkdir xrutils && \
	git clone https://github.com/PixarAnimationStudios/USD usdsrc && \
	cd usdsrc && git checkout tags/v${USD_VERSION} && cd ../ && \
	python usdsrc/build_scripts/build_usd.py -v --no-usdview ${USD_BUILD_PATH} 
	
	#rm -rf usdsrc && \
	## remove build files we no longer need to save space
	#rm -rf ${USD_BUILD_PATH}/build && \
	#rm -rf ${USD_BUILD_PATH}/cmake && \
	#rm -rf ${USD_BUILD_PATH}/pxrConfig.cmake && \
	#rm -rf ${USD_BUILD_PATH}/share && \
	#rm -rf ${USD_BUILD_PATH}/src 

RUN pip install cython scipy Pillow
ENV TORCH_CUDA_ARCH_LIST="7.5"
ENV KAOLIN_INSTALL_EXPERIMENTAL=1
RUN git clone --recursive https://github.com/NVIDIAGameWorks/kaolin && \
	cd kaolin && \
	python setup.py develop 

RUN pip install jupyter matplotlib 
