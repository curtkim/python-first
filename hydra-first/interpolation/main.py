import hydra
import logging
from omegaconf import DictConfig, OmegaConf

@hydra.main(config_name="config")
def main_func(cfg: DictConfig):
    server_address = cfg.server.address
    print(f"The server address = {server_address}")


# python main.py server.port=10
# The server address = 127.0.0.1:10

if __name__ == "__main__":
    main_func()

