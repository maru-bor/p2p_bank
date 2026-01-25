from bank import Bank
from server import BankServer
from web_monitor import WebMonitor
from logger import Logger
from libs.pvl_config import load_yaml_config
from utils import *

if __name__ == "__main__":
    cfg = load_yaml_config("config/config.yaml")
    own_ip = get_own_ip()

    logger = Logger()


    bank = Bank(
        own_ip,
        cfg["storage"]["data_file"],
        logger
    )

    server = BankServer(cfg, bank, logger)
    monitor = WebMonitor(bank, logger, port=8080)

    monitor.start()
    server.start()
