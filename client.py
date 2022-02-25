import requests
from requests.auth import HTTPBasicAuth

passport_url = "https://passport.moex.com"
api_url = "http://iss.moex.com/iss"

class Client:
    def __init__(self, username, password):
       self.session = requests.Session()
       if username is None or password is None:
           raise Exception("Invalid credentials for MOEXISS")

       self.session.auth = (username, password)
       # perform authentication
       self._auth()

    @staticmethod
    def form_sec_path(candles=False, **args):
        engine = args["engine"]
        market = args["market"]
        board = args["board"]
        sec = args["security"]
        start_date = args.get("start_date", "")
        end_date = args.get("end_date", "")

        sec_path = f"/engines/{engine}/markets/{market}/boards/{board}/securities/{sec}"
        if candles:
            sec_path = sec_path + "/candles"
        sec_path += ".json"

        if end_date != "" or start_date != "":
            sec_path += F"?from={start_date}&till={end_date}"

        query_url = sec_path

        return query_url

    def _get(self, resource):
        return self.session.get(resource, params={"lang": "en"})

    def _auth(self):
        auth_url = passport_url + "/authenticate"
        self._get(auth_url)

    def engines(self):
        engine_path = "/engines.json"
        r = self._get(api_url+engine_path)

        return r.json()["engines"]

    def markets(self, engine):
        market_path = f"/engines/{engine}/markets.json"
        r = self._get(api_url+market_path)

        return r.json()["markets"]

    def boards(self, engine, market):
        board_path = f"/engines/{engine}/markets/{market}/boards.json"
        r = self._get(api_url+board_path)

        return r.json()["boards"]

    def securities(self, engine, market, board):
        secs_path = f"/engines/{engine}/markets/{market}/boards/{board}/securities.json"
        r = self._get(api_url + secs_path)

        return r.json()["securities"]


    def security_range(self, **args):
        query_url = self.form_sec_path(**args)
        r = self._get(api_url + query_url)

        return r.json()["securities"]

    def candle_data(self, **args):
        query_url = self.form_sec_path(True, **args)
        r = self._get(api_url + query_url)

        return r.json()["candles"]

if __name__ == "__main__":
    pass
