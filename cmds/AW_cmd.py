from cmds.cmd import Command
from cmds.cmd_registry import CommandRegistry


class AWCommand(Command):
    def __init__(self, bank, acct, amount):
        self.bank = bank
        self.acct = acct
        self.amount = amount


    def execute(self):
        self.bank.withdraw(self.acct, self.amount)
        return f"AW"

CommandRegistry.register("AW", AWCommand)