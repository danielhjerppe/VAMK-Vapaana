import requests
import json
import urllib3


def setup_session() -> requests.Session:
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    custom_headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/117.0",
        "Accept": "application/json, text/plain, */*"
    }
    session = requests.Session()
    session.headers.update(custom_headers)
    return session


def get_cookies(session: requests.Session) -> bool:
    url = "https://lukkarit.vamk.fi/rest/user"
    response = session.get(url, verify=False)
    if response.status_code == 200:
        print(f"Connection ok! {response.status_code = }")
        csrf_token = "PHPSESSID=" + session.cookies.get_dict()["PHPSESSID"]
        print(f"Cookie: {csrf_token}")
        return True
    else:
        print(f"Error. Check connection. {response.status_code = }")
        return False


def room_search(session: requests.Session, search_term: str) -> None:
    """Based on 'search_term', prints a list of rooms to a .json file. """
    url = "https://lukkarit.vamk.fi/rest/locations"
    payload = {
        "target": "locations",
        "type": "name",
        "text": f"{search_term}",
        "dateFrom": "",
        "dateTo": "",
        "filters": "[]",
        "show": "true"
    }
    response = session.request("POST", url, json=payload, headers=session.headers, verify=False)
    data = json.loads(response.text)
    sorted_data = sorted(data, key=lambda x: x['class'])  # Sort the data based on the "class" key
    with open(f"{search_term}-rooms.json", "w") as json_file:
        json.dump(sorted_data, json_file, indent=5)
    print(f"Found {len(sorted_data)} rooms. Saved to {search_term}-rooms.json")


def main():
    session = setup_session()
    if get_cookies(session):
        room_search(session, search_term="Wolffintie")


if __name__ == "__main__":
    main()
