import flet as ft
import json
import availabilityfinder
from datetime import datetime, timedelta


def main(page: ft.Page):
    page.title = "VAMK: Vapaana"
    page.appbar = ft.AppBar(
        title=ft.Text("VAMK Vapaana", color=ft.colors.WHITE),  # title of the AppBar, with a white color
        center_title=False,  # we center the title
        bgcolor=ft.colors.BLUE,  # a color for the AppBar's background
    )
    field_time = ft.TextField(label="Time", value=datetime.now().strftime("%Y-%m-%d %H:%M"), width=200)
    today_date = datetime.now().strftime("%Y-%m-%d")

    floor_3_a_1 = [28, 29, 30, 31, 32, 33, 34]

    room_cards = []

    for room in availabilityfinder.check_room_availability(field_time.value, today_date):
        room_cards.append(ft.Container(
            content=ft.Text(room["class"]),
            alignment=ft.alignment.center,
            width=150,
            height=150,
            bgcolor="grey",
            border_radius=5,
            animate_opacity=300,
        ))


    def click_manual_time(e):
        field_time.value = field_time.value
        field_time.update()

    def click_automatic_time(e):
        field_time.value = datetime.now().strftime("%Y-%m-%d %H:%M")
        field_time.update()
        click_update_rooms(e)

    def click_update_rooms(e):
        i = 0
        availability_list = availabilityfinder.check_room_availability(field_time.value, today_date)
        for card in room_cards:
            availability_dict = availability_list[i]
            card.bgcolor = "green" if availability_dict["available"] else "red"
            card.update()
            i += 1

    def click_subtract_time(e):
        field_time.value = datetime.strftime(datetime.strptime(field_time.value, "%Y-%m-%d %H:%M")  - timedelta(minutes=30), "%Y-%m-%d %H:%M")
        field_time.update()
        click_update_rooms(e)

    def click_add_time(e):
        field_time.value = datetime.strftime(datetime.strptime(field_time.value, "%Y-%m-%d %H:%M") + timedelta(minutes=30), "%Y-%m-%d %H:%M")
        field_time.update()
        click_update_rooms(e)

    button_update_time_automatically = ft.ElevatedButton("Time now", on_click=click_automatic_time)
    button_update_rooms = ft.ElevatedButton("Update rooms", on_click=click_update_rooms)
    button_subtract_time = ft.FilledTonalButton("- 30 min", on_click=click_subtract_time)
    button_add_time = ft.FilledTonalButton("+ 30 min", on_click=click_add_time)

    control_row = ft.Row(wrap=True, spacing=5,
                         controls=[button_subtract_time,field_time, button_add_time,button_update_time_automatically, button_update_rooms],
                         alignment=ft.MainAxisAlignment.START,)
    rooms_row = ft.Row(wrap=True, spacing=5, controls=room_cards,
                         width=page.window_width,
                         alignment=ft.MainAxisAlignment.CENTER)
    rooms_row = ft.GridView(room_cards,expand=True, max_extent=100, child_aspect_ratio=1)

    page.add(control_row)
    page.add(rooms_row)
    page.update()



ft.app(target=main)
#view=ft.AppView.WEB_BROWSER