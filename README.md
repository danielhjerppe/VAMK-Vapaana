# VAMK: Vapaana
Shows a real-time map of free classrooms. Useful e.g. working on group assignments at campus.

Consists of three parts:
1. **roomfinder** 
* Is used to find all available rooms at campus based on a searchword. 
* Ideally only needs to be run once.
2. **eventfinder**
* Reads list of available rooms, posts them to the web API and receives all booked events for today.
* Strips unnecessary information from response and saves a .json file with bookings per room
* Needs to be run at least daily
3. **availabilityfinder**
* Checks which rooms are currently free
* The "real-time" component of the program


To do:
* Web GUI

