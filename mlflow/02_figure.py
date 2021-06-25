import os
from random import random, randint
from mlflow import log_metric, log_param, log_artifacts
import matplotlib.pyplot as plt

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

    fig, ax = plt.subplots()
    ax.plot([0, 1], [2, 3])
    mlflow.log_figure(fig, "figure.png")
    
