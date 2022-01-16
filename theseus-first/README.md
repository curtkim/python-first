## SuiteSparse install

    sudo apt-get install libgmp3-dev libmpc-dev

    git clone https://github.com/DrTimothyAldenDavis/SuiteSparse.git
    cd SuiteSparse
    make CUDA=no -j
    sudo make install INSTALL=/usr/local/
    LD_LIBRARY_PATH=/usr/local/lib/:$LD_LIBRARY_PATH


