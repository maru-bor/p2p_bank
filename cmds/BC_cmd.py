from cmds.cmd import Command
from cmds.cmd_registry import CommandRegistry


class BCCommand(Command):
    def __init__(self, own_ip):
        self.own_ip = own_ip

    def execute(self):
        return f"BC {self.own_ip}"
CommandRegistry.register("BC", BCCommand)