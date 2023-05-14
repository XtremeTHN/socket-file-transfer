import json, os
from modules.exception_handler import ExceptionHandler
from typing import Dict, NoReturn

class Json():
    RESULT = int

    class JsonConfigs():
        def __init__(self, configs: dict):
            for x in configs:
                setattr(self, x, configs[x])

    def __init__(self, file, default_values=None, indent=None) -> NoReturn:
        self.file = file
        try:
            if not os.path.isfile(file):
                with open(file, 'w') as file:
                    json.dump(default_values if default_values else {}, file, indent=indent)
            elif open(self.file).read() == "":
                with open(file, 'w') as file:
                    json.dump(default_values if default_values else {}, file, indent=indent)
        except (FileNotFoundError):
            os.makedirs(os.path.split(file)[0], exist_ok=True)
            self.__init__(file, default_values=default_values)

        self.content = None
        pass
    
    def get(self) -> Dict:
        with open(self.file) as file:
            self.content = json.load(file)
        return self.content
    
    def get_to_object(self, obj=None) -> JsonConfigs:
        with open(self.file) as file:
            self.content = json.load(file)
        return self.JsonConfigs(self.content)
    
    def set(self, data, indent=None) -> RESULT:
        try:
            with open(self.file, 'w') as file:
                json.dump(data, file, indent=indent)
            return 0
        except:
            return 1