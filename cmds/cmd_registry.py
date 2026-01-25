class CommandRegistry:
    _registry = {}

    @classmethod
    def register(cls, command_name: str, command_cls):
        cls._registry[command_name.upper()] = command_cls

    @classmethod
    def get(cls, command_name: str):
        return cls._registry.get(command_name.upper())