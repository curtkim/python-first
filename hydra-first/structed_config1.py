from dataclasses import dataclass

import hydra
from hydra.core.config_store import ConfigStore

@dataclass
class MySQLConfig:
    host: str = "localhost"
    port: int = 3306

cs = ConfigStore.instance()
# Registering the Config class with the name 'config'.
cs.store(name="config", node=MySQLConfig)

@hydra.main(config_name="config")
def my_app(cfg: MySQLConfig) -> None:
    # pork should be port!
    #print(cfg) # {'host': 'localhost', 'port': 3306}
    if cfg.pork == 80:
        print("Is this a webserver?!")

if __name__ == "__main__":
    my_app()


# python structed_config1.py port=80
# Is this a webserver?!

