import datetime
import json
import os

import requests
from dotenv import load_dotenv

load_dotenv()


class RatioObtainer:
    base = None
    target = None

    def __init__(self, base, target):
        self.base = base
        self.target = target
        self.access_key = os.getenv('ACCESS_KEY')
        self.host = os.getenv('HOST') or 'http://api.exchangerate.host/convert'
        self.ratio_file_path = os.getenv('RATIO_FILE') or 'ratios.json'

    def _get_parsed_data_from_file(self) -> list:
        with open(self.ratio_file_path, 'r') as file:
            if os.stat(self.ratio_file_path).st_size == 0: # if file is empty
                return []
            parsed_data = json.load(file)
            file.close()
            return parsed_data

    def _save_to_file(self, data: list):
        with open(self.ratio_file_path, 'w') as file:
            json.dump(data, file, indent=4)
            file.close()

    def was_ratio_saved_today(self) -> bool:
        data = self._get_parsed_data_from_file()
        if data:
            today_radios = list(filter(
                lambda x: x.get('date_fetched') == str(datetime.date.today()) and x.get(
                    'base_currency') == self.base and x.get(
                    'target_currency') == self.target, data))
            if today_radios:
                return True
        return False

    def fetch_ratio(self):
        response = requests.get(self.host,
                                params={'access_key': self.access_key, 'from': self.base, 'to': self.target,
                                        'amount': 1})
        parsed_data = json.loads(response.text)
        self._save_ratio(parsed_data['result'])

    def _save_ratio(self, ratio: float):
        data = self._get_parsed_data_from_file()

        if data:
            for currency in data:
                if currency['base_currency'] == self.base and currency['target_currency'] == self.target:
                    currency['ratio'] = ratio
                    currency['date_fetched'] = str(datetime.date.today())
                    break
            else:
                data.append({'base_currency': self.base, 'target_currency': self.target, 'ratio': ratio,
                                 'date_fetched': str(datetime.date.today())}) # if currency not found
        else:
            data.append({'base_currency': self.base, 'target_currency': self.target, 'ratio': ratio,
                         'date_fetched': str(datetime.date.today())}) # if file is empty
        self._save_to_file(data)

    def get_matched_ratio_value(self) -> float or None:
        matched_currency = list(
            filter(lambda x: x.get('base_currency') == self.base and x.get('target_currency') == self.target,
                   self._get_parsed_data_from_file()))
        if not matched_currency:
            return None

        return matched_currency[0].get('ratio')
