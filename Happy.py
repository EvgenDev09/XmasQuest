def print_letter(letter):
    if letter == 'H':
        return ['*   *', '*   *', '*****', '*   *', '*   *']
    elif letter == 'A':
        return [' *** ', '*   *', '*****', '*   *', '*   *']
    elif letter == 'P':
        return ['**** ', '*   *', '**** ', '*    ', '*    ']
    elif letter == 'Y':
        return ['*   *', ' * * ', '  *  ', '  *  ', '  *  ']
    elif letter == 'N':
        return ['*   *', '**  *', '* * *', '*  **', '*   *']
    elif letter == 'E':
        return ['*****', '*    ', '*****', '*    ', '*****']
    elif letter == 'W':
        return ['*   *', '*   *', '* * *', '** **', '*   *']
    elif letter == 'R':
        return ['**** ', '*   *', '**** ', '* *  ', '*   *']
    else:
        return ['     ', '     ', '     ', '     ', '     ']

def print_word(word):
    for i in range(5):
        for letter in word:
            print(print_letter(letter)[i], end='  ')
        print()

print_word('HAPPY')
print()
print_word('NEW')
print()
print_word('YEAR')


print("   *   ")
print("  ***  ")
print(" ***** ")
print("*******")
print("  ***  ")
