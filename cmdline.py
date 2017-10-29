class Command:
    """
    The definition of a command line command, allows specification of the command itself
    the options it expects and also optional arguments
    """
    def __init__(self, description):
        self.description = description


class CommandNotFoundError(Exception):
    pass


class CommandParser:
    """
    Parses input from the user based on a set of registered commands
    """
    def __init__(self, registered_commands={}):
        self._registered_commands = registered_commands

    def register_command(self, command, implementation):
        """
        Registers the command in the command parser
        :param command: the command text
        :param implementation: the implementation of the command
        :return: None
        :raises: ValueError if command is already registered
        """
        if command not in self._registered_commands:
            self._registered_commands[command] = implementation
        else:
            raise ValueError('Command {0} has already been implemented.'.format(command))

    def process(self, input):
        parts = input.split(' ')
        if parts[0] in self._registered_commands:
            implementation = self._registered_commands[parts[0]]
            implementation.execute(input)
        else:
            raise CommandNotFoundError('Command {0} was not registered with the command parser.'.format(parts[0]))