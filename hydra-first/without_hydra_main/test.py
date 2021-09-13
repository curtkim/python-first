from hydra import compose, initialize
from omegaconf import OmegaConf
import os

initialize(config_path=".", job_name="test_app")
cfg = compose(config_name="config", overrides=["db.user=me"])
print(OmegaConf.to_yaml(cfg))
print(os.getcwd())

