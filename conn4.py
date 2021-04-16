import pygame
from pygame.locals import *
import numpy as np
import os

BOARD = np.zeros((6,7))
PLAYER_1 = 1
PLAYER_2 = 5
SIZE = WIDTH, HEIGHT = 630, 540
WIDTH_CIRCLE = WIDTH / 7 #radius of each circle

#Colors
BLUE = 42, 73, 168
DARK_BLUE = 25, 54, 142
RED = 182, 5, 8
YELLOW = 242, 226, 0

#Initialize
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT + 90))
screen.fill(BLUE)

def draw_board():
    for row in range(6):
        for col in range(7):
            circle_center = (WIDTH_CIRCLE*col + WIDTH_CIRCLE /2) ,(WIDTH_CIRCLE*row + WIDTH_CIRCLE /2 + 90)
            pygame.draw.circle(screen, DARK_BLUE, circle_center, 40)
            pygame.draw.circle(screen, (2, 31, 124), circle_center, 41, 2)
    
    pygame.draw.line(screen, (2, 31, 124), (0, 90), (WIDTH, 90), 2)
    
    pygame.display.update()

def draw_circle():   
    
    for row in range(6):
        for col in range(7):
            if BOARD[row, col] == PLAYER_1:
                circle_center = (WIDTH_CIRCLE*col + WIDTH_CIRCLE /2) ,(WIDTH_CIRCLE*row + WIDTH_CIRCLE /2 + 90)
                pygame.draw.circle(screen, RED, circle_center, 39)
                pygame.display.update()
            elif BOARD[row, col] == PLAYER_2:
                circle_center = (WIDTH_CIRCLE*col + WIDTH_CIRCLE /2) ,(WIDTH_CIRCLE*row + WIDTH_CIRCLE /2 + 90)
                pygame.draw.circle(screen, YELLOW, circle_center, 39)
                pygame.display.update()

def get_pos():    
    (mouse_x, mouse_y) = pygame.mouse.get_pos() #Get Coords
    col = mouse_x // 90
    #row = (mouse_y - 90) // 90
    return col

def display_mpos(color):
    pygame.draw.rect(screen, BLUE, ((0,0), (WIDTH, 90))) 
    col = get_pos()
    circle_center = (WIDTH_CIRCLE*col + WIDTH_CIRCLE /2) ,45      
    pygame.draw.circle(screen, color, circle_center, 39)
   
def count_num():
    count = 0
    for row in range(6):
        for col in range(7):
            if BOARD[row, col] == PLAYER_1 or BOARD[row, col] == PLAYER_2:
                count = count + 1
    return count

def print_board():
    for row in range(6):
        for col in range(7):
            print(int(BOARD[row, col]), " ", end = "")
        print("")

def insert_num(col, turn):
    row = 5
    if BOARD[row, col] == 0:
        BOARD[row, col] = turn
        return row, col
    else:
        while True:
            row = row - 1  
            if row < 0:
                return None
            if BOARD[row, col] == 0:
                BOARD[row, col] = turn
                return row, col
            if row == 0:
                return row, col

def check_board(row, col, turn):

    #Horizontal
    if (col + 4) <= 7: #Right side from current point
        check_sum = 0
        for i in range(col, col + 4):
            check_sum += BOARD[row, i]
        if check_sum == turn * 4:
            return turn
    
    if (col - 4) >= -1: #Left side from current point 
        check_sum = 0
        for i in range(col, col - 4, -1): #step -1
            check_sum += BOARD[row, i]
        if check_sum == turn * 4:
            return turn
    

    #Vertical
    if (row + 4) <= 6: #Down from current point
        check_sum = 0
        for i in range(row, row + 4):
            check_sum += BOARD[i, col]
        if check_sum == turn * 4:
            return turn


    #Diagonals

    if (row + 4) <= 6 and (col + 4) <= 7: #Down and Right Diagonal
        check_sum = 0
        for i, j in zip(range(row, row +4), range(col, col + 4)):
            check_sum += BOARD[i, j]
        if check_sum == turn * 4:
            return turn
    
    if (row + 4) <= 6 and (col - 4) >= -1: #Down and Left Diagonal
        check_sum = 0
        for i, j in zip(range(row, row +4), range(col, col - 4, -1)):
            check_sum += BOARD[i, j]
        if check_sum == turn * 4:
            return turn
    
    if (row - 4) >= -1 and (col + 4) <= 7: #Up and Right Diagonal
        check_sum = 0
        for i, j in zip(range(row, row -4, -1), range(col, col + 4)):
            check_sum += BOARD[i, j]
        if check_sum == turn * 4:
            return turn
    
    if (row - 4) >= -1 and (col - 4) >= -1: #Up and Left Diagonal
        check_sum = 0
        for i, j in zip(range(row, row -4, -1), range(col, col + 4, -1)):
            check_sum += BOARD[i, j]
        if check_sum == turn * 4:
            return turn



def main():
    draw_board()
    result = None
    turn = PLAYER_1 
    while True:        
        
        if turn == PLAYER_1:
            color = RED
        else:
            color = YELLOW
        display_mpos(color) #Show where mouse it at
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()   
                     
            if event.type == pygame.MOUSEBUTTONDOWN: #When mouse is pressed   
 
                col = get_pos() #Get column to insert the disc              
                row, col = insert_num(col, turn) #Get Current Position
                
                draw_circle()  #Draw the dics that is inserted
                result = check_board(row, col, turn) #Check to see if anyone won
                count = count_num() #Count to check player's turn     
                if count % 2 == 0:
                    turn = PLAYER_1
                else:
                    turn = PLAYER_2    

                

        if result:
            if  result == PLAYER_1:
                pygame.time.delay(1000) 
                print("Red Wins")
                return
            elif result == PLAYER_2:
                pygame.time.delay(1000) 
                print("Yellow Wins")
                return
           
        pygame.display.flip()
        pygame.display.update()
    

main()