import hydra
from omegaconf import DictConfig, OmegaConf


@hydra.main(config_path=".", config_name="config")
def my_app(cfg: DictConfig) -> None:
    print(OmegaConf.to_yaml(cfg, resolve=True))
    print(cfg.db.user)


if __name__ == "__main__":
    my_app()

# USER=abc python my_app.py
# python my_app.py db.user=curt
