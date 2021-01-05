import pygame
import random
import time
from pygame.locals import *


pygame.init()
screen = pygame.display.set_mode([500, 500])
pygame.display.set_caption('TicTacToe 4x4')
gameIcon = pygame.image.load('images/table2.png')
pygame.transform.scale(gameIcon, (10, 10))
pygame.display.set_icon(gameIcon)


def blankMatrix():
    return [[' ', ' ', ' ', ' '], [' ', ' ', ' ', ' '], [' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ']]

# function for printing text into pygame window with parameters:
# -string for printing
# -x and y are coordinates of text rectangle center
# -size is size of text in pixels
def printText(string, x, y, size):
    font = pygame.font.Font('freesansbold.ttf', size)
    text = font.render(string, True, (255, 255, 255))
    textRect = text.get_rect()
    textRect.center = (x, y)
    screen.blit(text, textRect)
    pygame.display.update()

# function for window which will ask player which sign
# he/she wants to be, X or O and returns that sign(as string)
def firstWindow():
    beginning = True
    bg = pygame.display.set_mode([500, 500])
    bg.fill([255, 200, 100])
    printText('Welcome to TicTacToe 4x4!', 250, 40, 35)
    printText('Choose your sign:', 250, 150, 45)
    pygame.draw.rect(bg, (255, 255, 255), (100, 250, 100, 100), 5, 5, 5, 5)
    printText('X', 150, 300, 40)
    pygame.draw.rect(bg, (255, 255, 255), (300, 250, 100, 100), 5, 5, 5, 5)
    printText('O', 350, 300, 40)
    pygame.display.update()
    while beginning:
        events = pygame.event.get()
        for e in events:
            if e.type == pygame.QUIT:
                pygame.quit()
                quit()
            if e.type == MOUSEBUTTONUP:
                x, y = pygame.mouse.get_pos()
                if 100 < x < 200 and 250 < y < 350:
                    return 'x'
                elif 300 < x < 400 and 250 < y < 350:
                    return 'o'

# function for window which will ask player what difficulty
# he/she wants to play and returns that difficulty(as string/chr)
def secondWindow():
    second = True
    bg = pygame.display.set_mode([500, 500])
    bg.fill([255, 200, 100])
    printText('Welcome to TicTacToe 4x4!', 250, 40, 35)
    printText('Choose difficulty:', 250, 150, 45)
    pygame.draw.rect(bg, (98, 243, 93), (50, 250, 100, 70), 0, 5, 5, 5)
    printText('Easy', 100, 285, 30)
    pygame.draw.rect(bg, (85, 125, 255), (175, 250, 150, 70), 0, 5, 5, 5)
    printText('Medium', 250, 285, 30)
    pygame.draw.rect(bg, (255, 61, 61), (350, 250, 100, 70), 0, 5, 5, 5)
    printText('Hard', 400, 285, 30)
    pygame.display.update()
    while second:
        events = pygame.event.get()
        for e in events:
            if e.type == pygame.QUIT:
                pygame.quit()
                quit()
            if e.type == MOUSEBUTTONUP:
                x, y = pygame.mouse.get_pos()
                if 50 < x < 150 and 250 < y < 320:
                    return 'easy'
                elif 175 < x < 325 and 250 < y < 320:
                    return 'medium'
                elif 350 < x < 450 and 250 < y < 320:
                    return 'hard'


playerSign = firstWindow()
gameDifficulty = secondWindow()

# giving player and computer their signs for game
if playerSign == 'x':
    computerSign = 'o'
else:
    computerSign = 'x'

# function which defines computers turn; depending of difficulty which player has chosen, computer will play
# if difficulty is easy, computer will play randomly
# if difficulty is medium, computer will know to find if there is row, column, diagonal or square without one player
# sign and it will prevent the player from winning; if there isn't that combination, it plays randomly
# if difficulty is hard, computer will know to find everything like in medium, but also if there are three computer's
# signs in row, column, diagonal or square, it will know that it should take fourth there and win
def computerTurn():
    pygame.draw.rect(screen, (255, 200, 100), (0, 0, 500, 100))
    printText("Computer's turn", 250, 40, 35)
    state = False
    if gameDifficulty == 'hard':
        state, a, b = computerTurnHard()
        if not state:
            state, a, b = computerTurnMedium()
    elif gameDifficulty == 'medium':
        state, a, b = computerTurnMedium()
    if not state:
        tmp = random.randint(0, 15)
        a = tmp // 4
        b = tmp % 4
        if matrix[a][b] == ' ':
            matrix[a][b] = computerSign
            time.sleep(1)
            if computerSign == 'x':
                printText('X', b * 75 + 138, a * 75 + 142, 60)
            else:
                printText('O', b * 75 + 138, a * 75 + 142, 60)
        else:
            computerTurn()
    else:
        matrix[a][b] = computerSign
        time.sleep(1)
        if computerSign == 'x':
            printText('X', b * 75 + 138, a * 75 + 142, 60)
        else:
            printText('O', b * 75 + 138, a * 75 + 142, 60)

    pygame.draw.rect(screen, (255, 200, 100), (0, 0, 500, 100))
    printText("Your turn", 250, 40, 35)
    pygame.display.update()


