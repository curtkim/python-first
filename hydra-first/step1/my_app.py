import hydra
from omegaconf import DictConfig, OmegaConf


@hydra.main(config_path=".", config_name="config")
def my_app(cfg : DictConfig) -> None:
    print(OmegaConf.to_yaml(cfg))
    
    print(cfg.db)
    print(cfg.db.tables)                # ['a', 'b', 'c', 'd', 'e']
    print(type(cfg.db.tables))
    print(cfg.db.mappings)              # {'a': 1, 'b': 2, 'c': 3}
    print(type(cfg.db.mappings))


if __name__ == "__main__":
    my_app()
