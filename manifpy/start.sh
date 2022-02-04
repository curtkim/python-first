docker run -it -v $(pwd):/data -p 8888:8888 manifpy jupyter notebook --allow-root --ip=0.0.0.0 --NotebookApp.token=''

