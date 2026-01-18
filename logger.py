import logging

class Logger:
    _instance = None

    def __new__(cls, log_file="bank_node.log"):
        if cls._instance is None:
            cls._instance = super().__new__(cls)

            logging.basicConfig(
                filename=log_file,
                level=logging.INFO,
                format="%(asctime)s - %(levelname)s - %(message)s",
            )
            cls._instance.logger = logging.getLogger("BankNode")

        return cls._instance

    def info(self, msg):
        self.logger.info(msg)

    def error(self, msg):
        self.logger.error(msg)
