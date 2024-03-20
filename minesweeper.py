import random
import pygame

SCREEN_HEIGHT = 600
SCREEN_WIDTH = 900

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (180, 180, 180)

BORDER_COLOR = (170, 170, 170)
NOT_PRESSED_COLOR = (210, 210, 210)
BACKGROUND_COLOR = (150,150,150)

# Variables that effect difficulty of the game
HEIGHT = 16
WIDTH = 30
BOMBS = 99

GAMEPLAY_SCREEN_HEIGHT = HEIGHT * 24
GAMEPLAY_SCREEN_WIDTH = WIDTH * 24
# GAMEPLAY_SCREEN_HEIGHT = SCREEN_HEIGHT
# GAMEPLAY_SCREEN_WIDTH = SCREEN_WIDTH

TILE_HEIGHT = GAMEPLAY_SCREEN_HEIGHT // HEIGHT
TILE_WIDTH = GAMEPLAY_SCREEN_WIDTH // WIDTH

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

number_font = pygame.font.SysFont(None, 20)

class Tile():
    def __init__(self, x, y, width, height, isbomb:bool, adjacent):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.isbomb = isbomb
        self.pressed = False
        if not self.isbomb:
            self.adjacent = adjacent
            self.num_image = number_font.render(str(self.adjacent), True, WHITE, BACKGROUND_COLOR)
        self.rect = pygame.Rect(x, y, width, height)
        
# class for the game itself
class MineSweeper():
    def __init__(self):
        self.height = HEIGHT
        self.width = WIDTH
        self.bombs = BOMBS
        self.board = [[Tile(0,0,0,0,False,0) for _ in range(self.height)] for _ in range(self.width)]
        self.y_multiplier = GAMEPLAY_SCREEN_HEIGHT // self.height
        self.x_multiplier = GAMEPLAY_SCREEN_WIDTH // self.width
        self.bomb_coordinates = set()
        
    # function to place the bombs on the board
    def populate_board(self):
        self.generate_bomb_coordinates()
        for coordinate in self.bomb_coordinates:
            self.board[coordinate[0]][coordinate[1]] = Tile(coordinate[0] * self.x_multiplier, coordinate[1] * self.y_multiplier, TILE_WIDTH, TILE_HEIGHT, True, 0)
    
    def generate_bomb_coordinates(self):
        while len(self.bomb_coordinates) != self.bombs:
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            self.bomb_coordinates.add((x, y))
        
    # function to numerate tiles
    def check_adjacent(self):
        for x in range(self.width):
            for y in range(self.height):
                if self.board[x][y].isbomb:
                    continue
                num_adjacent_bombs = 0
                
                if self.is_valid_pos(x - 1, y - 1):
                    if self.board[x - 1][y - 1].isbomb:
                        num_adjacent_bombs += 1
                        
                if self.is_valid_pos(x - 1, y):
                    if self.board[x - 1][y].isbomb:
                        num_adjacent_bombs += 1
                
                if self.is_valid_pos(x - 1, y + 1):
                    if self.board[x - 1][y + 1].isbomb:
                        num_adjacent_bombs += 1
                        
                if self.is_valid_pos(x, y - 1):
                    if self.board[x][y - 1].isbomb:
                        num_adjacent_bombs += 1
                        
                if self.is_valid_pos(x, y + 1):
                    if self.board[x][y + 1].isbomb:
                        num_adjacent_bombs += 1
                        
                if self.is_valid_pos(x + 1, y - 1):
                    if self.board[x + 1][y - 1].isbomb:
                        num_adjacent_bombs += 1
                        
                if self.is_valid_pos(x + 1, y):
                    if self.board[x + 1][y].isbomb:
                        num_adjacent_bombs += 1
                        
                if self.is_valid_pos(x + 1, y + 1):
                    if self.board[x + 1][y + 1].isbomb:
                        num_adjacent_bombs += 1
                
                self.board[x][y] = Tile(x * self.x_multiplier, y * self.y_multiplier, TILE_WIDTH, TILE_HEIGHT, False, num_adjacent_bombs)
                
    def is_valid_pos(self, x, y):
        if x < 0 or y < 0 or x > self.width - 1 or y > self.height - 1:
            return 0
        return 1

    def draw_board(self):
        for x in range(self.width):
            for y in range(self.height):
                tile = self.board[x][y]
                if not tile.pressed:
                    pygame.draw.rect(screen, (NOT_PRESSED_COLOR), tile.rect)
                    pygame.draw.rect(screen, (BORDER_COLOR), tile.rect, 1)
                else:
                    pygame.draw.rect(screen, BORDER_COLOR, tile.rect, 1)
                    if not tile.isbomb:
                        screen.blit(tile.num_image, (tile.x, tile.y))
                        
    def tile_click(self, m_coordinates):
        x_m, y_m = m_coordinates
        for x in range(self.width):
            for y in range(self.height):
                tile = self.board[x][y]
                if tile.rect.collidepoint(x_m, y_m):
                    tile.pressed = True 
                    return
           
if __name__ == "__main__":
    # set up board
    game = MineSweeper()
    game.populate_board()
    game.check_adjacent()

    #game loop
    while True:
        events = pygame.event.get()
        for event in events:
            
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            
            # keyboard presses
            if event.type == pygame.KEYDOWN:
                pass
            if event.type == pygame.MOUSEBUTTONDOWN:
                game.tile_click(pygame.mouse.get_pos())
                
                # BACKGROUND_COLOR = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                
        
        screen.fill(BACKGROUND_COLOR)
        
        game.draw_board()
        
        pygame.display.update()
        