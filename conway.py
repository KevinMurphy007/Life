import os
import csv

MY_DIR = os.path.dirname(os.path.realpath(__file__))
MY_CONFIG_FILE = 'starting_board_10x10.csv'


def master_board(location, board, gen):
    """
    take the board as a list of lists and display each entry.
    The board is a m x n rectangular list that contains
    either 0 or 1 in it.

    If it contains a 0, print a dot char ('.')
    If it contains a 1, print a star char ('*')
    recall that print( 'foo', end='') will prevent a newline to be printed

    TODO: iterate thru the list of lists and display each position of the board
    """

    print(f'Displaying board for generation {gen}')

    # TODO: complete the display board code

    with open(location) as body_file:
            reader = csv.reader(body_file)
            map = []
            count = 0
            for rows in reader:
                print()
                map.append([])
                for cols in rows:
                    if int(cols) == 1:
                        print('*', end='')

                    if int(cols) == 0:
                        print('.', end='')

                    map[count].append(int(cols))
                count += 1
            print()
            reader = update_board(map)
    #for gen number use (update board ) recursion becasue the gen num
    #is the number off generations the board goes thru DUMMY


def count_num_neighbors_pop(board):
    """
    take the row and col and find out how many neighbors the square has
    """
    rows = len(board)
    cols = len(board[0])
    neighbor_num=0
    for j in range(rows):
        if j == 0:#TOP ROPE
            for i in range(cols):

                if i == 0:#left, top corner
                    if board[j][i+1] == 1:
                        neighbor_num += 1
                    if board[j+1][i]==1:
                        neighbor_num += 1
                    if board[j+1][i+1] == 1:
                        neighbor_num += 1

                if i+1 == cols:#right, top corner
                    if board[j][i-1] == 1:
                        neighbor_num += 1
                    if board[j+1][i]==1:
                        neighbor_num += 1
                    if board[j+1][i-1] == 1:
                        neighbor_num += 1

                else:
                    if i != 0:#top side
                        if board[j][i-1] == 1:
                            neighbor_num += 1
                        if board[j+1][i]==1:
                            neighbor_num += 1
                        if board[j+1][i-1] == 1:
                            neighbor_num += 1

                        if board[j][i+1] == 1:
                            neighbor_num += 1

                        if board[j+1][i+1] == 1:
                            neighbor_num += 1


        if j + 1 == rows:#LOW GROUND
            for i in range(cols):
                if i == 0:#left, bottom corner
                    if board[j][i+1] == 1:
                        neighbor_num += 1
                    if board[j-1][i]==1:
                        neighbor_num += 1
                    if board[j-1][i+1] == 1:
                        neighbor_num += 1


                if i+1 == cols:#right, bottom corner
                    if board[j][i-1] == 1:
                        neighbor_num += 1
                    if board[j-1][i]==1:
                        neighbor_num += 1
                    if board[j-1][i-1] == 1:
                        neighbor_num += 1

                else:
                    if i != 0:#bottom side
                        if board[j][i-1] == 1:
                            neighbor_num += 1
                        if board[j-1][i]==1:
                            neighbor_num += 1
                        if board[j-1][i-1] == 1:
                            neighbor_num += 1

                        if board[j][i+1] == 1:
                            neighbor_num += 1

                        if board[j-1][i+1] == 1:
                            neighbor_num += 1

        if j + 1 != rows:#NORMAL
            if j != 0:
                for i in range(cols):
                    if i != 0:
                        if i +1 != cols:
                            if board[j][i-1] == 1:
                                neighbor_num += 1

                            if board[j-1][i]==1:
                                neighbor_num += 1

                            if board[j-1][i-1] == 1:
                                neighbor_num += 1

                            if board[j+1][i]==1:
                                neighbor_num += 1

                            if board[j-1][i+1] == 1:
                                neighbor_num += 1

                            if board[j+1][i-1] == 1:
                                neighbor_num += 1

                            if board[j+1][i+1] == 1:
                                neighbor_num += 1

                            if board[j][i+1] == 1:
                                neighbor_num += 1





    return neighbor_num
    # TODO: calculate the number of neighbors that a square has



def update_board(board):
    """
    This function will update the board using the rules for
    how to update each square.

    iterate thru the board.  When the function ends, the board should be
    updated to reflect the next generation.

    The rules for updating the board from 1 generation to another:

    if the square has a '1' in it it is considered "populated"
    if the square has a '0' in it is is considered 'empty'

    Check each square in your grid.
    If it has a 1 in it, then :
         * if it has 1 or 0 "neighbors" (populated adjacent squares, including
         diagonals), then it "dies" (loneliness).  So the square will be
         updated to be 0.
         * if it has 4 or more "neighbors" (including diagonals), then it
         "dies" (overcrowding).  So the square will be updated to 0
         * if it has 2 or 3 neighbors, then it is happy and stays alive
    If it has a 0 in it, then :
         * If it has precisely 3 neighbors (not more, not fewer), then a
         new entity is "born".  So the square will be updated to 1
         * Any other number of neighbors causes no change and the square
         stays 0
    Edge/Corner case :
         for squares on the edge or corner of the map, DO NOT wrap around the
         map.  ie., a corner square has only 3 neighboring squares.  a
         Non-corner Edge square has 5 neighbors.
    """
    for row in board:
        for col in row:
            neighbor_num = count_num_neighbors_pop(board)
            if col == 1:
                if neighbor_num <= 1:
                    col = 0
                if neighbor_num >= 4:
                    col = 0
            if col == 0:
                if neighbor_num == 3:
                    col = 1
    return board


    # TODO: modify the board to reflect the next generation

def main():
    """
    Main loop
    """
    print('hello, starting Conway Life')

    # Init primary vars
    board = []
    num_rows = 10
    num_cols = 10

    infile_name = MY_DIR + '/' + MY_CONFIG_FILE

    generations_to_do = 10

    for i in range(generations_to_do-1):
        master_board(infile_name, board, i)

    # do one final display to show end state
    master_board(infile_name, board, i+1)




if __name__ == '__main__':
    main()
