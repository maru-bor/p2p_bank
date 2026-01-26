from cmds.cmd import Command
from cmds.cmd_registry import CommandRegistry



class ACCommand(Command):
    def __init__(self, bank):
        self.bank = bank

    def execute(self):
        account_id = self.bank.create_account()
        return f"AC {account_id}/{self.bank.bank_ip}"

CommandRegistry.register("AC", ACCommand)