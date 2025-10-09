import requests

class HttpUtil:
    """Utility class for making HTTP requests with error handling."""

    @staticmethod
    def get_json(url, timeout=10):
        try:
            resp = requests.get(url, timeout=timeout)
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            print(f"Error doing GET {url}: {e}")
            return None