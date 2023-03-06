import controllers
import frontend
from schedule_app import app
import logging
import sys

console = logging.StreamHandler(sys.stdout)
console.setLevel(logging.INFO)
file = logging.FileHandler("./logs/main.txt", mode="a", encoding="UTF-8")
file.setLevel(logging.DEBUG)
logging.basicConfig(
                handlers=[console, file],
                format='[%(asctime)s,%(msecs)d] %(name)s [%(levelname)s] %(message)s',
                datefmt='%H:%M:%S',
                level=logging.DEBUG)

logging.getLogger("main.adapter")
logging.getLogger("main.controller")
logging.getLogger("main.data_model")
logging.info("----------------------------------Starting app!----------------------------------")
app.run()
logging.info("----------------------------------Stopped app!----------------------------------")
logging.shutdown()