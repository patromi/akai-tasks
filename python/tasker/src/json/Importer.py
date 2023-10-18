import json
import os


class Importer:
    tasks = None

    def __init__(self):
        self.file = os.getenv('JSON_FILE') or 'taski.json'

    def read_tasks(self) -> None:
        with open('taski.json', 'r', encoding='utf-8') as file:
            data = file.read().encode('utf-8')
            self.tasks = json.loads(data)
            file.close()

    def get_tasks(self) -> list:
        return self.tasks
