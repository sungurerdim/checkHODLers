import requests
from .common import sleep

def getRequestResult(_target_URL, _parameters):
    retry_delay = 5

    with requests.Session() as session:
        adapter = requests.adapters.HTTPAdapter(max_retries=10)
        session.mount('http://', adapter)
        session.mount('https://', adapter)

        while True:
            try:
                response = session.get(_target_URL, params=_parameters,  timeout=30)
                response.raise_for_status()
                return response.json()['result']
            except requests.exceptions.RequestException as ex:
                print(f"An exception of type {type(ex).__name__} occurred: {ex}")
                print(f"Request response: {response}")
                print(f"Will retry after {retry_delay} seconds...")
                sleep(retry_delay)