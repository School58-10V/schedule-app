from interfaces.cli import CLI
from adapters.file_source import FileSource
import os

cli = CLI(db_source=FileSource)