def computerTurnHard():
    # searching for rows
    for row in matrix:
        if row[0] == row[1] == row[2] == computerSign and row[3] == ' ':
            row[3] = computerSign
            return True, matrix.index(row), 3
        elif row[0] == row[1] == row[3] == computerSign and row[2] == ' ':
            row[2] = computerSign
            return True, matrix.index(row), 2
        elif row[0] == row[1] == row[2] == computerSign and row[1] == ' ':
            row[3] = computerSign
            return True, matrix.index(row), 1
        elif row[3] == row[1] == row[2] == computerSign and row[0] == ' ':
            row[0] = computerSign
            return True, matrix.index(row), 0
    # searching for columns
    if matrix[0][0] == matrix[1][0] == matrix[2][0] == computerSign and matrix[3][0] == ' ':
        matrix[3][0] = computerSign
        return True, 3, 0
    elif matrix[0][0] == matrix[1][0] == matrix[3][0] == computerSign and matrix[2][0] == ' ':
        matrix[2][0] = computerSign
        return True, 2, 0
    elif matrix[0][0] == matrix[3][0] == matrix[2][0] == computerSign and matrix[1][0] == ' ':
        matrix[1][0] = computerSign
        return True, 1, 0
    elif matrix[3][0] == matrix[1][0] == matrix[2][0] == computerSign and matrix[0][0] == ' ':
        matrix[0][0] = computerSign
        return True, 0, 0
    elif matrix[0][1] == matrix[1][1] == matrix[2][1] == computerSign and matrix[3][1] == ' ':
        matrix[3][1] = computerSign
        return True, 3, 1
    elif matrix[0][1] == matrix[1][1] == matrix[3][1] == computerSign and matrix[2][1] == ' ':
        matrix[2][1] = computerSign
        return True, 2, 1
    elif matrix[0][1] == matrix[3][1] == matrix[2][1] == computerSign and matrix[1][1] == ' ':
        matrix[1][1] = computerSign
        return True, 1, 1
    elif matrix[3][1] == matrix[1][1] == matrix[2][1] == computerSign and matrix[0][1] == ' ':
        matrix[0][1] = computerSign
        return True, 0, 1
    elif matrix[0][2] == matrix[1][2] == matrix[2][2] == computerSign and matrix[3][2] == ' ':
        matrix[3][2] = computerSign
        return True, 3, 2
    elif matrix[0][2] == matrix[1][2] == matrix[3][2] == computerSign and matrix[2][2] == ' ':
        matrix[2][2] = computerSign
        return True, 2, 2
    elif matrix[0][2] == matrix[3][2] == matrix[2][2] == computerSign and matrix[1][2] == ' ':
        matrix[1][2] = computerSign
        return True, 1, 2
    elif matrix[3][2] == matrix[1][2] == matrix[2][2] == computerSign and matrix[0][2] == ' ':
        matrix[0][2] = computerSign
        return True, 0, 2
    elif matrix[0][3] == matrix[1][3] == matrix[2][3] == computerSign and matrix[3][3] == ' ':
        matrix[3][3] = computerSign
        return True, 3, 3
    elif matrix[0][3] == matrix[1][3] == matrix[3][3] == computerSign and matrix[2][3] == ' ':
        matrix[2][3] = computerSign
        return True, 2, 3
    elif matrix[0][3] == matrix[2][3] == matrix[3][3] == computerSign and matrix[1][3] == ' ':
        matrix[1][3] = computerSign
        return True, 1, 3
    elif matrix[1][3] == matrix[2][3] == matrix[3][3] == computerSign and matrix[0][3] == ' ':
        matrix[0][3] = computerSign
        return True, 0, 3
    elif matrix[0][0] == matrix[1][1] == matrix[2][2] == computerSign and matrix[3][3] == ' ':
        matrix[3][3] = computerSign
        return True, 3, 3
    elif matrix[0][0] == matrix[1][1] == matrix[3][3] == computerSign and matrix[2][2] == ' ':
        matrix[3][3] = computerSign
        return True, 2, 2
    elif matrix[0][0] == matrix[3][3] == matrix[2][2] == computerSign and matrix[1][1] == ' ':
        matrix[1][1] = computerSign
        return True, 1, 1
    elif matrix[3][3] == matrix[1][1] == matrix[2][2] == computerSign and matrix[0][0] == ' ':
        matrix[0][0] = computerSign
        return True, 0, 0
    elif matrix[0][3] == matrix[1][2] == matrix[2][1] == computerSign and matrix[3][0] == ' ':
        matrix[3][0] = computerSign
        return True, 3, 0
    elif matrix[0][3] == matrix[1][2] == matrix[3][0] == computerSign and matrix[2][1] == ' ':
        matrix[2][1] = computerSign
        return True, 2, 1
    elif matrix[0][3] == matrix[3][0] == matrix[2][1] == computerSign and matrix[1][2] == ' ':
        matrix[1][2] = computerSign
        return True, 1, 2
    elif matrix[3][0] == matrix[1][2] == matrix[2][1] == computerSign and matrix[0][3] == ' ':
        matrix[0][3] = computerSign
        return True, 0, 3
    # searching for squares
    # first square
    elif matrix[0][0] == matrix[0][1] == matrix[1][0] == computerSign and matrix[1][1] == ' ':
        matrix[1][1] = computerSign
        return True, 1, 1
    elif matrix[0][0] == matrix[0][1] == matrix[1][1] == computerSign and matrix[1][0] == ' ':
        matrix[1][0] = computerSign
        return True, 1, 0
    elif matrix[0][0] == matrix[1][1] == matrix[1][0] == computerSign and matrix[0][1] == ' ':
        matrix[0][1] = computerSign
        return True, 0, 1
    elif matrix[1][1] == matrix[0][1] == matrix[1][0] == computerSign and matrix[0][0] == ' ':
        matrix[0][0] = computerSign
        return True, 0, 0
    # second square
    elif matrix[0][1] == matrix[0][2] == matrix[1][1] == computerSign and matrix[1][2] == ' ':
        matrix[1][2] = computerSign
        return True, 1, 2
    elif matrix[0][1] == matrix[0][2] == matrix[1][2] == computerSign and matrix[1][1] == ' ':
        matrix[1][1] = computerSign
        return True, 1, 1
    elif matrix[0][1] == matrix[1][2] == matrix[1][1] == computerSign and matrix[0][2] == ' ':
        matrix[0][2] = computerSign
        return True, 0, 2
    elif matrix[0][2] == matrix[1][2] == matrix[1][1] == computerSign and matrix[0][1] == ' ':
        matrix[0][1] = computerSign
        return True, 0, 1
    # third square
    elif matrix[0][2] == matrix[0][3] == matrix[1][2] == computerSign and matrix[1][3] == ' ':
        matrix[1][3] = computerSign
        return True, 1, 3
    elif matrix[0][2] == matrix[0][3] == matrix[1][3] == computerSign and matrix[1][2] == ' ':
        matrix[1][2] = computerSign
        return True, 1, 2
    elif matrix[0][2] == matrix[1][2] == matrix[1][3] == computerSign and matrix[0][3] == ' ':
        matrix[0][3] = computerSign
        return True, 0, 3
    elif matrix[0][3] == matrix[1][2] == matrix[1][3] == computerSign and matrix[0][2] == ' ':
        matrix[0][2] = computerSign
        return True, 0, 2
    # fourth square
    elif matrix[1][0] == matrix[1][1] == matrix[2][0] == computerSign and matrix[2][1] == ' ':
        matrix[2][1] = computerSign
        return True, 2, 1
    elif matrix[1][0] == matrix[1][1] == matrix[2][1] == computerSign and matrix[2][0] == ' ':
        matrix[2][0] = computerSign
        return True, 2, 0
    elif matrix[1][0] == matrix[2][1] == matrix[2][0] == computerSign and matrix[1][1] == ' ':
        matrix[1][1] = computerSign
        return True, 1, 1
    elif matrix[2][1] == matrix[1][1] == matrix[2][0] == computerSign and matrix[1][0] == ' ':
        matrix[1][0] = computerSign
        return True, 1, 0
    # fifth square
    elif matrix[1][1] == matrix[1][2] == matrix[2][1] == computerSign and matrix[2][2] == ' ':
        matrix[2][2] = computerSign
        return True, 2, 2
    elif matrix[1][1] == matrix[1][2] == matrix[2][2] == computerSign and matrix[2][1] == ' ':
        matrix[2][1] = computerSign
        return True, 2, 1
    elif matrix[1][1] == matrix[2][2] == matrix[2][1] == computerSign and matrix[1][2] == ' ':
        matrix[1][2] = computerSign
        return True, 1, 2
    elif matrix[1][2] == matrix[2][2] == matrix[2][1] == computerSign and matrix[1][1] == ' ':
        matrix[1][1] = computerSign
        return True, 1, 1
    # sixth square
    elif matrix[1][2] == matrix[1][3] == matrix[2][2] == computerSign and matrix[2][3] == ' ':
        matrix[2][3] = computerSign
        return True, 2, 3
    elif matrix[1][2] == matrix[1][3] == matrix[2][3] == computerSign and matrix[2][2] == ' ':
        matrix[2][2] = computerSign
        return True, 2, 2
    elif matrix[1][2] == matrix[2][2] == matrix[2][3] == computerSign and matrix[1][3] == ' ':
        matrix[1][3] = computerSign
        return True, 1, 3
    elif matrix[1][3] == matrix[2][2] == matrix[2][3] == computerSign and matrix[1][2] == ' ':
        matrix[1][2] = computerSign
        return True, 1, 2
    # seventh square
    elif matrix[2][0] == matrix[2][1] == matrix[3][0] == computerSign and matrix[3][1] == ' ':
        matrix[3][1] = computerSign
        return True, 3, 1
    elif matrix[2][0] == matrix[2][1] == matrix[3][1] == computerSign and matrix[3][0] == ' ':
        matrix[3][0] = computerSign
        return True, 3, 0
    elif matrix[2][0] == matrix[3][1] == matrix[3][0] == computerSign and matrix[2][1] == ' ':
        matrix[2][1] = computerSign
        return True, 2, 1
    elif matrix[3][1] == matrix[2][1] == matrix[3][0] == computerSign and matrix[2][0] == ' ':
        matrix[2][0] = computerSign
        return True, 2, 0
    # eighth square
    elif matrix[2][1] == matrix[2][2] == matrix[3][1] == computerSign and matrix[3][2] == ' ':
        matrix[3][2] = computerSign
        return True, 3, 2
    elif matrix[2][1] == matrix[2][2] == matrix[3][2] == computerSign and matrix[3][1] == ' ':
        matrix[3][1] = computerSign
        return True, 3, 1
    elif matrix[2][1] == matrix[3][2] == matrix[3][1] == computerSign and matrix[2][2] == ' ':
        matrix[2][2] = computerSign
        return True, 2, 2
    elif matrix[2][2] == matrix[3][2] == matrix[3][1] == computerSign and matrix[2][1] == ' ':
        matrix[2][1] = computerSign
        return True, 2, 1
    # ninth square
    elif matrix[2][2] == matrix[2][3] == matrix[3][2] == computerSign and matrix[3][3] == ' ':
        matrix[3][3] = computerSign
        return True, 3, 3
    elif matrix[2][2] == matrix[2][3] == matrix[3][3] == computerSign and matrix[3][2] == ' ':
        matrix[3][2] = computerSign
        return True, 3, 2
    elif matrix[2][2] == matrix[3][2] == matrix[3][3] == computerSign and matrix[2][3] == ' ':
        matrix[2][3] = computerSign
        return True, 2, 3
    elif matrix[2][3] == matrix[3][2] == matrix[3][3] == computerSign and matrix[2][2] == ' ':
        matrix[2][2] = computerSign
        return True, 2, 2
    else:
        return False, 4, 4


