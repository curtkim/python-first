## prepare

    wget http://storage.googleapis.com/nvdata-openimages/openimages-train-000000.tar
    tar tf openimages-train-000000.tar | wc -l  # 6408
    tar tf openimages-train-000001.tar | wc -l  # 6380


## make tar file

    # 압축하지 않는다.
    tar --sort=name -cf voc.tar --directory=data .
    tar tf voc.tar

## tarp docker

    docker build -t tarp .
