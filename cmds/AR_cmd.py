from cmds.cmd import Command
from cmds.cmd_registry import CommandRegistry


class ARCommand(Command):
    def __init__(self, bank, acct):
        self.bank = bank
        self.acct = acct


    def execute(self):
        self.bank.remove(self.acct)
        return f"AR"

CommandRegistry.register("AR", ARCommand)