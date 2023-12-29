import json
import keyboard
import os
import time

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
gift_count = 0
total_gifts = 0
gift_map = [[False for j in range(field["width"])] for i in range(field["height"])]
for i in range(field["height"]):
    for j in range(field["width"]):
        if field["field"][i][j] == field["symbols"]["player"]["in-file"]:
            x, y = i, j
        if field["field"][i][j] == field["symbols"]["present"]["in-file"]:
            total_gifts += 1
            gift_map[i][j] = True

previous_room = 0
previous_cell = "."
last_interaction_type = "none"
last_interaction_num = -1
last_interaction_other = -1
about_gifts = False
about_count = False

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
    print("\x1b[1;31;40mX\x1b[0m-\x1b[1;32;40mMAS\x1b[0m \x1b[1;36;40mQUEST\x1b[0m")
    print("- "*20)
    print("\x1B[1;33;40mМиссии:")
    if about_gifts:
        if about_count:
            print(f"- Собери все подарки! ({gift_count} / {total_gifts})...")
        else:
            print(f"- Собери все подарки! ({gift_count})...")
    else:
        print("- Нету...")
    print("\x1b[0m")
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
                if gift_map[i][j] is True:
                    print(f'\x1b[1;{field["symbols"]["present"]["color"]};40m', end="")
                    print(field["symbols"]["present"]["in-game"], end="")
                else:
                    if i == x and j == y:
                        print(f'\x1b[1;{field["symbols"]["player"]["color"]};40m', end="")
                        print(field["symbols"]["player"]["in-game"], end="")
                    else:
                        print(f'\x1b[1;{field["symbols"]["space"]["color"]};40m', end="")
                        print(field["symbols"]["space"]["in-game"], end="")
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
    print("\x1B[1;33;40m")
    if last_interaction_type == "present":
        print("Подарок собран!")
    elif last_interaction_type == "character":
        for i in range(last_interaction_other):
            print(field["dialogs"][last_interaction_num][i][0], end=" | ")
            print(field["symbols"]["characters"][field["dialogs"][last_interaction_num][i][0]]["name"].ljust(15), end=" | ")
            print(field["dialogs"][last_interaction_num][i][1])
        if last_interaction_other < len(field["dialogs"][last_interaction_num]):
            print("Нажмите E, чтобы продолжить диалог...")
    elif last_interaction_type == "sign":
        print(f'"{field["symbols"]["signs"]["in-file"][last_interaction_num]}"')
    else:
        for d in [[1, 0], [0, 1], [-1, 0], [0, -1]]:
            if field["field"][x + d[0]][y + d[1]] == field["symbols"]["present"]["in-file"] and gift_map[x + d[0]][y + d[1]] is True:
                print("Нажмите E, чтобы собрать подарок...")
                break
            if field["field"][x + d[0]][y + d[1]] in field["symbols"]["characters"].keys() and field["field"][x + d[0]][y + d[1]] != field["symbols"]["player"]["in-file"]:
                print(f'Нажмите E, чтобы поговорить с человеком...')
                break
            if field["field"][x + d[0]][y + d[1]] in field["symbols"]["signs"]["in-file"].keys():
                print(f'Нажмите E, чтобы прочитать табличку...')
                break
    print("\x1b[0m")

def change_position(dx, dy):
    global x, y, last_interaction_type
    if gift_count == total_gifts:
        return
    x += dx
    y += dy
    last_interaction_type = "none"
    if field["field"][x][y] == field["symbols"]["wall"]["in-file"]:
        x -= dx
        y -= dy
    if field["field"][x][y] == field["symbols"]["present"]["in-file"] and gift_map[x][y] is True:
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
    last_interaction_type = "none"
    print_field()

def interact():
    global last_interaction_other, last_interaction_type, last_interaction_num, gift_count, about_count, about_gifts
    if gift_count == total_gifts:
        return
    if last_interaction_type == "character" and last_interaction_other < len(field["dialogs"][last_interaction_num]):
        last_interaction_other += 1
        if last_interaction_num == 0 and last_interaction_other == 5:
            about_gifts = True
        elif last_interaction_num == 1 and last_interaction_other == 4:
            about_gifts = True
            about_count = True
        print_field()
    elif last_interaction_type == "none":
        for d in [[1, 0], [0, 1], [-1, 0], [0, -1]]:
            if field["field"][x + d[0]][y + d[1]] == field["symbols"]["present"]["in-file"] and gift_map[x + d[0]][y + d[1]] is True:
                last_interaction_type = "present"
                gift_count += 1
                gift_map[x + d[0]][y + d[1]] = False
                if gift_count == total_gifts:
                    ending()
                else:
                    print_field()
                break
            if field["field"][x + d[0]][y + d[1]] in field["symbols"]["characters"].keys() and field["field"][x + d[0]][y + d[1]] != field["symbols"]["player"]["in-file"]:
                last_interaction_type = "character"
                last_interaction_num = field["symbols"]["characters"][field["field"][x + d[0]][y + d[1]]]["dialog"]
                last_interaction_other = 1
                print_field()
                break
            if field["field"][x + d[0]][y + d[1]] in field["symbols"]["signs"]["in-file"].keys():
                last_interaction_type = "sign"
                last_interaction_num = field["field"][x + d[0]][y + d[1]]
                print_field()
                break

