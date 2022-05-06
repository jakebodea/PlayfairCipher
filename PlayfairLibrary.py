def to_alpha(text):  # makes sure a text consists of only uppercase letters
    alpha = ''
    for i in range(len(text)):
        if text.lower()[i] >= 'a' and text[i] <= 'z':
            alpha += text[i].lower()

    return alpha.upper()


def remove_duplicates(text):  # removes duplicate letters
    new_text = ''

    for i in range(len(text)):
        ch = text[i]
        if ch not in new_text:
            new_text += ch

    return new_text


def spaced_twos(text):   # seperates a string into two characters + ' '
    spaced = ''

    for a, b in zip(text[::2], text[1::2]):
        spaced = spaced + a + b + ' '

    return spaced[:-1]


def add_x(text):  # adds an 'X' between double letters and at the end of a string if it has an odd number of characters
    idx = 0
    idx2 = 1
    enc_text = text
    temp = ''

    for i in range(len(text) - 1):
        if text[i] == text[i+1]:
            temp = enc_text[:idx + idx2] + 'X' + text[idx + 1:]
            enc_text = temp
            idx2 += 1
        idx += 1

    if len(enc_text) % 2 != 0:
        enc_text = enc_text + 'X'

    return enc_text


def keyword_prep(keyword):  # parent function to do all the necessary keyword funcitons
    keyword = to_alpha(keyword)
    keyword = remove_duplicates(keyword)
    return keyword


def message_prep(message):  # parent fuction to do all the necessary message functions
    message = message.upper()
    message = to_alpha(message)
    message = add_x(message)
    message = spaced_twos(message)
    message = message.replace('J', 'I')
    return message


# returns a list of lists of columns to help see if elements are same row, col, rect
def cols_and_rows(grid):
    numbers = []
    for i in range(5):
        col = []
        for j in range(5):
            if i + 5 * j > 24:
                break

            ch = grid[i + 5*j]
            col.append(ch)
        numbers.append(col)
    return numbers


def create_grid(keyword):
    alphabet = 'abcdefghiklmnopqrstuvwxyz'  # not including the letter j

    grid = keyword + alphabet
    grid = grid.upper()
    grid = remove_duplicates(grid)
    grid = to_alpha(grid)

    return cols_and_rows(grid)


def letter_col(letter, grid):  # finds column of letter in grid
    for i in range(5):
        for j in range(5):
            if grid[i][j] == letter:
                return i


def letter_row(letter, grid):  # finds row of letter in grid
    for i in range(5):
        for j in range(5):
            if grid[i][j] == letter:
                return j


def letter_info(letter, grid):
    return (letter_col(letter, grid), letter_row(letter, grid))


def letter_below(letter, grid):
    original = letter_info(letter, grid)
    col = original[0]
    row = original[1]
    if row+1 > 4:
        row = -1
    return grid[col][row+1]


def letter_right(letter, grid):
    original = letter_info(letter, grid)
    col = original[0]
    row = original[1]
    if col+1 > 4:
        col = -1
    return grid[col+1][row]


def rectangles(letter1, letter2, grid):   # swaps columns for letters in a rectangle
    info1 = letter_info(letter1, grid)
    info2 = letter_info(letter2, grid)

    col1 = info1[0]
    row1 = info1[1]

    col2 = info2[0]
    row2 = info2[1]
    
    return (grid[col2][row1], grid[col1][row2])


def encryption(keyword, message):
    plaintext = message_prep(message)
    ciphertext = ''
    grid = create_grid(keyword)

    for i in range(len(plaintext)-1):
        # makes sure we deal with non-space couples
        if plaintext[i] == ' ' or plaintext[i + 1] == ' ':
            pass
        else:
            first = plaintext[i]
            second = plaintext[i+1]

            # same column
            if letter_col(first, grid) == letter_col(second, grid):
                ciphertext = ciphertext + \
                    letter_below(first, grid) + letter_below(second, grid)

            # same row
            elif letter_row(first, grid) == letter_row(second, grid):
                ciphertext = ciphertext + \
                    letter_right(first, grid) + letter_right(second, grid)

            # rectangles
            else:
                letters = rectangles(first, second, grid)
                ciphertext = ciphertext + letters[0] + letters[1]

    return ciphertext


def letter_above(letter, grid):
    original = letter_info(letter, grid)
    col = original[0]
    row = original[1]
    if row-1 < 0:
        row = 5
    return grid[col][row-1]


def letter_left(letter, grid):
    original = letter_info(letter, grid)
    col = original[0]
    row = original[1]
    if col-1 < 0:
        col = 5
    return grid[col-1][row]


def decryption(keyword, ciphertext):
    grid = create_grid(keyword)
    ciphertext = ciphertext.replace('J', 'I')
    ciphertext = spaced_twos(ciphertext)
    plaintext = ''

    for i in range(len(ciphertext)-1):
        if ciphertext[i] == ' ' or ciphertext[i + 1] == ' ':
            pass

        else:

            first = ciphertext[i]
            second = ciphertext[i+1]

            # same col
            if letter_col(first, grid) == letter_col(second, grid):
                plaintext = plaintext + \
                    letter_above(first, grid) + letter_above(second, grid)

            # same row
            elif letter_row(first, grid) == letter_row(second, grid):
                plaintext = plaintext + \
                    letter_left(first, grid) + letter_left(second, grid)

            # rectangles
            else:
                letters = rectangles(first, second, grid)
                plaintext = plaintext + letters[0] + letters[1]

    # optional removing X to make it clearer but may confuse when X in the message
    return plaintext.replace('X', '')


def lets_try(keyword, message):  # function to quickly test some values
    print(message)
    cipher = encryption(keyword, message)
    print(cipher)
    plaintext = decryption(keyword, cipher)
    print(plaintext)

    if plaintext == to_alpha(message).upper():
        print('Hurray :)')


def very_cool_showoff():  # an interactive UI to demonstrate a message's encoding/decoding
    message = input('What message would you like encoded? ')
    keyword = input("What's the secret keyword? (Shh, keep it a secret) ")
    print('Your encoded message is ' + encryption(keyword,
                                                  message) + '. Feel free to share if you like.')
    print()
    print('Just a friendly FYI, once your friends decode the message, it will look like this: ' +
          decryption(keyword, encryption(keyword, message)))
