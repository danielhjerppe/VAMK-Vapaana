from datetime import datetime, timedelta

import json
import requests
import time
import urllib3


def add_rooms(session: requests.Session) -> None:
    url = "https://lukkarit.vamk.fi/rest/basket/0/location"
    with open("Wolffintie-rooms.json", "r") as rooms_file:
        room_data = json.load(rooms_file)
    for i in range(len(room_data)):  # Restrict amount of rooms for testing
        room_data[i]["adding"] = True
        print(f"Adding room {i+1} of {len(room_data)}. Payload = {room_data[i]}")
        session.request("POST", url, json=room_data[i], headers=session.headers, verify=False)
        time.sleep(0.1)


def read_events(session: requests.Session, today_date: str, tomorrow_date: str) -> None:
    url = "https://lukkarit.vamk.fi/rest/basket/0/events"
    payload = {
        "dateFrom": f"{today_date}",
        "dateTo": f"{tomorrow_date}",
        "eventType": "visible"
    }
    response = session.request("POST", url, json=payload, headers=session.headers, verify=False)
    data = json.loads(response.text)
    with open(f"{today_date}_events.json", "w") as json_file:
        json.dump(data, json_file, indent=5)


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
    #today_date = "2023-09-18"  # TESTING
    #tomorrow_date = "2023-09-19"  # TESTING

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
    read_events(session, today_date, tomorrow_date)
    clean_events(today_date)


if __name__ == "__main__":
    main()
