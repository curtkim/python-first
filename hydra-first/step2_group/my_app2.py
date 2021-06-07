import hydra
from omegaconf import DictConfig, OmegaConf

@hydra.main(config_path="conf")
def my_app(cfg : DictConfig) -> None:
    print(OmegaConf.to_yaml(cfg))

if __name__ == "__main__":
    my_app()

'''
$ python my_app.py
{}


$ python my_app2.py +db=mysql
db:
  driver: mysql
  user: omry
  pass: secret


$ python my_app2.py +db=postgres db.timeout=20
db:
  driver: postgresql
  pass: drowssap
  timeout: 20
  user: postgre_user


'''