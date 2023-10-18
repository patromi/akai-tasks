import json
import os


class Exporter:

    def __init__(self):
        self.file = os.getenv('JSON_FILE') or 'taski.json'

    def save_tasks(self, tasks) -> None:
        with open(self.file, 'w',encoding='utf-8') as file:
            json.dump(tasks, file, indent=4, ensure_ascii=False)
            file.close()



