import os
import time

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
time.sleep(2)
