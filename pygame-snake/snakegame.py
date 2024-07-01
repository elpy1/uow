#!/usr/bin/env python
from random import choice
import pygame as pg

# Constants for colours and fonts
COLOURS = {
    'black': (0, 0, 0),
    'blue': (5, 158, 212),
    'lightgrey': (240, 247, 255),
    'grey': (193, 194, 196),
    'orange': (255, 179, 0),
    'red': (255, 102, 106),
    'green': (62, 207, 149),
    'pink': (207, 62, 120),
}

FONTS = {
    'game_over': ('arial', 72),
    'score': ('arial', 18)
}

class Game:
    def __init__(self, width=600, height=600, cell_size=30):
        # set display values
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.screen = None

        # set game window caption
        self.caption = 'Snake Game'
        # set game difficulty
        self.difficulty = 'easy'
        # map difficulty to wait time (ms)
        self.speed = {'easy': 72, 'medium': 60, 'hard': 48, 'comp801': 36}
        # set boundaries to on by default
        self.boundaries = True
        # game score (number of times food is eaten)
        self.score = 0

    def initialise(self):
        """Check if settings are valid, initialise pygame and create screen"""
        if self.width != self.height:
            raise ValueError('Width and height must be equal.')
        if self.width % self.cell_size != 0 or self.height % self.cell_size != 0:
            raise ValueError('Width and height must be evenly divisible by cell_size.')
        if self.difficulty not in self.speed:
            raise ValueError(f'Difficulty must be one of {list(self.speed.keys())}.')

        pg.init()
        pg.display.set_caption(self.caption)
        pg.time.Clock().tick(60)
        pg.mouse.set_visible(False)
        self.screen = pg.display.set_mode((self.width, self.height))

    def get_user_input(self, turn):
        """Check user key press event and return direction or end game"""
        pg.event.pump()
        keys = pg.key.get_pressed()
        if keys[pg.K_ESCAPE]:
            self.game_over()
        elif keys[pg.K_LEFT] or keys[ord('a')]:
            return (-1, 0)
        elif keys[pg.K_RIGHT] or keys[ord('d')]:
            return (1, 0)
        elif keys[pg.K_UP] or keys[ord('w')]:
            return (0, -1)
        elif keys[pg.K_DOWN] or keys[ord('s')]:
            return (0, 1)
        return turn

    def draw_grid(self, bg_colour, grid_colour):
        """Draw the game board grid"""
        self.screen.fill(bg_colour)
        for x in range(0, self.width, self.cell_size):
            pg.draw.line(self.screen, grid_colour, (0, x), (self.width, x), 1)
            pg.draw.line(self.screen, grid_colour, (x, 0), (x, self.height), 1)

    def draw_score(self, colour, font):
        """Draw game score"""
        f = pg.font.SysFont(*font)
        s = f.render(f'Score: {self.score}', True, colour)
        self.screen.blit(s, (self.cell_size // 10, self.cell_size // 10))

    def update_screen(self):
        """Update whole display and control game speed"""
        pg.display.update()
        pg.time.delay(self.speed[self.difficulty])

    def game_over(self, colour=COLOURS['red'], font=FONTS['game_over']):
        """Draw game over text and end the game"""
        f = pg.font.SysFont(*font)
        g = f.render('GAME OVER', True, colour)
        g_rect = g.get_rect(center=(self.width // 2, self.cell_size * 2))
        self.screen.blit(g, g_rect)
        pg.display.update()
        pg.time.wait(2000)
        pg.quit()
        raise SystemExit(0)


class Snake:
    def __init__(self, game):
        self.game = game
        self.colour = COLOURS['green']
        self.length = 1
        self.body = [[self.game.width // 2, self.game.height // 2]]
        self.direction = choice([(-1, 0), (1, 0), (0, -1), (0, 1)])

    def get_head_pos(self):
        """Return (x, y) for snake head position"""
        return self.body[0]

    def eat(self, food_pos):
        """Check if snake ate food"""
        return self.get_head_pos() == food_pos

    def grow(self):
        """Grow snake size by incrementing snake length"""
        self.length += 1

    def turn(self, direction):
        """Check for valid turn direction and update direction"""
        opposite = tuple(-d for d in direction)
        if self.length > 1 and self.direction == opposite:
            return
        self.direction = direction

    def move(self):
        """Move the snake by updating the snake body"""
        head = self.get_head_pos()
        x = self.game.cell_size * self.direction[0] + head[0]
        y = self.game.cell_size * self.direction[1] + head[1]
        new = (x, y) if self.game.boundaries else (x % self.game.width, y % self.game.height)
        self.body.insert(0, new)
        if len(self.body) > self.length:
            self.body.pop()

    def draw(self):
        """Draw the snake"""
        for b in self.body:
            r = pg.Rect(b, (self.game.cell_size, self.game.cell_size))
            pg.draw.rect(self.game.screen, self.colour, r)

    def is_collision(self):
        """Check for snake collisions with screen boundaries or self"""
        h = self.get_head_pos()
        return ((h[0] >= self.game.width or h[0] < 0) or
                (h[1] >= self.game.height or h[1] < 0) or
                h in self.body[2:])


class Food:
    def __init__(self, game, snake):
        self.game = game
        self.snake = snake
        self.colour = COLOURS['pink']
        self.position = None
        self.new_position()

    def new_position(self):
        """Set a random food position and ensure it is not in the same position as the snake body"""
        rows = self.game.height // self.game.cell_size
        cols = self.game.width // self.game.cell_size
        while True:
            new_pos = (choice(range(1, cols)) * self.game.cell_size,
                       choice(range(1, rows)) * self.game.cell_size)
            if new_pos not in self.snake.body:
                break
        self.position = new_pos

    def draw(self):
        """Draw snake food"""
        r = pg.Rect(self.position, (self.game.cell_size, self.game.cell_size))
        pg.draw.rect(self.game.screen, self.colour, r)


def main():
    game = Game(width=800, height=800, cell_size=40)
    snake = Snake(game)
    food = Food(game, snake)

    # game configuration examples
    game.caption = 'Snake Game'
    game.difficulty = 'medium'
    game.boundaries = False
    snake.length = 2
    snake.colour = COLOURS['blue']
    food.colour = COLOURS['orange']

    try:
        game.initialise()
    except Exception as e:
        raise SystemExit(f'Game initialisation failed with: {e}') from e

    print('Game initialised!')

    # game loop
    while True:
        game.draw_grid(COLOURS['lightgrey'], COLOURS['grey'])
        snake.draw()
        food.draw()
        game.draw_score(COLOURS['black'], FONTS['score'])
        snake.turn(game.get_user_input(snake.direction))
        snake.move()
        if snake.is_collision():
            game.game_over(COLOURS['red'], FONTS['game_over'])
        if snake.eat(food.position):
            snake.grow()
            game.score += 1
            food.new_position()
        game.update_screen()


if __name__ == '__main__':
    main()