def computerTurnMedium():
    # searching for rows
    for row in matrix:
        if row[0] == row[1] == row[2] == playerSign and row[3] == ' ':
            row[3] = computerSign
            return True, matrix.index(row), 3
        elif row[0] == row[1] == row[3] == playerSign and row[2] == ' ':
            row[2] = computerSign
            return True, matrix.index(row), 2
        elif row[0] == row[1] == row[2] == playerSign and row[1] == ' ':
            row[3] = computerSign
            return True, matrix.index(row), 1
        elif row[3] == row[1] == row[2] == playerSign and row[0] == ' ':
            row[0] = computerSign
            return True, matrix.index(row), 0
    # searching for columns
    if matrix[0][0] == matrix[1][0] == matrix[2][0] == playerSign and matrix[3][0] == ' ':
        matrix[3][0] = computerSign
        return True, 3, 0
    elif matrix[0][0] == matrix[1][0] == matrix[3][0] == playerSign and matrix[2][0] == ' ':
        matrix[2][0] = computerSign
        return True, 2, 0
    elif matrix[0][0] == matrix[3][0] == matrix[2][0] == playerSign and matrix[1][0] == ' ':
        matrix[1][0] = computerSign
        return True, 1, 0
    elif matrix[3][0] == matrix[1][0] == matrix[2][0] == playerSign and matrix[0][0] == ' ':
        matrix[0][0] = computerSign
        return True, 0, 0
    elif matrix[0][1] == matrix[1][1] == matrix[2][1] == playerSign and matrix[3][1] == ' ':
        matrix[3][1] = computerSign
        return True, 3, 1
    elif matrix[0][1] == matrix[1][1] == matrix[3][1] == playerSign and matrix[2][1] == ' ':
        matrix[2][1] = computerSign
        return True, 2, 1
    elif matrix[0][1] == matrix[3][1] == matrix[2][1] == playerSign and matrix[1][1] == ' ':
        matrix[1][1] = computerSign
        return True, 1, 1
    elif matrix[3][1] == matrix[1][1] == matrix[2][1] == playerSign and matrix[0][1] == ' ':
        matrix[0][1] = computerSign
        return True, 0, 1
    elif matrix[0][2] == matrix[1][2] == matrix[2][2] == playerSign and matrix[3][2] == ' ':
        matrix[3][2] = computerSign
        return True, 3, 2
    elif matrix[0][2] == matrix[1][2] == matrix[3][2] == playerSign and matrix[2][2] == ' ':
        matrix[2][2] = computerSign
        return True, 2, 2
    elif matrix[0][2] == matrix[3][2] == matrix[2][2] == playerSign and matrix[1][2] == ' ':
        matrix[1][2] = computerSign
        return True, 1, 2
    elif matrix[3][2] == matrix[1][2] == matrix[2][2] == playerSign and matrix[0][2] == ' ':
        matrix[0][2] = computerSign
        return True, 0, 2
    elif matrix[0][3] == matrix[1][3] == matrix[2][3] == playerSign and matrix[3][3] == ' ':
        matrix[3][3] = computerSign
        return True, 3, 3
    elif matrix[0][3] == matrix[1][3] == matrix[3][3] == playerSign and matrix[2][3] == ' ':
        matrix[2][3] = computerSign
        return True, 2, 3
    elif matrix[0][3] == matrix[2][3] == matrix[3][3] == playerSign and matrix[1][3] == ' ':
        matrix[1][3] = computerSign
        return True, 1, 3
    elif matrix[1][3] == matrix[2][3] == matrix[3][3] == playerSign and matrix[0][3] == ' ':
        matrix[0][3] = computerSign
        return True, 0, 3
    elif matrix[0][0] == matrix[1][1] == matrix[2][2] == playerSign and matrix[3][3] == ' ':
        matrix[3][3] = computerSign
        return True, 3, 3
    elif matrix[0][0] == matrix[1][1] == matrix[3][3] == playerSign and matrix[2][2] == ' ':
        matrix[3][3] = computerSign
        return True, 2, 2
    elif matrix[0][0] == matrix[3][3] == matrix[2][2] == playerSign and matrix[1][1] == ' ':
        matrix[1][1] = computerSign
        return True, 1, 1
    elif matrix[3][3] == matrix[1][1] == matrix[2][2] == playerSign and matrix[0][0] == ' ':
        matrix[0][0] = computerSign
        return True, 0, 0
    elif matrix[0][3] == matrix[1][2] == matrix[2][1] == playerSign and matrix[3][0] == ' ':
        matrix[3][0] = computerSign
        return True, 3, 0
    elif matrix[0][3] == matrix[1][2] == matrix[3][0] == playerSign and matrix[2][1] == ' ':
        matrix[2][1] = computerSign
        return True, 2, 1
    elif matrix[0][3] == matrix[3][0] == matrix[2][1] == playerSign and matrix[1][2] == ' ':
        matrix[1][2] = computerSign
        return True, 1, 2
    elif matrix[3][0] == matrix[1][2] == matrix[2][1] == playerSign and matrix[0][3] == ' ':
        matrix[0][3] = computerSign
        return True, 0, 3
    # searching for squares
    # first square
    elif matrix[0][0] == matrix[0][1] == matrix[1][0] == playerSign and matrix[1][1] == ' ':
        matrix[1][1] = computerSign
        return True, 1, 1
    elif matrix[0][0] == matrix[0][1] == matrix[1][1] == playerSign and matrix[1][0] == ' ':
        matrix[1][0] = computerSign
        return True, 1, 0
    elif matrix[0][0] == matrix[1][1] == matrix[1][0] == playerSign and matrix[0][1] == ' ':
        matrix[0][1] = computerSign
        return True, 0, 1
    elif matrix[1][1] == matrix[0][1] == matrix[1][0] == playerSign and matrix[0][0] == ' ':
        matrix[0][0] = computerSign
        return True, 0, 0
    # second square
    elif matrix[0][1] == matrix[0][2] == matrix[1][1] == playerSign and matrix[1][2] == ' ':
        matrix[1][2] = computerSign
        return True, 1, 2
    elif matrix[0][1] == matrix[0][2] == matrix[1][2] == playerSign and matrix[1][1] == ' ':
        matrix[1][1] = computerSign
        return True, 1, 1
    elif matrix[0][1] == matrix[1][2] == matrix[1][1] == playerSign and matrix[0][2] == ' ':
        matrix[0][2] = computerSign
        return True, 0, 2
    elif matrix[0][2] == matrix[1][2] == matrix[1][1] == playerSign and matrix[0][1] == ' ':
        matrix[0][1] = computerSign
        return True, 0, 1
    # third square
    elif matrix[0][2] == matrix[0][3] == matrix[1][2] == playerSign and matrix[1][3] == ' ':
        matrix[1][3] = computerSign
        return True, 1, 3
    elif matrix[0][2] == matrix[0][3] == matrix[1][3] == playerSign and matrix[1][2] == ' ':
        matrix[1][2] = computerSign
        return True, 1, 2
    elif matrix[0][2] == matrix[1][2] == matrix[1][3] == playerSign and matrix[0][3] == ' ':
        matrix[0][3] = computerSign
        return True, 0, 3
    elif matrix[0][3] == matrix[1][2] == matrix[1][3] == playerSign and matrix[0][2] == ' ':
        matrix[0][2] = computerSign
        return True, 0, 2
    # fourth square
    elif matrix[1][0] == matrix[1][1] == matrix[2][0] == playerSign and matrix[2][1] == ' ':
        matrix[2][1] = computerSign
        return True, 2, 1
    elif matrix[1][0] == matrix[1][1] == matrix[2][1] == playerSign and matrix[2][0] == ' ':
        matrix[2][0] = computerSign
        return True, 2, 0
    elif matrix[1][0] == matrix[2][1] == matrix[2][0] == playerSign and matrix[1][1] == ' ':
        matrix[1][1] = computerSign
        return True, 1, 1
    elif matrix[2][1] == matrix[1][1] == matrix[2][0] == playerSign and matrix[1][0] == ' ':
        matrix[1][0] = computerSign
        return True, 1, 0
    # fifth square
    elif matrix[1][1] == matrix[1][2] == matrix[2][1] == playerSign and matrix[2][2] == ' ':
        matrix[2][2] = computerSign
        return True, 2, 2
    elif matrix[1][1] == matrix[1][2] == matrix[2][2] == playerSign and matrix[2][1] == ' ':
        matrix[2][1] = computerSign
        return True, 2, 1
    elif matrix[1][1] == matrix[2][2] == matrix[2][1] == playerSign and matrix[1][2] == ' ':
        matrix[1][2] = computerSign
        return True, 1, 2
    elif matrix[1][2] == matrix[2][2] == matrix[2][1] == playerSign and matrix[1][1] == ' ':
        matrix[1][1] = computerSign
        return True, 1, 1
    # sixth square
    elif matrix[1][2] == matrix[1][3] == matrix[2][2] == playerSign and matrix[2][3] == ' ':
        matrix[2][3] = computerSign
        return True, 2, 3
    elif matrix[1][2] == matrix[1][3] == matrix[2][3] == playerSign and matrix[2][2] == ' ':
        matrix[2][2] = computerSign
        return True, 2, 2
    elif matrix[1][2] == matrix[2][2] == matrix[2][3] == playerSign and matrix[1][3] == ' ':
        matrix[1][3] = computerSign
        return True, 1, 3
    elif matrix[1][3] == matrix[2][2] == matrix[2][3] == playerSign and matrix[1][2] == ' ':
        matrix[1][2] = computerSign
        return True, 1, 2
    # seventh square
    elif matrix[2][0] == matrix[2][1] == matrix[3][0] == playerSign and matrix[3][1] == ' ':
        matrix[3][1] = computerSign
        return True, 3, 1
    elif matrix[2][0] == matrix[2][1] == matrix[3][1] == playerSign and matrix[3][0] == ' ':
        matrix[3][0] = computerSign
        return True, 3, 0
    elif matrix[2][0] == matrix[3][1] == matrix[3][0] == playerSign and matrix[2][1] == ' ':
        matrix[2][1] = computerSign
        return True, 2, 1
    elif matrix[3][1] == matrix[2][1] == matrix[3][0] == playerSign and matrix[2][0] == ' ':
        matrix[2][0] = computerSign
        return True, 2, 0
    # eighth square
    elif matrix[2][1] == matrix[2][2] == matrix[3][1] == playerSign and matrix[3][2] == ' ':
        matrix[3][2] = computerSign
        return True, 3, 2
    elif matrix[2][1] == matrix[2][2] == matrix[3][2] == playerSign and matrix[3][1] == ' ':
        matrix[3][1] = computerSign
        return True, 3, 1
    elif matrix[2][1] == matrix[3][2] == matrix[3][1] == playerSign and matrix[2][2] == ' ':
        matrix[2][2] = computerSign
        return True, 2, 2
    elif matrix[2][2] == matrix[3][2] == matrix[3][1] == playerSign and matrix[2][1] == ' ':
        matrix[2][1] = computerSign
        return True, 2, 1
    # ninth square
    elif matrix[2][2] == matrix[2][3] == matrix[3][2] == playerSign and matrix[3][3] == ' ':
        matrix[3][3] = computerSign
        return True, 3, 3
    elif matrix[2][2] == matrix[2][3] == matrix[3][3] == playerSign and matrix[3][2] == ' ':
        matrix[3][2] = computerSign
        return True, 3, 2
    elif matrix[2][2] == matrix[3][2] == matrix[3][3] == playerSign and matrix[2][3] == ' ':
        matrix[2][3] = computerSign
        return True, 2, 3
    elif matrix[2][3] == matrix[3][2] == matrix[3][3] == playerSign and matrix[2][2] == ' ':
        matrix[2][2] = computerSign
        return True, 2, 2
    else:
        return False, 4, 4


