from cmds.cmd import Command

class ABCommand(Command):
    def __init__(self, bank, acct):
        self.bank = bank
        self.acct = acct


    def execute(self):
        balance = self.bank.balance(self.acct)
        return f"AB {balance}"