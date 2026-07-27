import json
import urllib.error
import urllib.request


class GreenhouseCollector:
    BASE_URL = "https://boards-api.greenhouse.io/v1/boards"

    def collect(self, identifier: str) -> list[dict]:
        url = f"{self.BASE_URL}/{identifier}/jobs?content=true"

        try:
            with urllib.request.urlopen(url, timeout=60) as response:
                data = json.load(response)

        except urllib.error.HTTPError as error:
            if error.code == 404:
                return []
            raise

        except (TimeoutError, urllib.error.URLError) as error:
            print(f"Failed to collect {identifier}: {error}")
            return []

        return data.get("jobs", [])