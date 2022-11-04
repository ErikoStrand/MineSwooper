import pygame
import sys
import numpy as np
import time
pygame.init()
pygame.font.init()

infoObject = pygame.display.Info()
pygame.event.set_allowed([pygame.MOUSEBUTTONDOWN])
WIDTH, HEIGHT = 900, 900 + 100
# has to be perfectly devisibitly
BOARD_SQUARES = 9
BOMBS = 7
SQUARE_SIZE = int(WIDTH/BOARD_SQUARES)

display = pygame.display.set_mode((WIDTH, HEIGHT))
BACKGROUND = (40, 40, 40)
OUTLINE = (60, 60, 70)
clock = pygame.time.Clock()
TILES = []
DEAD = False
flag = pygame.image.load("flag.png")
flag = pygame.transform.scale(flag, (WIDTH/BOARD_SQUARES, WIDTH/BOARD_SQUARES))
RESTART = pygame.Rect(WIDTH/2 - 100, HEIGHT - 85, 200, 70)  

def drawText(text, font_size, x, y, color):
    font = pygame.font.Font("8-bit-hud.ttf", font_size)
    a, b = pygame.font.Font.size(font, str(text))
    draw = font.render(str(text), False, color)
    display.blit(draw, (x - a/2, y - b/2))
    
def drawTime(text, font_size, x, y, color):
    font = pygame.font.Font("8-bit-hud.ttf", font_size)
    a, b = pygame.font.Font.size(font, str(text))
    draw = font.render(str(text), False, color)
    display.blit(draw, (x, y - b/2))    
class Board:
    def __init__(self, rect, display, color, outline, x, y, bomb, shown):
        self.x = x
        self.y = y
        self.bomb: bool = bomb
        self.shown: bool = shown
        self.rect: pygame.Rect = rect
        self.display = display
        self.color: tuple = color
        self.outline: tuple = outline
        self.bombAmount: int = 0
        self.flag: bool = False
        
    def drawTile(self):
        if self.shown:
            self.color =  (30, 30, 30)
        pygame.draw.rect(self.display, self.color, self.rect)
        pygame.draw.rect(self.display, self.outline, self.rect, 2)        

def createClasses():
    startClass = time.time()
    for x in range(BOARD_SQUARES):
        for y in range(BOARD_SQUARES):
            TILES.append(Board(pygame.Rect(x * SQUARE_SIZE, y * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), display, BACKGROUND, OUTLINE, x, y, False, False))
    print("Created Classes In:", str(time.time()-startClass) + "s")
    
def createBombs(bombs):
    startBomb = time.time()
    for _ in range(bombs):
        x = np.random.randint(0, BOARD_SQUARES)
        y = np.random.randint(0, BOARD_SQUARES)
        for tile in TILES:    
            if tile.y == y and tile.x == x:
                tile.bomb = True   
    print("Bombs Placed In:", str(time.time()-startBomb) + "s")    
    
def checkBombAroundTile(x, y):
    amount = 0
    topX = x - 1
    topY = y - 1
    for tile in TILES:
        for x in range(3):
            for y in range(3):   
                if tile.x == topX + x and tile.y == topY + y:
                    if tile.bomb == True:
                        amount += 1
    return amount

def checkSafeAroundTile(x, y):
    for tile in TILES:
        if tile.x == x and tile.y == y:
            if tile.bomb: return
            elif tile.shown: return
            elif tile.bombAmount > 0: 
                tile.shown = True 
                return
            elif not tile.bomb:
                tile.shown = True 
                checkSafeAroundTile(x + 1, y)
                checkSafeAroundTile(x - 1, y)
                checkSafeAroundTile(x, y + 1)
                checkSafeAroundTile(x, y - 1)

    
                        
def createBombAmount():
    startBombAmount = time.time()
    for x in range(BOARD_SQUARES):
        for y in range(BOARD_SQUARES):
            amount = checkBombAroundTile(x, y)
            for tile in TILES:
                if tile.x == x and tile.y == y:
                    tile.bombAmount += amount
    print("Checked Bomb Amount In:", str(time.time()-startBombAmount) + "s")       
    
createClasses()
createBombs(BOMBS)
createBombAmount()
gameStart = time.time()
while 1:
    dt = clock.tick(240)
    start = time.time()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and DEAD:
                x, y = pygame.mouse.get_pos()
                if RESTART.collidepoint(x, y):
                    TILES = []
                    createClasses()
                    createBombs(BOMBS)
                    createBombAmount()
                    gameStart = time.time()
                    DEAD = False
                    
            if event.button == 1 and not DEAD:
                x, y = pygame.mouse.get_pos()
                x = int(x/SQUARE_SIZE)
                y = int(y/SQUARE_SIZE)
                for tile in TILES:
                    if tile.x == x and tile.y == y:
                        if tile.bomb:
                            DEAD = True
                            tile.shown = True
                            
                        if not tile.bomb:
                            checkSafeAroundTile(x, y)
                            tile.shown = True    
            if event.button == 3:
                x, y = pygame.mouse.get_pos()
                x = int(x/SQUARE_SIZE)
                y = int(y/SQUARE_SIZE)
                for tile in TILES:
                    if tile.x == x and tile.y == y:
                        tile.flag = not tile.flag
                        print("hey")
                            
    display.fill((BACKGROUND))
    for tile in TILES:
        tile.drawTile()
        if tile.shown:
            tile.flag = False
        if tile.shown and tile.bombAmount > 0:
            drawText(tile.bombAmount, int(30/(BOARD_SQUARES/9)), (tile.x * SQUARE_SIZE + SQUARE_SIZE/2), (tile.y * SQUARE_SIZE + SQUARE_SIZE/2), (255, 255, 255))   
        if tile.flag:
            display.blit(flag, (tile.x * SQUARE_SIZE, tile.y * SQUARE_SIZE)) 
        if tile.bomb and tile.shown:
            pygame.draw.circle(display, (0, 0, 0), (tile.x * SQUARE_SIZE + SQUARE_SIZE/2, tile.y * SQUARE_SIZE + SQUARE_SIZE/2), SQUARE_SIZE/3)   
                          
    drawTime(int(time.time()-gameStart), 40, 30, HEIGHT - 50, (255, 255, 255))
    
    if DEAD:
        pygame.draw.rect(display, OUTLINE, RESTART)
        drawText("Try Again?", 15, RESTART.x + 100, RESTART.y + 35, (255, 255, 255))
    pygame.display.flip()
    stop = time.time()        
    #print(stop-start)