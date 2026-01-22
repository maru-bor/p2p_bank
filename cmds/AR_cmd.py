from cmds.cmd import Command

class ARCommand(Command):
    def __init__(self, bank, acct):
        self.bank = bank
        self.acct = acct


    def execute(self):
        self.bank.remove(self.acct)
        return f"AR"