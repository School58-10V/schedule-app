from interfaces.cli import CLI
from adapters.file_source import FileSource

data = FileSource('../db')
class_interface = CLI(data)
CLI.run()
