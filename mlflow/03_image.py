import os
from random import random, randint
from mlflow import log_metric, log_param, log_artifacts
import matplotlib.pyplot as plt

from PIL import Image
import numpy as np

import mlflow
mlflow.set_tracking_uri("http://localhost:5000")
mlflow.set_experiment("my-experiment")


if __name__ == "__main__":
    # Log a parameter (key-value pair)
    log_param("param1", randint(0, 100))

    # Log a metric; metrics can be updated throughout the run
    log_metric("foo", random())
    log_metric("foo", random() + 1)
    log_metric("foo", random() + 2)

    image = Image.new("RGB", (100, 100))
    mlflow.log_image(image, "image.png")

    numpy_image = np.random.randint(0, 256, size=(100, 100, 3), dtype=np.uint8)
    mlflow.log_image(numpy_image, "numpy_image.png")

