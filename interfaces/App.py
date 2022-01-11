from interfaces.cli import CLI
from adapters.file_source import FileSource
import os

data = FileSource('../db')
class_interface = CLI(data)
