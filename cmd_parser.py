from bank import Bank
from cmds.AC_cmd import ACCommand
from cmds.BA_cmd import BACommand
from cmds.BN_cmd import BNCommand
from logger import Logger
from cmds.BC_cmd import BCCommand

class CommandParser:
    def __init__(self, own_ip):
        self.own_ip = own_ip
        self.logger = Logger()
        self.bank = Bank(own_ip, "bank_data.json", self.logger)

    def parse_and_execute(self, text: str) -> str:
        text = text.strip()
        self.logger.info(f"USER INPUT: {text}")

        if text == "BC":
            cmd = BCCommand(self.own_ip)
            response = cmd.execute()
            self.logger.info(f"ANSWER: {response}")
            return response
        elif text == "BA":
            cmd = BACommand(self.bank)
            response = cmd.execute()
            self.logger.info(f"ANSWER: {response}")
            return response
        elif text == "BN":
            cmd = BNCommand(self.bank)
            response = cmd.execute()
            self.logger.info(f"ANSWER: {response}")
            return response
        elif text == "AC":
            cmd = ACCommand(self.bank)
            response = cmd.execute()
            self.logger.info(f"ANSWER: {response}")
            return response

        error_msg = "ER Unknown command."
        self.logger.error(f"ERROR: {error_msg}")
        return error_msg