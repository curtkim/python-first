from hydra import compose, initialize
from omegaconf import OmegaConf
import os
import sys

if __name__ == '__main__':
    initialize(config_path=".", job_name="test_app")
    cfg = compose(config_name="config", overrides=["db.user=me", "db.pass=pass"])
    print(OmegaConf.to_yaml(cfg))
    print('pwd=', os.getcwd())

    print('sys.argv=', sys.argv)
    cfg = compose(config_name="config", overrides=sys.argv[1:])
    print(OmegaConf.to_yaml(cfg))