def print_letter(letter):
    if letter == 'H':
        return ['█   █', '█   █', '█████', '█   █', '█   █']
    elif letter == 'A':
        return [' ███ ', '█   █', '█████', '█   █', '█   █']
    elif letter == 'P':
        return ['████ ', '█   █', '████ ', '█    ', '█    ']
    elif letter == 'Y':
        return ['█   █', ' █ █ ', '  █  ', '  █  ', '  █  ']
    elif letter == 'N':
        return ['█   █', '██  █', '█ █ █', '█  ██', '█   █']
    elif letter == 'E':
        return ['█████', '█    ', '█████', '█    ', '█████']
    elif letter == 'W':
        return ['█   █', '█   █', '█ █ █', '██ ██', '█   █']
    elif letter == 'R':
        return ['████ ', '█   █', '████ ', '█ █  ', '█   █']
    elif letter == '0':
        return [' ███ ', '█  ██', '█ █ █', '██  █', ' ███ ']
    elif letter == '2':
        return [' ███ ', '█   █', '  ██ ', ' █   ', '█████']
    elif letter == '3':
        return ['████ ', '    █', '  ██ ', '    █', '████ ']
    elif letter == '4':
        return ['█  █ ', '█  █ ', '█████', '   █ ', '   █ ']
    else:
        return ['     ', '     ', '     ', '     ', '     ']

def print_word(word, color):
    print(f'\x1b[1;{color};40m', end='')
    for i in range(5):
        for letter in word:
            print(print_letter(letter)[i], end='  ')
        print()

def ending():
    os.system('cls')
    print_word('HAPPY', 31)
    print()
    time.sleep(1)
    print_word('NEW', 32)
    print()
    time.sleep(1)
    print_word('YEAR', 33)
    print()
    time.sleep(1)
    for i in range(5):
        print(f'\x1b[1;36;40m', end='')
        for letter in "202":
            print(print_letter(letter)[i], end='  ')
        print(f'\x1b[1;31;40m', end='')
        print(print_letter("3")[i])
    time.sleep(1)
    for j in range(5):
        os.system('cls')
        print_word('HAPPY', 31)
        print()
        print_word('NEW', 32)
        print()
        print_word('YEAR', 33)
        print()
        for i in range(5):
            print(f'\x1b[1;36;40m', end='')
            for letter in "202":
                print(print_letter(letter)[i], end='  ')
            if i <= j:
                print(print_letter("4")[4 - j + i])
            else:
                print(f'\x1b[1;31;40m', end='')
                print(print_letter("3")[i - j])
        time.sleep(0.2)
        print()
    time.sleep(2)
    print("\x1B[1;33;40mСпасибо за Прохождение игры!\x1B[0m")
    print()
    time.sleep(1)
    print("\x1b[1;31;40mX\x1b[0m-\x1b[1;32;40mmas\x1b[0m \x1b[1;36;40mQuest\x1b[0m от:")
    time.sleep(1)
    print("\x1b[1;31;40mЛиппа Евгений\x1b[0m (Кодинг, Поле, Диалоги)")
    time.sleep(0.25)
    print("\x1b[1;32;40mДорошкевич Глеб\x1b[0m (Кодинг)")
    time.sleep(0.25)
    print("\x1b[1;33;40mНовицкий Максим\x1b[0m (Поле, Диалоги)")
    time.sleep(0.25)
    print("\x1b[1;36;40mТуровец Степан\x1b[0m (Поле)")
    print()
    time.sleep(3)
    print("\x1b[1;90;40mНажмите Q, чтобы выйти из игры...\x1b[0m")

pressedQ = False
def leave():
    global pressedQ
    os.system('cls')
    pressedQ = True
    print("\x1b[1;90;40mВыход из игры...\x1b[0m")

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
keyboard.add_hotkey('q', leave)

while not pressedQ:
    time.sleep(1)
