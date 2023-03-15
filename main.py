import controllers
import frontend
from schedule_app import app
import logging
import sys
from config import Configuration


loggers = [logging.getLogger("main.adapter"), logging.getLogger("main.controller"), logging.getLogger("main.data_model"), logging.getLogger("main.auth")]
for logger in loggers:
    logger.handlers.clear()

config = Configuration()
handlers = []
if (config.getBoolean("console_log_isactive")):
    console = logging.StreamHandler(sys.stdout)
    console.setLevel(config.get("console_log_level"))
    handlers.append(console)

if (config.getBoolean("file_log_isactive")):
    file = logging.FileHandler(config.get("logfile_path"), mode="a", encoding="UTF-8")
    file.setLevel(config.get("file_log_level"))
    handlers.append(file)

logging.basicConfig(
                handlers=handlers,
                format='[%(asctime)s,%(msecs)d] %(name)s [%(levelname)s] %(message)s',
                datefmt='%H:%M:%S',
                level=logging.DEBUG)


logging.getLogger("werkzeug").disabled = True
logging.info("----------------------------------Starting app!----------------------------------")
app.run()
logging.info("----------------------------------Stopped app!----------------------------------")
logging.shutdown()