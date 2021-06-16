import hydra
from omegaconf import DictConfig, OmegaConf

@hydra.main(config_name="config")
def my_app(cfg : DictConfig) -> None:
    print(OmegaConf.to_yaml(cfg))
    
    print(cfg.db)
    print(cfg.db.tables)
    print(type(cfg.db.tables))
    print(cfg.db.mappings)
    print(type(cfg.db.mappings))


if __name__ == "__main__":
    my_app()