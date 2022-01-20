from interfaces.cli_team_G import CLI
from adapters.file_source import FileSource

class_interface = CLI(db_source=FileSource('../db'))
class_interface.run()
