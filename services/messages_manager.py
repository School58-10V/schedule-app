from config import Configuration


class MessagesManager:
    def __init__(self) -> None:
        self.__config = Configuration("./messages.json")
    
    def get_message(self, path: str, placeholders: dict = None):
        message = self.__config.get(path)
        if placeholders:
            for key in placeholders.keys():
                message = message.replace(f"%{key}%", placeholders[key])
        return message