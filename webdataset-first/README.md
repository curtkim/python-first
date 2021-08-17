## prepare

    wget http://storage.googleapis.com/nvdata-openimages/openimages-train-000000.tar
    tar tf openimages-train-000000.tar | wc -l  # 6408

## make tar file

    tar --sort=name -cf voc.tar --directory=data .
    tar tf voc.tar

## tarp docker

    docker build -t tarp .
