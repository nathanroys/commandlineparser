import sys
from cmdline import CommandParser

parser = CommandParser('./test.yml')
parser.load_configuration()
parser.process_input(sys.argv)