matrix = blankMatrix()

# function of countdown, you can see it on the end of game at the window bootom :D
def countdown(secs):
    stime = secs
    while stime > 0:
        pygame.draw.rect(screen, (255, 200, 100), (0, 456, 500, 100))
        printText('This window will close in ' + str(stime) + ' seconds.', 250, 480, 20)
        pygame.display.update()
        time.sleep(1)
        stime -= 1
    pygame.quit()
    quit()

# function which prints who is the winner
def endOfGame(winner):
    if winner == playerSign:
        printText('Congratulations! You won!', 250, 440, 32)
    else:
        printText('You lost. More luck next time!', 250, 440, 32)
    pygame.draw.rect(screen, (255, 200, 100), (0, 0, 500, 100))
    pygame.display.update()
    countdown(5)

# function which checks if there is any winning combination in matrix, if is then returns 1
# also, checks if there is full matrix and there is no winning combination, so it return 2 and that means it is draw
def checkWin():
    # returns 1 if row is XXXX or OOOO
    if matrix[0][0] == matrix[0][1] == matrix[0][2] == matrix[0][3] != ' ':
        pygame.draw.line(screen, [255, 0, 0], (100, 137), (400, 137), 7)
        endOfGame(matrix[0][0])
        return 1
    elif matrix[1][0] == matrix[1][1] == matrix[1][2] == matrix[1][3] != ' ':
        pygame.draw.line(screen, [255, 0, 0], (100, 212), (400, 212), 7)
        endOfGame(matrix[1][0])
        return 1
    elif matrix[2][0] == matrix[2][1] == matrix[2][2] == matrix[2][3] != ' ':
        pygame.draw.line(screen, [255, 0, 0], (100, 287), (400, 287), 7)
        endOfGame(matrix[2][0])
        return 1
    elif matrix[3][0] == matrix[3][1] == matrix[3][2] == matrix[3][3] != ' ':
        pygame.draw.line(screen, [255, 0, 0], (100, 362), (400, 362), 7)
        endOfGame(matrix[3][0])
        return 1
    # returns 1 if column is XXXX or OOOO
    elif matrix[0][0] == matrix[1][0] == matrix[2][0] == matrix[3][0] != ' ':
        pygame.draw.line(screen, [255, 0, 0], (138, 100), (138, 400), 7)
        endOfGame(matrix[0][0])
        return 1
    elif matrix[0][1] == matrix[1][1] == matrix[2][1] == matrix[3][1] != ' ':
        pygame.draw.line(screen, [255, 0, 0], (213, 100), (213, 400), 7)
        endOfGame(matrix[0][1])
        return 1
    elif matrix[0][2] == matrix[1][2] == matrix[2][2] == matrix[3][2] != ' ':
        pygame.draw.line(screen, [255, 0, 0], (288, 100), (288, 400), 7)
        endOfGame(matrix[0][2])
        return 1
    elif matrix[0][3] == matrix[1][3] == matrix[2][3] == matrix[3][3] != ' ':
        pygame.draw.line(screen, [255, 0, 0], (363, 100), (363, 400), 7)
        endOfGame(matrix[0][3])
        return 1
    # returns 1 if diagonals are XXXX or OOOO
    elif matrix[0][0] == matrix[1][1] == matrix[2][2] == matrix[3][3] != ' ':
        pygame.draw.line(screen, [255, 0, 0], (100, 100), (400, 400), 7)
        endOfGame(matrix[0][0])
        return 1
    elif matrix[0][3] == matrix[1][2] == matrix[2][1] == matrix[3][0] != ' ':
        pygame.draw.line(screen, [255, 0, 0], (400, 100), (100, 400), 7)
        endOfGame(matrix[0][3])
        return 1
    # returns 1 if there is a square of Xs or Os
    elif matrix[0][0] == matrix[0][1] == matrix[1][0] == matrix[1][1] != ' ':
        pygame.draw.rect(screen, [255, 0, 0], (137, 137, 77, 77), 7, 1, 1)
        endOfGame(matrix[0][0])
        return 1
    elif matrix[0][1] == matrix[0][2] == matrix[1][1] == matrix[1][2] != ' ':
        pygame.draw.rect(screen, [255, 0, 0], (212, 137, 77, 77), 7, 1, 1)
        endOfGame(matrix[0][1])
        return 1
    elif matrix[0][2] == matrix[0][3] == matrix[1][2] == matrix[1][3] != ' ':
        pygame.draw.rect(screen, [255, 0, 0], (287, 137, 77, 77), 7, 1, 1)
        endOfGame(matrix[0][2])
        return 1
    elif matrix[1][0] == matrix[1][1] == matrix[2][0] == matrix[2][1] != ' ':
        pygame.draw.rect(screen, [255, 0, 0], (137, 212, 77, 77), 7, 1, 1)
        endOfGame(matrix[1][0])
        return 1
    elif matrix[1][1] == matrix[1][2] == matrix[2][1] == matrix[2][2] != ' ':
        pygame.draw.rect(screen, [255, 0, 0], (212, 212, 77, 77), 7, 1, 1)
        endOfGame(matrix[1][1])
        return 1
    elif matrix[1][2] == matrix[1][3] == matrix[2][2] == matrix[2][3] != ' ':
        pygame.draw.rect(screen, [255, 0, 0], (287, 212, 77, 77), 7, 1, 1)
        endOfGame(matrix[1][2])
        return 1
    elif matrix[2][0] == matrix[2][1] == matrix[3][0] == matrix[3][1] != ' ':
        pygame.draw.rect(screen, [255, 0, 0], (137, 287, 77, 77), 7, 1, 1)
        endOfGame(matrix[2][0])
        return 1
    elif matrix[2][1] == matrix[2][2] == matrix[3][1] == matrix[3][2] != ' ':
        pygame.draw.rect(screen, [255, 0, 0], (212, 287, 77, 77), 7, 1, 1)
        endOfGame(matrix[2][1])
        return 1
    elif matrix[2][2] == matrix[2][3] == matrix[3][2] == matrix[3][3] != ' ':
        pygame.draw.rect(screen, [255, 0, 0], (287, 287, 77, 77), 7, 1, 1)
        endOfGame(matrix[2][2])
        return 1
    elif ' ' not in matrix[0] and ' ' not in matrix[1] and ' ' not in matrix[2] and ' ' not in matrix[3]:
        printText('Draw!', 250, 440, 32)
        pygame.draw.rect(screen, (255, 200, 100), (0, 0, 500, 100))
        printText('Thanks for playing!', 250, 40, 35)
        countdown(5)
        return 2

