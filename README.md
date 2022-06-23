# Flatliner

[![unit-tests](https://github.com/hhc97/flatliner-src/actions/workflows/tests.yml/badge.svg)](https://github.com/hhc97/flatliner-src/actions/workflows/tests.yml)

This repo contains the core code for Flatliner ([https://flatliner.herokuapp.com/](https://flatliner.herokuapp.com/)). (Give it a couple seconds if it doesn't load immediately.)

### Basic overview

This project aims to convert Python 3 programs into a _single line_ of Python 3 code that is functionally equivalent
-- meaning that the output code will do the same thing as the input code even though it is only one line long.

For example, we can convert an entire interactive tic-tac-toe game into one line of code.

Input:
```python
"""
A simple two player tic tac toe implementation.
"""


def get_line(line: list) -> str:
    """
    Format a line of the board into a string.
    """
    temp_string = ' '
    spacer = ' | '
    temp_string += line[0]
    temp_string += spacer
    temp_string += line[1]
    temp_string += spacer
    temp_string += line[2]
    return temp_string


def print_board(state: list) -> None:
    """
    Prints the board.
    """
    horizontal_spacer = '---+---+---'
    print(get_line(state[0]))
    print(horizontal_spacer)
    print(get_line(state[1]))
    print(horizontal_spacer)
    print(get_line(state[2]))


def check_won(state: list) -> str:
    """
    Checks if a player has won the game and returns the winning symbol.
    ''
    'X'
    'O'
    """
    if state[0][0] == state[1][1] == state[2][2] and state[0][0] != ' ':
        return state[0][0]
    if state[0][2] == state[1][1] == state[2][0] and state[0][2] != ' ':
        return state[0][2]
    for r in range(3):
        if state[r][0] == state[r][1] == state[r][2] and state[r][0] != ' ':
            return state[r][0]
    for c in range(3):
        if state[0][c] == state[1][c] == state[2][c] and state[0][c] != ' ':
            return state[0][c]
    return ''


def have_space(state: list) -> bool:
    """
    Return whether there is still an empty space on the board.
    """
    if ' ' in state[0] or ' ' in state[1] or ' ' in state[2]:
        return True
    return False


def translate_move_to_english(move: list) -> str:
    """
    Translates move coordinates to English.
    [1, 2]
    """
    if move[0] == 0 and move[1] == 0:
        return 'top-left'
    if move[0] == 0 and move[1] == 1:
        return 'top-center'
    if move[0] == 0 and move[1] == 2:
        return 'top-right'
    if move[0] == 1 and move[1] == 0:
        return 'middle-left'
    if move[0] == 1 and move[1] == 1:
        return 'middle-center'
    if move[0] == 1 and move[1] == 2:
        return 'middle-right'
    if move[0] == 2 and move[1] == 0:
        return 'bottom-left'
    if move[0] == 2 and move[1] == 1:
        return 'bottom-center'
    if move[0] == 2 and move[1] == 2:
        return 'bottom-right'


def play_game() -> None:
    """
    Starts a new game played via the command line.
    """
    board = [[' ', ' ', ' '],
             [' ', ' ', ' '],
             [' ', ' ', ' ']]
    print_board(board)
    current_player = 'X'
    # while these two conditions are satisfied, the game has not ended
    while check_won(board) == '' and have_space(board):
        valid_moves = []
        # get valid moves using a nested for loop
        for row in range(3):
            for col in range(3):
                if board[row][col] == ' ':
                    valid_moves.append([row, col])
        move_number = 1
        # print the prompt for the player
        for move in valid_moves:
            print(str(move_number) + '.', translate_move_to_english(move))
            move_number += 1
        # obtain the move from the player. NOTE THAT THIS WILL CRASH IF THE PLAYER TROLLS
        player_selected_move = int(input('\nPlayer ' + current_player + ', select a move: '))
        actual_move = valid_moves[player_selected_move - 1]
        board[actual_move[0]][actual_move[1]] = current_player
        print_board(board)
        if current_player == 'X':
            current_player = 'O'
        else:
            current_player = 'X'
    winner = check_won(board)
    if winner == '':
        print('It was a tie :)')
    else:
        print('Congratulations, player ' + winner + ' won!')


if __name__ == '__main__':
    play_game()
```
Output:
```python
(lambda _Y: (lambda get_line: (lambda print_board: (lambda check_won: (lambda have_space: (lambda translate_move_to_english: (lambda play_game: (play_game() if __name__ == '__main__' else None))(lambda: (lambda board: [print_board(board), (lambda current_player: (lambda actual_move, current_player, move_number, player_selected_move, valid_moves: (lambda _loop1: _loop1(actual_move, current_player, move_number, player_selected_move, valid_moves))(_Y(lambda _loop1: (lambda actual_move, current_player, move_number, player_selected_move, valid_moves: ((lambda valid_moves: (lambda _term3, _items3: (lambda _targ3: (lambda _targ3, row: (lambda _loop3: _loop3(_targ3, row))(_Y(lambda _loop3: (lambda _targ3, row: ((lambda row: (lambda _term4, _items4: (lambda _targ4: (lambda _targ4, col: (lambda _loop4: _loop4(_targ4, col))(_Y(lambda _loop4: (lambda _targ4, col: ((lambda col: ([valid_moves.append([row, col]), (lambda _targ4: _loop4(_targ4, col))(next(_items4, _term4))][-1] if board[row][col] == ' ' else (lambda _targ4: _loop4(_targ4, col))(next(_items4, _term4))))(_targ4)) if _targ4 is not _term4 else (lambda _targ3: _loop3(_targ3, row))(next(_items3, _term3))))))(_targ4 if "_targ4" in dir() else None, col if "col" in dir() else None))(next(_items4, _term4)))([], iter(range(3))))(_targ3)) if _targ3 is not _term3 else (lambda move_number: (lambda _term2, _items2: (lambda _targ2: (lambda _targ2, move, move_number: (lambda _loop2: _loop2(_targ2, move, move_number))(_Y(lambda _loop2: (lambda _targ2, move, move_number: ((lambda move: [print((str(move_number) + '.'), translate_move_to_english(move)), (lambda move_number: (lambda _targ2: _loop2(_targ2, move, move_number))(next(_items2, _term2)))((move_number + 1))][-1])(_targ2)) if _targ2 is not _term2 else (lambda player_selected_move: (lambda actual_move: [[print_board(board), ((lambda current_player: _loop1(actual_move, current_player, move_number, player_selected_move, valid_moves))('O') if current_player == 'X' else (lambda current_player: _loop1(actual_move, current_player, move_number, player_selected_move, valid_moves))('X'))][-1] for board[actual_move[0]][actual_move[1]] in [current_player]][0])(valid_moves[(player_selected_move - 1)]))(int(input((('\nPlayer ' + current_player) + ', select a move: '))))))))(_targ2 if "_targ2" in dir() else None, move if "move" in dir() else None, move_number if "move_number" in dir() else None))(next(_items2, _term2)))([], iter(valid_moves)))(1)))))(_targ3 if "_targ3" in dir() else None, row if "row" in dir() else None))(next(_items3, _term3)))([], iter(range(3))))([])) if check_won(board) == '' and have_space(board) else (lambda winner: (print('It was a tie :)') if winner == '' else print((('Congratulations, player ' + winner) + ' won!'))))(check_won(board))))))(actual_move if "actual_move" in dir() else None, current_player if "current_player" in dir() else None, move_number if "move_number" in dir() else None, player_selected_move if "player_selected_move" in dir() else None, valid_moves if "valid_moves" in dir() else None))('X')][-1])([[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']])))(lambda move: ('top-left' if move[0] == 0 and move[1] == 0 else ('top-center' if move[0] == 0 and move[1] == 1 else ('top-right' if move[0] == 0 and move[1] == 2 else ('middle-left' if move[0] == 1 and move[1] == 0 else ('middle-center' if move[0] == 1 and move[1] == 1 else ('middle-right' if move[0] == 1 and move[1] == 2 else ('bottom-left' if move[0] == 2 and move[1] == 0 else ('bottom-center' if move[0] == 2 and move[1] == 1 else ('bottom-right' if move[0] == 2 and move[1] == 2 else None)))))))))))(lambda state: (True if ' ' in state[0] or ' ' in state[1] or ' ' in state[2] else False)))(lambda state: (state[0][0] if state[0][0] == state[1][1] == state[2][2] and state[0][0] != ' ' else (state[0][2] if state[0][2] == state[1][1] == state[2][0] and state[0][2] != ' ' else (lambda _term6, _items6: (lambda _targ6: (lambda _targ6, r: (lambda _loop6: _loop6(_targ6, r))(_Y(lambda _loop6: (lambda _targ6, r: ((lambda r: (state[r][0] if state[r][0] == state[r][1] == state[r][2] and state[r][0] != ' ' else (lambda _targ6: _loop6(_targ6, r))(next(_items6, _term6))))(_targ6)) if _targ6 is not _term6 else (lambda _term5, _items5: (lambda _targ5: (lambda _targ5, c: (lambda _loop5: _loop5(_targ5, c))(_Y(lambda _loop5: (lambda _targ5, c: ((lambda c: (state[0][c] if state[0][c] == state[1][c] == state[2][c] and state[0][c] != ' ' else (lambda _targ5: _loop5(_targ5, c))(next(_items5, _term5))))(_targ5)) if _targ5 is not _term5 else ''))))(_targ5 if "_targ5" in dir() else None, c if "c" in dir() else None))(next(_items5, _term5)))([], iter(range(3)))))))(_targ6 if "_targ6" in dir() else None, r if "r" in dir() else None))(next(_items6, _term6)))([], iter(range(3)))))))(lambda state: (lambda horizontal_spacer: [print(get_line(state[0])), [print(horizontal_spacer), [print(get_line(state[1])), [print(horizontal_spacer), print(get_line(state[2]))][-1]][-1]][-1]][-1])('---+---+---')))(lambda line: (lambda temp_string: (lambda spacer: (lambda temp_string: (lambda temp_string: (lambda temp_string: (lambda temp_string: (lambda temp_string: temp_string)((temp_string + line[2])))((temp_string + spacer)))((temp_string + line[1])))((temp_string + spacer)))((temp_string + line[0])))(' | '))(' ')))((lambda f: (lambda x: x(x))(lambda y: f(lambda *args: y(y)(*args)))))
```

Running this output shows us it works like the original code, how neat!
![](/assets/tic-tac-toe.gif)

For more examples of what can be converted, see [code_examples](/code_examples).

### Misc

For those interested in how this works, the conversion happens in [flatline.py](/flatline.py). This program
can also convert itself into one line! See [flatline_one_lined.py](/demo/flatline_one_lined.py).


### Acknowledgement

This project was made together with [Naaz](https://github.com/naazsibia) and [Ritvik](https://github.com/AipioxTechson)
for a compilers course at the University of Toronto.

While implementing our project, we also came across an excellent python 2 implementation of the same concept [here](https://github.com/csvoss/onelinerizer).
