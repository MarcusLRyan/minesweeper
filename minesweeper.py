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

TILE_HEIGHT = GAMEPLAY_SCREEN_HEIGHT // HEIGHT
TILE_WIDTH = GAMEPLAY_SCREEN_WIDTH // WIDTH



pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

number_font = pygame.font.SysFont(None, 20)

flag_image = pygame.image.load("flag.png").convert_alpha()
bomb_image = pygame.image.load("bomb.png").convert_alpha()

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
        else:
            self.bomb_image = bomb_image
        self.rect = pygame.Rect(x, y, width, height)
        self.placeholder = False
        
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
                    if not tile.placeholder:
                        pygame.draw.rect(screen, (NOT_PRESSED_COLOR), tile.rect)
                    else:
                        screen.blit(flag_image, (tile.x, tile.y))
                else:
                    if not tile.isbomb:
                        screen.blit(tile.num_image, (tile.x, tile.y))
                    else:
                        screen.blit(tile.bomb_image, (tile.x, tile.y))
                        
                pygame.draw.rect(screen, BORDER_COLOR, tile.rect, 1)
                        
    def tile_click(self, m_coordinates:tuple):
        # maybe expand this to spread out to
        # all adjacent tiles that dont border bombs
        # should use a searching algorithm
        x_m, y_m = m_coordinates
        for x in range(self.width):
            for y in range(self.height):
                tile = self.board[x][y]
                if tile.rect.collidepoint(x_m, y_m):
                    tile.pressed = True
                    # or call self.expand() here
                    if not tile.isbomb and tile.adjacent == 0:
                        self.expand(x, y)
                    return
    
    def expand(self, x, y):
        # return
        queue = [(x, y)]
        visited = set()
        while len(queue) > 0:
            x, y = queue.pop(0)
            visited.add((x, y))
            self.board[x][y].pressed = True
            
            for x, y in self.neighbours(x, y):
                if (x, y) not in visited and not self.board[x][y].isbomb and self.board[x][y].adjacent == 0:
                    queue.append((x, y))
                else:
                    self.board[x][y].pressed = True
    
    def neighbours(self, x, y):
        indices = [
            (x - 1, y - 1),
            (x - 1, y),
            (x - 1, y + 1),
            (x, y - 1),
            (x, y + 1),
            (x + 1, y - 1),
            (x + 1, y),
            (x + 1, y + 1)
            ]
        return [(x, y) for x, y in indices if self.is_valid_pos(x, y)]
    
    def bomb_filler(self, m_coordinates:tuple):
        x_m, y_m = m_coordinates
        for x in range(self.width):
            for y in range(self.height):
                tile = self.board[x][y]
                if tile.rect.collidepoint(x_m, y_m):
                    tile.placeholder = True
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
                
                keys = pygame.key.get_pressed()
                if keys[pygame.K_LCTRL]:
                    if event.button == 1:
                        # place bomb
                        game.bomb_filler(pygame.mouse.get_pos())
                        pass
                else:
                    game.tile_click(pygame.mouse.get_pos())                
        
        screen.fill(BACKGROUND_COLOR)
        
        game.draw_board()
        
        pygame.display.update()
        