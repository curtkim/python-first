import hydra
from omegaconf import DictConfig, OmegaConf
from user import User

@hydra.main(config_name='conf')
def my_app(cfg: DictConfig) -> None:
    print(OmegaConf.to_yaml(cfg))

    user1 : User = hydra.utils.instantiate(cfg.bond)
    assert isinstance(user1, User)
    assert user1.name == "Bond"
    assert user1.age == 7    


if __name__ == "__main__":
    my_app()