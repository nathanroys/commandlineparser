import yaml


class Command:

    def __init__(self, command, implementation, arguments):
        self.command = command
        self.implementation = implementation
        self.arguments = arguments


class Argument:

    def __init__(self, type, input_type, name, friendly_name, description):
        self.type = type
        self.input_type = input_type
        self.name = name
        self.friendly_name = friendly_name
        self.description = description


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
        else:
            raise ValueError('Could not find tag {0}, please check your configuration file.'.format(self.COMMANDS_TAG))


