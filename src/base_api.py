import time
import requests


class ESPNBaseAPI:
    def __init__(self):
        self._base_url = 'https://site.api.espn.com/apis/site/v2/sports'
        self._core_url = 'https://sports.core.api.espn.com/v2/sports'

    def api_request(self, url, retry_count=0):
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
            }
            resp = requests.get(url=url,headers=headers)
            if resp.status_code == 404:
                return None
            res = resp.json()
            if 'error' in res:
                if res['error']['code'] == 404: # No data
                    return None
            if 'code' in res:
                if res['code'] == 2502:
                    raise Exception('Flooded') # Too many requests
                if res['code'] == 400: # Data cant be found (wrong endpoint/wrong request)
                    return None
            return res
        except Exception as e:
            if retry_count >= 3:
                raise e
            time.sleep(5)
            print(f'URL error for {url}')
            self.api_request(url, retry_count = retry_count + 1)

