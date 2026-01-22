from cmds.cmd import Command

class BACommand(Command):
    def __init__(self, bank):
        self.bank = bank

    def execute(self):
        return f"BA {self.bank.total_amount()}"
