import os
import csv
from PIL import Image
import csv
from math import sqrt
from numba import jit

MY_DIR = os.path.dirname(os.path.realpath(__file__))
MY_CONFIG_FILE = 'starting_board_40x40_acorn.csv'


def display_board(board, gen):
    """
    take the board as a list of lists and display each entry.
    The board is a m x n rectangular list that contains
    either 0 or 1 in it.
    If it contains a 0, print a dot char ('.')
    If it contains a 1, print a star char ('*')
    recall that print( 'foo', end='') will prevent a newline to be printed
    TODO: iterate thru the list of lists and display each position of the board
    """
    my_image = Image.new('RGB', (len(board[0]),len(board)))
    my_image_pixels = my_image.load()
    img_fname = os.path.dirname(os.path.realpath(__file__)) + '/' + f'generation{gen}.png'
    # get the image size
    image_x_size = my_image.size[0]
    image_y_size = my_image.size[1]
    # iterate over x and y to pick the pixel color
    for y in range(image_y_size):

        for x in range(image_x_size):

            if board[y][x] == 1:
                pixel_color = (255,255,255)

                my_image_pixels[x, y] = pixel_color
            if board[y][x] == 0:
                pixel_color =(0,0,0)

                my_image_pixels[x, y] = pixel_color
    my_image.save(img_fname, 'png')

def t_b_sidemath(board,j,i,mod):
    if board[j][i-1] == 1:
        neighbor_num += 1
    if board[j+mod][i]==1:
        neighbor_num += 1
    if board[j+mod][i-1] == 1:
        neighbor_num += 1
    if board[j][i+1] == 1:
        neighbor_num += 1
    if board[j+mod][i+1] == 1:
        neighbor_num += 1

def cornermath(board,j,i,modj,modi):
    if board[j][i+modi] == 1:
        neighbor_num += 1

    if board[j+modj][i]==1:
        neighbor_num += 1

    if board[j+modj][i+modi] == 1:
        neighbor_num += 1

def midsidemath(board,j,i,modi):
    if board[j-1][i]==1:
        neighbor_num += 1
    if board[j+1][i]==1:
        neighbor_num += 1
    if board[j-1][i+modi] == 1:
        neighbor_num += 1
    if board[j+1][i+modi] == 1:
        neighbor_num += 1
    if board[j][i+modi]==1:
        neighbor_num += 1

def count_num_neighbors(board, i, j):
    """
    take the row and col and find out how many neighbors the square has
    """
    temp_num = j
    j = i
    i = temp_num
#j and i are swapped because the code below is backwards
    neighbor_num=0
    cols = len(board[0])
    rows = len(board)

    if j == 0:#TOP ROPE

        if i == 0:#left, top corner
            modj = +1
            modi = +1
            neighbor_num= cornermath(board,j, i, modj, modi)

        if i+1 == cols:#right, top corner
            modj = +1
            modi = -1
            neighbor_num= cornermath(board,j, i, modj, modi)

        else:
            if i != 0:#top side
                modj = +1
                neighbor_num= t_b_sidemath(board,j, i, modj)


    if j + 1 == rows:#LOW GROUND
        if i == 0:#left, bottom corner
            modj = -1
            modi = +1
            neighbor_num= cornermath(board,j, i, modj, modi)

        if i+1 == cols:#right, bottom corner
            modj = -1
            modi = -1
            neighbor_num= cornermath(board,j, i, modj, modi)

        else:
            if i != 0:#bottom side
                modj = -1
                neighbor_num= t_b_sidemath(board,j, i, modj)

    if j + 1 != rows:#NORMAL
        if j != 0:
            if i == 0:#leftside
                modi = +1
                neighbor_num = midsidemath(board,j,i,modi)

            if i + 1 == cols:#rightside
                modi = -1
                neighbor_num = midsidemath(board,j,i,modi)
            if i != 0:
                if i +1 != cols:#middlenorm

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

    # TODO: calculate the number of neighbors that a square has

    return neighbor_num

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
    len_row = len(board)
    len_col = len(board[0])
    map = []


    for i in range(len_row):
        map.append([])
        for j in range(len_col):

            neighbor_num = count_num_neighbors(board, i, j)

            if board[i][j] == 1:
                if neighbor_num <= 1:
                    map[i].append(0)
                if neighbor_num >= 4:
                    map[i].append(0)
                if neighbor_num == 2:
                    map[i].append(1)
                if neighbor_num == 3:
                    map[i].append(1)

            if board[i][j] == 0:
                if neighbor_num == 3:
                    map[i].append(1)
                else:
                    map[i].append(0)
    board = map
    return board

def load_board(board, infile_name):
    """
    open the CSV file and read in the values.  These will
    all be 1s or 0s and should populate the initial board.
    """
    with open(infile_name) as body_file:
            reader = csv.reader(body_file)
            count = 0
            for rows in reader:
                board.append([])
                for cols in rows:
                    board[count].append(int(cols))
                count += 1
    return board
    # TODO: load the csv file int the board

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

    load_board(board, infile_name)

    generations_to_do = 10

    for i in range(generations_to_do-1):
        display_board(board, i)
        board =update_board(board)


    # do one final display to show end state
    display_board(board, i+1)
    print('Conways Life is finished, please check images for results.')
    print('White is live, Black is dead')




if __name__ == '__main__':
    main()
