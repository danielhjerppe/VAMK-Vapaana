import requests
import json


def room_search(session):
    """Based on 'search_term', prints a list of rooms to a .json file. """
    url = "https://lukkarit.vamk.fi/rest/locations"
    search_term = "Wolffintie"
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


def main():
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
    print(f"Cooke: {csrf_token}")

    room_search(session)


if __name__ == "__main__":
    main()
