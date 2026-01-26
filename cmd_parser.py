import socket
from cmds.BC_cmd import BCCommand
from cmds.BA_cmd import BACommand
from cmds.BN_cmd import BNCommand
from cmds.AC_cmd import ACCommand
from cmds.AD_cmd import ADCommand
from cmds.AW_cmd import AWCommand
from cmds.AB_cmd import ABCommand
from cmds.AR_cmd import ARCommand
from cmds.cmd_registry import CommandRegistry

class CommandParser:
    def __init__(self, own_ip, bank, logger, bank_port):
        self.own_ip = own_ip
        self.bank_port = int(bank_port)
        self.bank = bank
        self.logger = logger

    def _proxy(self, target_ip: str, command_text: str) -> str:
        try:
            with socket.create_connection((target_ip, self.bank_port), timeout=3.0) as s:
                s.sendall(command_text.encode("utf-8") + b"\r\n")
                data = s.recv(4096)
            return data.decode("utf-8").strip()
        except Exception as e:
            self.logger.error(f"ER Proxy error to {target_ip}: {e}")
            return "ER Proxy connection failed."

    def parse_and_execute(self, text: str) -> str:
        text = text.strip()
        self.logger.info(f"USER INPUT: {text}")

        if not text:
            return "ER Empty command."

        parts = text.split(" ", 1)
        cmd_name = parts[0]
        args = parts[1] if len(parts) > 1 else ""

        try:
            cmd_cls = CommandRegistry.get(cmd_name)
            if not cmd_cls:
                self.logger.error(f"Unknown command: {cmd_name}")
                return "ER Unknown command."

            if cmd_name in ["BC", "BA", "BN", "AC"]:
                cmd = cmd_cls(self.own_ip if cmd_name == "BC" else self.bank)
            elif cmd_name in ["AD", "AW", "AB", "AR"]:
                acct_str, rest = args.split("/", 1)
                ip_and_amount = rest.split(" ", 1)
                ip = ip_and_amount[0]
                if ip != self.own_ip:
                    return self._proxy(ip, text)

                acct = int(acct_str)
                if cmd_name in ["AD", "AW"]:
                    amount = int(ip_and_amount[1])
                    cmd = cmd_cls(self.bank, acct, amount)
                else:
                    cmd = cmd_cls(self.bank, acct)
            response = cmd.execute()
            self.logger.info(f"ANSWER: {response}")
            return response
        except Exception as e:
            self.logger.error(str(e))
            return f"ER {e}"