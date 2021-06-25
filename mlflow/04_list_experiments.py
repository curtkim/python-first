import os
from random import random, randint
from mlflow import log_metric, log_param, log_artifacts
from mlflow.entities import ViewType
from mlflow.tracking import MlflowClient

from PIL import Image
import numpy as np

import mlflow
mlflow.set_tracking_uri("http://localhost:5000")
mlflow.set_experiment("my-experiment")


if __name__ == "__main__":
    experiments = mlflow.list_experiments()
    for ex in experiments:
        print(ex)

    runs = mlflow.list_run_infos("1", run_view_type=ViewType.ALL)
    for run_info in runs:
        print(run_info)
        run = mlflow.get_run(run_info.run_id)
        print("metrics: {}".format(run.data.metrics))
        artifacts = [f.path for f in MlflowClient().list_artifacts(run_info.run_id)]
        print(artifacts)

