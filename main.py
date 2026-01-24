from server import BankServer
from libs.pvl_config import load_yaml_config

if __name__ == "__main__":
    cfg = load_yaml_config("config/config.yaml")
    server = BankServer(cfg)
    server.start()