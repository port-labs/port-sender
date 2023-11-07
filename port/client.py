import logging

import requests


logger = logging.getLogger(__name__)


class PortClient:
    def __init__(self, api_url: str, client_id:str, client_secret:str):
        self.api_url = api_url
        self.access_token = self.get_token(client_id, client_secret)
        self.headers = {
            "Authorization": f"Bearer {self.access_token}",
            "User-Agent": "port-message-service",
        }

    def get_token(self, client_id, client_secret):
        credentials = {"clientId": client_id, "clientSecret": client_secret}
        token_response = requests.post(
            f"{self.api_url}/v1/auth/access_token", json=credentials
        )
        token_response.raise_for_status()
        return token_response.json()["accessToken"]

    def search_entities(self, query):
        search_req = requests.post(
            f"{self.api_url}/v1/entities/search",
            json=query,
            headers=self.headers,
            params={},
        )
        search_req.raise_for_status()
        return search_req.json()["entities"]

    def get_scorecard(self, blueprint_id: str, scorecard_id: str):
        scorecard_req = requests.get(
            f"{self.api_url}/v1/blueprints/{blueprint_id}/scorecards/{scorecard_id}",
            headers=self.headers,
        )
        scorecard_req.raise_for_status()
        return scorecard_req.json()

