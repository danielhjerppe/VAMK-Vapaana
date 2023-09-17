import json
from datetime import datetime, timedelta


def check_room_availability(time_now, today_date):
    with open(f"{today_date}_clean_events.json", "r") as events_file:
        event_data = json.load(events_file)

    for event in event_data:
        print(f"Room: {event['class']} ", end="\t")
        print(f'{len(event["start"])} event(s)', end="\t")
        available = True
        if len(event["start"]) > 0:
            for i in range(len(event["start"])):
                starttime = datetime.strptime(event["start"][i], "%Y-%m-%d %H:%M")
                endtime = datetime.strptime(event["end"][i], "%Y-%m-%d %H:%M")
                if starttime < datetime.strptime(time_now, "%Y-%m-%d %H:%M") < endtime:
                    available = False
        print(f"{available = }")


def main():
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M")
    time_now = "2023-09-18 13:00"
    today_date = datetime.now().strftime("%Y-%m-%d")
    today_date = "2023-09-18"  # TESTING

    print(f"{time_now = }\n")

    check_room_availability(time_now, today_date)


if __name__ == "__main__":
    main()
