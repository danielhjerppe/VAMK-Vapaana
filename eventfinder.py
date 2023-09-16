import requests
import json
import time
from datetime import datetime, timedelta
import urllib3


def add_rooms(session):
    url = "https://lukkarit.vamk.fi/rest/basket/0/location"
    with open("Wolffintie-rooms.json", "r") as file:
        data = json.load(file)
    for i in range(len(data)):  # TESTING, restricting amount of rooms to add. Replace with len(data)
        data[i]["adding"] = True
        print(f"Adding room {i} of {len(data)}. Payload = {data[i]}")
        session.request("POST", url, json=data[i], headers=session.headers, verify=False)
        time.sleep(0.1)


def read_events(session):
    today_date = datetime.now().strftime("%Y-%m-%d")
    tomorrow_date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    today_date = "2023-09-18"  # TESTING
    tomorrow_date = "2023-09-19"  # TESTING
    url = "https://lukkarit.vamk.fi/rest/basket/0/events"
    payload = {
        "dateFrom": f"{today_date}",
        "dateTo": f"{tomorrow_date}",
        "eventType": "visible"
    }
    response = session.request("POST", url, json=payload, headers=session.headers, verify=False)
    data = json.loads(response.text)
    with open(f"{today_date}-events.json", "w") as json_file:
        json.dump(data, json_file, indent=5)



def main():
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    url = "https://lukkarit.vamk.fi/rest/user"
    custom_headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/117.0",
        "Accept": "application/json, text/plain, */*"
    }
    session = requests.Session()
    session.headers.update(custom_headers)
    response = session.get(url, verify=False)
    if response.status_code == 200:
        print("Connection ok! Continuing")
    csrf_token = "PHPSESSID=" + session.cookies.get_dict()["PHPSESSID"]
    print(f"Cooke: {csrf_token}\n")

    add_rooms(session)
    read_events(session)


if __name__ == "__main__":
    main()
