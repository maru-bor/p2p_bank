from cmds.cmd import Command


class BNCommand(Command):
    def __init__(self, bank):
        self.bank = bank

    def execute(self):
        return f"BN {self.bank.number_of_clients()}"