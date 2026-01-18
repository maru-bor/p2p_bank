from cmds.cmd import Command

class BCCommand(Command):
    def __init__(self, own_ip):
        self.own_ip = own_ip

    def execute(self):
        return f"BC {self.own_ip}"