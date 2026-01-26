from bank import Bank
from server import BankServer
from ui.web_monitor import WebMonitor
from logger import Logger
from libs.pvl_config import ConfigLoader, ConfigError
from utils import *

if __name__ == "__main__":
    try:
        cfg = ConfigLoader.load_yaml_config("config/config.yaml")
    except ConfigError as e:
        print(f"CONFIG ERROR: {e}")
        exit(1)

    own_ip = get_own_ip()

    logger = Logger()

    bank = Bank(
        own_ip,
        cfg["storage"]["data_file"],
        logger
    )

    server = BankServer(cfg, bank, logger)
    monitor = WebMonitor(bank, server, logger, "0.0.0.0", 8080)

    monitor.start()
    server.start()
