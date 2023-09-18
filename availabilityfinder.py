import json
from datetime import datetime, timedelta


def check_room_availability(time_now, today_date):
    with open(f"{today_date}_clean_events.json", "r") as events_file:
        event_data = json.load(events_file)

    availability_now = []

    for event in event_data:
        avail_dict = {"class": "", "available": ""}
        print(f"Room: {event['class']} ", end="\t")
        avail_dict["class"] = event["class"]
        print(f'{len(event["start"])} event(s)', end="\t")
        available = True
        avail_dict["available"] = available
        if len(event["start"]) > 0:
            for i in range(len(event["start"])):
                starttime = datetime.strptime(event["start"][i], "%Y-%m-%d %H:%M")
                endtime = datetime.strptime(event["end"][i], "%Y-%m-%d %H:%M")
                if starttime < datetime.strptime(time_now, "%Y-%m-%d %H:%M") < endtime:
                    available = False
                    avail_dict["available"] = available
        if available:
            print("\033[92m", end="")  # Green
        else:
            print("\033[91m", end="")  # Red
        print(f"{available = }", end="")
        print("\033[0m")
        availability_now.append(avail_dict)
    return availability_now



def main():
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M")
    #time_now = "2023-09-18 13:00"
    today_date = datetime.now().strftime("%Y-%m-%d")
    #today_date = "2023-09-18"  # TESTING

    print(f"{time_now = }\n")

    rooms_available = check_room_availability(time_now, today_date)
    print(rooms_available)


if __name__ == "__main__":
    main()
