import socket

from bank import Bank
from cmds.AC_cmd import ACCommand
from cmds.BA_cmd import BACommand
from cmds.BN_cmd import BNCommand
from cmds.AR_cmd import ARCommand
from cmds.AB_cmd import ABCommand
from cmds.AD_cmd import ADCommand
from cmds.AW_cmd import AWCommand
from logger import Logger
from cmds.BC_cmd import BCCommand


class CommandParser:
    def __init__(self, own_ip, store_path, bank_port: int):
        self.own_ip = own_ip
        self.bank_port = int(bank_port)
        self.logger = Logger()
        self.bank = Bank(own_ip, store_path, self.logger)

    def _proxy(self, target_ip: str, command_text: str) -> str:
        with socket.create_connection((target_ip, self.bank_port), timeout=3.0) as s:
            s.sendall(command_text.encode("utf-8") + b"\r\n")
            data = s.recv(4096)
        try:
            return data.decode("utf-8").strip()
        except UnicodeDecodeError:
            return "ER Proxy decode error."

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

        elif text.startswith("AR "):
            try:
                _, rest = text.split(" ", 1)
                acct_str, ip = rest.split("/", 1)

                if ip != self.own_ip:
                    return self._proxy(ip, text)

                acct = int(acct_str)
                cmd = ARCommand(self.bank, acct)
                response = cmd.execute()
                self.logger.info(f"ANSWER: {response}")
                return response

            except ValueError:
                return "ER Invalid account format."
            except Exception as e:
                self.logger.error(str(e))
                return f"ER {e}"

        elif text.startswith("AB "):
            try:
                _, rest = text.split(" ", 1)
                acct_str, ip = rest.split("/", 1)

                if ip != self.own_ip:
                    return self._proxy(ip, text)

                acct = int(acct_str)
                cmd = ABCommand(self.bank, acct)
                response = cmd.execute()
                self.logger.info(f"ANSWER: {response}")
                return response

            except ValueError:
                return "ER Invalid account format."
            except Exception as e:
                self.logger.error(str(e))
                return f"ER {e}"

        elif text.startswith("AD "):
            try:
                _, rest = text.split(" ", 1)
                acct_str, rest2 = rest.split("/", 1)
                ip, amount_str = rest2.split(" ", 1)

                if ip != self.own_ip:
                    return self._proxy(ip, text)

                acct = int(acct_str)
                amount = int(amount_str)
                cmd = ADCommand(self.bank, acct, amount)
                response = cmd.execute()
                self.logger.info(f"ANSWER: {response}")
                return response

            except ValueError:
                return "ER Invalid command format."
            except Exception as e:
                self.logger.error(str(e))
                return f"ER {e}"

        elif text.startswith("AW "):
            try:
                _, rest = text.split(" ", 1)
                acct_str, rest2 = rest.split("/", 1)
                ip, amount_str = rest2.split(" ", 1)

                if ip != self.own_ip:
                    return self._proxy(ip, text)

                acct = int(acct_str)
                amount = int(amount_str)
                cmd = AWCommand(self.bank, acct, amount)
                response = cmd.execute()
                self.logger.info(f"ANSWER: {response}")
                return response

            except ValueError:
                return "ER Invalid command format."
            except Exception as e:
                self.logger.error(str(e))
                return f"ER {e}"

        error_msg = "ER Unknown command."
        self.logger.error(f"ERROR: {error_msg}")
        return error_msg