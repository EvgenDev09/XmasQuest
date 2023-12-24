import json
import keyboard

def get_json(file: str):
    data = {}
    with open(file, 'r', encoding="utf-8") as f:
        data = json.load(f)
    return data

def replace_json(file: str, data) -> None:
    with open(file, 'w', encoding="utf-8") as f:
        json.dump(data, f)

field = get_json('field.json')
x, y = 7, 4

def print_field():
    print(x, y)

def change_position(dx, dy):
    global x, y
    x += dx
    y += dy
    if field["field"][x][y] == field["symbols"]["wall"]["in-file"]:
        print("wall")
        x -= dx
        y -= dy
    if field["field"][x][y] == field["symbols"]["present"]["in-file"]:
        print("present")
        x -= dx
        y -= dy
    for c in field["symbols"]["characters"]["in-file"]:
        if c == field["symbols"]["player"]["in-file"]:
            continue
        if field["field"][x][y] == c:
            print("character")
            x -= dx
            y -= dy
    for c in field["symbols"]["signs"]["in-file"]:
        if field["field"][x][y] == c:
            print("sign")
            x -= dx
            y -= dy
    print_field()

def interact():
    print("interaction")

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