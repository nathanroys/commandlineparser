import yaml


class Command:

    def __init__(self, command, implementation, arguments):
        self.command = command
        self.implementation = implementation
        self.arguments = arguments

    def execute(self, cmd_input):
        parts = self.implementation.split('/')
        module = __import__(parts[0])
        func = getattr(module, parts[1])
        func(cmd_input)


class Argument:

    ARGUMENT_PREFIX = '-'

    def __init__(self, type, input_type, name, friendly_name, description):
        self.type = type
        self.input_type = input_type
        self.name = name
        self.friendly_name = friendly_name
        self.description = description

    def get_value(self, parts):
        if (self.ARGUMENT_PREFIX + self.name) in parts:
            if self.input_type != "None":
                value = parts[parts.index(self.ARGUMENT_PREFIX + self.name) + 1]
                return {self.name: value}
            else:
                return {self.name: None}
        else:
            # TODO: Use custom exception, allow optional args
            raise ValueError('Could not find argument {0}.'.format(self.friendly_name))


class CommandParser:
    """
    Loads and parses command line input from the specified YAML file.
    """

    # The various constant tags
    COMMANDS_TAG = 'commands'
    COMMAND_TAG = 'command'
    IMPLEMENTATION_TAG = 'implementation'
    ARGUMENTS_TAG = 'arguments'
    TYPE_TAG = 'type'
    INPUT_TYPE_TAG = 'input_type'
    NAME_TAG = 'name'
    FRIENDLY_NAME_TAG = 'friendly_name'
    DESCRIPTION_TAG = 'description'

    def __init__(self, configuration_file):
        self._configuration_file = configuration_file
        self._configuration = {}
        self._registered_commands = {}

    def load_configuration(self):
        """
        Loads the configuration from the file specified at when the parser
        was created.
        :return: None
        :raises: ValueError if the file cannot be opened
        """
        try:
            # Read in the configuration if we can
            handle = open(self._configuration_file, 'r')
            self._configuration = yaml.load(handle)
            handle.close()

            # Process the input
            self.__process_configuration()
        except:
            raise ValueError('Could not open {0} for reading.'.format(self._configuration_file))

    def process_input(self, cmd_input):
        """
        Takes the input as a string and processes then executes the command
        :param cmd_input: the string input
        :return: None
        """
        cmd_input = cmd_input[1:]
        if cmd_input[0] in self._registered_commands:
            command = self._registered_commands[cmd_input[0]]
            args = {}
            for argument in command.arguments:
                args.update(argument.get_value(cmd_input))
            command.execute(args)

    def __process_configuration(self):
        if self.COMMANDS_TAG in self._configuration:
            for command in self._configuration[self.COMMANDS_TAG]:
                command_name = command[self.COMMAND_TAG]
                implementation = command[self.IMPLEMENTATION_TAG]
                arguments = []

                if self.ARGUMENTS_TAG in command:
                    for argument in command[self.ARGUMENTS_TAG]:
                        cmd_type = argument[self.TYPE_TAG]
                        input_type = argument[self.INPUT_TYPE_TAG]
                        name = argument[self.NAME_TAG]
                        friendly_name = argument[self.FRIENDLY_NAME_TAG]
                        description = argument[self.DESCRIPTION_TAG]

                        argument = Argument(cmd_type, input_type, name, friendly_name, description)
                        arguments.append(argument)

                command = Command(command_name, implementation, arguments)
                self._registered_commands[command_name] = command
        else:
            raise ValueError('Could not find tag {0}, please check your configuration file.'.format(self.COMMANDS_TAG))


