import json
import keyboard
import os

from colorama import init as colorama_init
from colorama import Fore

colorama_init()

def get_json(file: str):
    data = {}
    with open(file, 'r', encoding="utf-8") as f:
        data = json.load(f)
    return data

def replace_json(file: str, data) -> None:
    with open(file, 'w', encoding="utf-8") as f:
        json.dump(data, f)

field = get_json('field.json')
x, y = -1, -1
for i in range(field["height"]):
    for j in range(field["width"]):
        if field["field"][i][j] == field["symbols"]["player"]["in-file"]:
            x, y = i, j
            break
    if x != -1:
        break
previous_room = 0
previous_cell = "."

def get_rooms():
    for c, i in field["symbols"]["doors"].items():
        if field["field"][x][y] == c:
            return i
    for i, j in enumerate(field["rooms"]):
        if j["x"] <= x < j["x"] + j["a"] and j["y"] <= y < j["y"] + j["b"]:
            return [i]
    return [0]

def print_field():
    global previous_cell, previous_room
    rooms = get_rooms()
    room_num = rooms[0]
    if len(rooms) > 1:
        if previous_cell == field["field"][x][y]:
            room_num = previous_room
        elif previous_room == rooms[0]:
            room_num = rooms[1]
    room = field["rooms"][room_num]
    os.system('cls')
    for i in range(room["x"], room["x"] + room["a"]):
        for j in range(room["y"], room["y"] + room["b"]):
            if field["field"][i][j] == field["symbols"]["wall"]["in-file"]:
                print(f'\x1b[1;{field["symbols"]["wall"]["color"]};40m', end="")
                print(field["symbols"]["wall"]["in-game"], end="")
            elif field["field"][i][j] == field["symbols"]["space"]["in-file"] or field["field"][i][j] == field["symbols"]["player"]["in-file"]:
                if i == x and j == y:
                    print(f'\x1b[1;{field["symbols"]["player"]["color"]};40m', end="")
                    print(field["symbols"]["player"]["in-game"], end="")
                else:
                    print(f'\x1b[1;{field["symbols"]["space"]["color"]};40m', end="")
                    print(field["symbols"]["space"]["in-game"], end="")
            elif field["field"][i][j] == field["symbols"]["present"]["in-file"]:
                print(f'\x1b[1;{field["symbols"]["present"]["color"]};40m', end="")
                print(field["symbols"]["present"]["in-game"], end="")
            elif field["field"][i][j] in field["symbols"]["doors"].keys():
                if i == x and j == y:
                    print(f'\x1b[1;{field["symbols"]["player"]["color"]};40m', end="")
                    print(field["symbols"]["player"]["in-game"], end="")
                else:
                    print(f'\x1b[1;{field["symbols"]["space"]["color"]};40m', end="")
                    print(field["symbols"]["space"]["in-game"], end="")
            elif field["field"][i][j] in field["symbols"]["signs"]["in-file"].keys():
                print(f'\x1b[1;{field["symbols"]["signs"]["color"]};40m', end="")
                print(field["symbols"]["signs"]["in-game"], end="")
            elif field["field"][i][j] in field["symbols"]["characters"].keys():
                print(f'\x1b[1;{field["symbols"]["characters"]["color"]};40m', end="")
                print(field["field"][i][j], end="")
            else:
                if i == x and j == y:
                    print(f'\x1b[1;{field["symbols"]["player"]["color"]};40m', end="")
                    print(field["symbols"]["player"]["in-game"], end=" ")
                else:
                    print(f'\x1b[1;{field["symbols"]["space"]["color"]};40m', end="")
                    print(field["symbols"]["space"]["in-game"], end=" ")
            print(f'\x1b[0m', end=" ")
        print()
    previous_cell = field["field"][x][y]
    previous_room = room_num

def change_position(dx, dy):
    global x, y
    x += dx
    y += dy
    if field["field"][x][y] == field["symbols"]["wall"]["in-file"]:
        x -= dx
        y -= dy
    if field["field"][x][y] == field["symbols"]["present"]["in-file"]:
        x -= dx
        y -= dy
    for c in field["symbols"]["characters"]:
        if c == field["symbols"]["player"]["in-file"]:
            continue
        if field["field"][x][y] == c:
            x -= dx
            y -= dy
    for c in field["symbols"]["signs"]["in-file"]:
        if field["field"][x][y] == c:
            x -= dx
            y -= dy
    print_field()

def interact():
    print("interaction")

print_field()

keyboard.add_hotkey('w', change_position, args=(-1, 0))
keyboard.add_hotkey('up', change_position, args=(-1, 0))
keyboard.add_hotkey('d', change_position, args=(0, 1))
keyboard.add_hotkey('right', change_position, args=(0, 1))
keyboard.add_hotkey('a', change_position, args=(0, -1))
keyboard.add_hotkey('left', change_position, args=(0, -1))
keyboard.add_hotkey('s', change_position, args=(1, 0))
keyboard.add_hotkey('Down', change_position, args=(1, 0))
keyboard.add_hotkey('e', interact)

keyboard.wait()