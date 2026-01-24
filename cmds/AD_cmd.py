from cmds.cmd import Command

class ADCommand(Command):
    def __init__(self, bank, acct, amount):
        self.bank = bank
        self.acct = acct
        self.amount = amount


    def execute(self):
        self.bank.deposit(self.acct, self.amount)
        return f"AD"