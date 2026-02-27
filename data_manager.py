import requests

class DataManager:
    def __init__(self, endpoint, username, password):
        self.response = requests.get(url=endpoint, auth=(username, password))
        self.response.raise_for_status()
        data = self.response.json()
        self.prices = data["prices"]