# main function
def main():
    running = True
    bg = pygame.image.load('images/table.png')
    bg = pygame.transform.scale(bg, (300, 300))
    screen.fill([255, 200, 100])
    screen.blit(bg, (100, 100))
    pygame.display.flip()

    # randomly chooses who plays first
    beginning = random.randint(0, 1)
    if beginning == 1:
        printText('Computer plays first.', 250, 40, 35)
        pygame.display.update()
        time.sleep(1)
        computerTurn()
    else:
        printText('You play first.', 250, 40, 35)
        pygame.display.update()
        pass

    while running:
        evs = pygame.event.get()
        for ev in evs:
            if ev.type == pygame.QUIT:
                pygame.quit()
                quit()
            if ev.type == MOUSEBUTTONUP:         # on every click it will check if it was clicked on part of game table
                xpos, ypos = pygame.mouse.get_pos()
                if 100 < xpos < 175:
                    if 100 < ypos < 175:
                        if matrix[0][0] == ' ':
                            matrix[0][0] = playerSign
                            if playerSign == 'x':
                                printText('X', 138, 142, 60)
                            else:
                                printText('O', 138, 142, 60)
                            pygame.display.update()
                            if checkWin() == 1:
                                running = False
                            else:
                                computerTurn()
                            if checkWin() == 1:
                                running = False
                    elif 175 < ypos < 250:
                        if matrix[1][0] == ' ':
                            matrix[1][0] = playerSign
                            if playerSign == 'x':
                                printText('X', 138, 217, 60)
                            else:
                                printText('O', 138, 217, 60)
                            pygame.display.update()
                            if checkWin() == 1:
                                running = False
                            else:
                                computerTurn()
                                pygame.draw.rect(bg, (255, 200, 100), (0, 0, 500, 100))
                            if checkWin() == 1:
                                running = False
                    elif 250 < ypos < 325:
                        if matrix[2][0] == ' ':
                            matrix[2][0] = playerSign
                            if playerSign == 'x':
                                printText('X', 138, 292, 60)
                            else:
                                printText('O', 138, 292, 60)
                            pygame.display.update()
                            if checkWin() == 1:
                                running = False
                            else:
                                computerTurn()
                                pygame.draw.rect(bg, (255, 200, 100), (0, 0, 500, 100))
                            if checkWin() == 1:
                                running = False
                    elif 325 < ypos < 400:
                        if matrix[3][0] == ' ':
                            matrix[3][0] = playerSign
                            if playerSign == 'x':
                                printText('X', 138, 367, 60)
                            else:
                                printText('O', 138, 367, 60)
                            pygame.display.update()
                            if checkWin() == 1:
                                running = False
                            else:
                                computerTurn()
                                pygame.draw.rect(bg, (255, 200, 100), (0, 0, 500, 100))
                            if checkWin() == 1:
                                running = False
                elif 175 < xpos < 250:
                    if 100 < ypos < 175:
                        if matrix[0][1] == ' ':
                            matrix[0][1] = playerSign
                            if playerSign == 'x':
                                printText('X', 213, 142, 60)
                            else:
                                printText('O', 213, 142, 60)
                            pygame.display.update()
                            if checkWin() == 1:
                                running = False
                            else:
                                computerTurn()
                                pygame.draw.rect(bg, (255, 200, 100), (0, 0, 500, 100))
                            if checkWin() == 1:
                                running = False
                    elif 175 < ypos < 250:
                        if matrix[1][1] == ' ':
                            matrix[1][1] = playerSign
                            if playerSign == 'x':
                                printText('X', 213, 217, 60)
                            else:
                                printText('O', 213, 217, 60)
                            pygame.display.update()
                            if checkWin() == 1:
                                running = False
                            else:
                                computerTurn()
                            if checkWin() == 1:
                                running = False
                    elif 250 < ypos < 325:
                        if matrix[2][1] == ' ':
                            matrix[2][1] = playerSign
                            if playerSign == 'x':
                                printText('X', 213, 292, 60)
                            else:
                                printText('O', 213, 292, 60)
                            pygame.display.update()
                            if checkWin() == 1:
                                running = False
                            else:
                                computerTurn()
                            if checkWin() == 1:
                                running = False
                    elif 325 < ypos < 400:
                        if matrix[3][1] == ' ':
                            matrix[3][1] = playerSign
                            if playerSign == 'x':
                                printText('X', 213, 367, 60)
                            else:
                                printText('O', 213, 367, 60)
                            pygame.display.update()
                            if checkWin() == 1:
                                running = False
                            else:
                                computerTurn()
                            if checkWin() == 1:
                                running = False
                elif 250 < xpos < 325:
                    if 100 < ypos < 175:
                        if matrix[0][2] == ' ':
                            matrix[0][2] = playerSign
                            if playerSign == 'x':
                                printText('X', 288, 142, 60)
                            else:
                                printText('O', 288, 142, 60)
                            pygame.display.update()
                            if checkWin() == 1:
                                running = False
                            else:
                                computerTurn()
                            if checkWin() == 1:
                                running = False
                    elif 175 < ypos < 250:
                        if matrix[1][2] == ' ':
                            matrix[1][2] = playerSign
                            if playerSign == 'x':
                                printText('X', 288, 217, 60)
                            else:
                                printText('O', 288, 217, 60)
                            pygame.display.update()
                            if checkWin() == 1:
                                running = False
                            else:
                                computerTurn()
                            if checkWin() == 1:
                                running = False
                    elif 250 < ypos < 325:
                        if matrix[2][2] == ' ':
                            matrix[2][2] = playerSign
                            if playerSign == 'x':
                                printText('X', 288, 292, 60)
                            else:
                                printText('O', 288, 292, 60)
                            pygame.display.update()
                            if checkWin() == 1:
                                running = False
                            else:
                                computerTurn()
                            if checkWin() == 1:
                                running = False
                    elif 325 < ypos < 400:
                        if matrix[3][2] == ' ':
                            matrix[3][2] = playerSign
                            if playerSign == 'x':
                                printText('X', 288, 367, 60)
                            else:
                                printText('O', 288, 367, 60)
                            pygame.display.update()
                            if checkWin() == 1:
                                running = False
                            else:
                                computerTurn()
                            if checkWin() == 1:
                                running = False
                elif 325 < xpos < 400:
                    if 100 < ypos < 175:
                        if matrix[0][3] == ' ':
                            matrix[0][3] = playerSign
                            if playerSign == 'x':
                                printText('X', 363, 142, 60)
                            else:
                                printText('O', 363, 142, 60)
                            pygame.display.update()
                            if checkWin() == 1:
                                running = False
                            else:
                                computerTurn()
                            if checkWin() == 1:
                                running = False
                    elif 175 < ypos < 250:
                        if matrix[1][3] == ' ':
                            matrix[1][3] = playerSign
                            if playerSign == 'x':
                                printText('X', 363, 217, 60)
                            else:
                                printText('O', 363, 217, 60)
                            pygame.display.update()
                            if checkWin() == 1:
                                running = False
                            else:
                                computerTurn()
                            if checkWin() == 1:
                                running = False
                    elif 250 < ypos < 325:
                        if matrix[2][3] == ' ':
                            matrix[2][3] = playerSign
                            if playerSign == 'x':
                                printText('X', 363, 292, 60)
                            else:
                                printText('O', 363, 292, 60)
                            pygame.display.update()
                            if checkWin() == 1:
                                running = False
                            else:
                                computerTurn()
                            if checkWin() == 1:
                                running = False
                    elif 325 < ypos < 400:
                        if matrix[3][3] == ' ':
                            matrix[3][3] = playerSign
                            if playerSign == 'x':
                                printText('X', 363, 367, 60)
                            else:
                                printText('O', 363, 367, 60)
                            pygame.display.update()
                            if checkWin() == 1:
                                running = False
                            else:
                                computerTurn()
                            if checkWin() == 1:
                                running = False


main()
