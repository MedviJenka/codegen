import time
import requests
from time import sleep
from dataclasses import dataclass
from src.environment.image_compression import ImageCompression


@dataclass
class APIRequestHandler(ImageCompression):

    api_key: str
    endpoint: str
    session: requests.Session
    _last_payload: dict = None
    _last_response: dict = None

    @property
    def _headers(self) -> dict:
        """Returns the headers for the API request."""
        return {
            "Content-Type": "application/json",
            "api-key": self.api_key,
        }

    def get_response_json(self, payload: dict) -> dict:
        """Sends API request and returns the output."""
        self._last_payload = payload  # Save the last payload
        response = self.session.post(url=self.endpoint, headers=self._headers, json=payload, verify=False)
        response.raise_for_status()
        data = response.json()
        self._last_response = data  # Save the last response
        return data

    def get_tokens(self) -> str:
        tokens = self._last_response["usage"]["total_tokens"]
        return tokens

    def make_request(self, payload: dict) -> str:
        """Makes the API request and returns the output."""
        try:
            data = self.get_response_json(payload=payload)
            output = data['choices'][0]['message']['content']
            print(f'Tokens used: {self.get_tokens()}')  # Fetch tokens without passing an argument
            return output

        except requests.RequestException as e:
            print(f"Request error: {e}")
            sleep(3)
            raise e

        except Exception as e:
            print(f"An error occurred: {e}")
            raise e

    def make_request_with_retry(self, payload: dict, retries: int = 3) -> str:
        """Retries API calls to handle failures."""
        for attempt in range(retries):
            try:
                return self.make_request(payload)

            except requests.RequestException as e:
                if attempt < retries - 1:
                    time.sleep(3)
                else:
                    raise e
