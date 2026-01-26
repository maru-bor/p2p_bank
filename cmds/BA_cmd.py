from cmds.cmd import Command
from cmds.cmd_registry import CommandRegistry


class BACommand(Command):
    def __init__(self, bank):
        self.bank = bank

    def execute(self):
        return f"BA {self.bank.total_amount()}"

CommandRegistry.register("BA", BACommand)
