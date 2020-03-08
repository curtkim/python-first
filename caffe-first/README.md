## howto

    ./download_model_binary.py models/bvlc_reference_caffenet
    docker run --gpus all -v $(pwd):/workspace -it bvlc/caffe:gpu python test.py

    281
    ['n02123045 tabby, tabby cat' 'n02123159 tiger cat'
    'n02124075 Egyptian cat' 'n02119022 red fox, Vulpes vulpes'
    'n02127052 lynx, catamount']