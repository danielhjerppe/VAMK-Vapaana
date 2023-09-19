import json
from datetime import datetime, timedelta


def check_room_availability(time_now, today_date):
    with open(f"{today_date}_clean_events.json", "r") as events_file:
        event_data = json.load(events_file)

    availability_now = []

    for event in event_data:
        avail_dict = {"class": event["class"], "available": "", "number_of_events": len(event["start"])}
        available = True
        avail_dict["available"] = available
        if len(event["start"]) > 0:
            for i in range(len(event["start"])):
                starttime = datetime.strptime(event["start"][i], "%Y-%m-%d %H:%M")
                endtime = datetime.strptime(event["end"][i], "%Y-%m-%d %H:%M")
                if starttime < datetime.strptime(time_now, "%Y-%m-%d %H:%M") < endtime:
                    available = False
                    avail_dict["available"] = available

        availability_now.append(avail_dict)
    return availability_now


def print_to_terminal(rooms_available):
    for room_availability in rooms_available:
        print(f"Room: {room_availability['class']} ", end="\t")
        print(f"{room_availability['number_of_events']} event(s)", end="\t")
        if room_availability['available']:
            print("\033[92m", end="")  # Green
        else:
            print("\033[91m", end="")  # Red
        print(f"Available: {room_availability['available']}", end="")
        print("\033[0m")

def main():
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M")
    #time_now = "2023-09-18 13:00"
    today_date = datetime.now().strftime("%Y-%m-%d")
    #today_date = "2023-09-18"  # TESTING

    print(f"{time_now = }\n")

    rooms_available = check_room_availability(time_now, today_date)
    print_to_terminal(rooms_available)




if __name__ == "__main__":
    main()
