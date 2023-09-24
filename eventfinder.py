from datetime import datetime, timedelta

import json
import requests
import time
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


def add_rooms(session: requests.Session) -> None:
    url = "https://lukkarit.vamk.fi/rest/basket/0/location"
    with open("Wolffintie-rooms.json", "r") as rooms_file:
        room_data = json.load(rooms_file)
    for i in range(len(room_data)):  # Restrict amount of rooms for testing
        room_data[i]["adding"] = True
        print(f"Adding room {i+1} of {len(room_data)}. Payload = {room_data[i]}")
        response = session.request("POST", url, json=room_data[i], headers=session.headers, verify=False)
        # Implement a check if returned locations is empty
        print(f"{response.status_code = }")
        time.sleep(0.1)


def read_events(session: requests.Session, today_date: str, tomorrow_date: str) -> None:
    url = "https://lukkarit.vamk.fi/rest/basket/0/events"
    payload = {
        "dateFrom": f"{today_date}",
        "dateTo": f"{tomorrow_date}",
        "eventType": "visible"
    }
    response = session.request("POST", url, json=payload, headers=session.headers, verify=False)
    try:
        data = json.loads(response.text)
        with open(f"{today_date}_events.json", "w") as json_file:
            json.dump(data, json_file, indent=5)
    except json.decoder.JSONDecodeError:
        print(f"No events found for {today_date}.")


def clean_events(today_date: str) -> None:
    with open(f"{today_date}_events.json", "r") as event_file:
        event_data = json.load(event_file)
    with open("Wolffintie-rooms.json", "r") as room_file:
        room_data = json.load(room_file)

    room_reservations = []
    for room_item in room_data:
        classroom = room_item["class"]
        reservations_by_room = {
            "class": classroom,
            "start": [],
            "end": []
        }

        for event_item in event_data:
            # Check if the "location" key has a dictionary with "class" equal to {classroom}
            if any(loc.get("class") == classroom for loc in event_item.get("location", [])):
                reservations_by_room["start"].append(event_item["start_date"])
                reservations_by_room["end"].append(event_item["end_date"])
        room_reservations.append(reservations_by_room)

    with open(f"{today_date}_clean_events.json", "w") as json_file:
        json.dump(room_reservations, json_file, indent=5)


def main():
    today_date = datetime.now().strftime("%Y-%m-%d")
    tomorrow_date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    """Testing overrides"""
    #today_date = "2023-09-24"
    #tomorrow_date = "2023-09-25"

    session = setup_session()
    if get_cookies(session):
        add_rooms(session)
        read_events(session, today_date, tomorrow_date)
        try:
            clean_events(today_date)
        except FileNotFoundError:
            print(f"No events saved for {today_date}.")


if __name__ == "__main__":
    main()
