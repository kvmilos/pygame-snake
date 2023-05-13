import pygame
from pygame.locals import *
import time
import random

TIME = .15
TILE_SIZE = 20
SCREEN_X = 1200
SCREEN_Y = 800
GAME_X = 800
GAME_Y = 600
SCREEN_COLOUR = 'lightblue'
GAME_COLOUR = (102, 255, 178)
GAME_SCREEN = pygame.Rect((SCREEN_X - GAME_X) /2, (SCREEN_Y - GAME_Y) /2, GAME_X, GAME_Y)

class Apple:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.image = pygame.image.load("sprites/apple.png").convert()
        self.x = (SCREEN_X - GAME_X)/2 + random.randint(0,GAME_X//TILE_SIZE-1)*TILE_SIZE
        self.y = (SCREEN_Y - GAME_Y)/2 + random.randint(0,GAME_Y//TILE_SIZE-1)*TILE_SIZE

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))

    def generate(self):
        self.x = (SCREEN_X - GAME_X)/2 + random.randint(0,GAME_X//TILE_SIZE-1)*TILE_SIZE
        self.y = (SCREEN_Y - GAME_Y)/2 + random.randint(0,GAME_Y//TILE_SIZE-1)*TILE_SIZE

class Snake:
    def __init__(self, parent_screen, length):
        self.length = length
        self.parent_screen = parent_screen
        self.part = pygame.image.load("sprites/snake.png").convert()
        self.head_up = pygame.image.load("sprites/snakeU.png").convert()
        self.head_down = pygame.image.load("sprites/snakeD.png").convert()
        self.head_right = pygame.image.load("sprites/snakeR.png").convert()
        self.head_left = pygame.image.load("sprites/snakeL.png").convert()
        self.x = [(SCREEN_X - GAME_X)/2 + random.randint(0,GAME_X//TILE_SIZE-1)*TILE_SIZE]*length
        self.y = [((SCREEN_Y - GAME_Y)/2 + random.randint(0,GAME_Y//(2*TILE_SIZE))*TILE_SIZE)]*length
        self.direction = 'down'

    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)
    
    def draw(self):
        head_images = {
        'up': self.head_up,
        'down': self.head_down,
        'right': self.head_right,
        'left': self.head_left
    }
        self.parent_screen.fill(SCREEN_COLOUR)
        pygame.draw.rect(self.parent_screen, GAME_COLOUR, GAME_SCREEN)
        head_image = head_images[self.direction]
        self.parent_screen.blit(head_image, (self.x[0], self.y[0]))
        for i in range(1, self.length):
            self.parent_screen.blit(self.part, (self.x[i], self.y[i]))

    def move_left(self):
        self.direction = 'left'

    def move_right(self):
        self.direction = 'right'

    def move_up(self):
        self.direction = 'up'

    def move_down(self):
        self.direction = 'down'

    def remove_tail(self, x, y):
        pygame.draw.rect(self.parent_screen, GAME_COLOUR, (x, y, TILE_SIZE, TILE_SIZE))

    def walk(self):
        del_x, del_y = self.x[self.length-1], self.y[self.length-1]

        for i in range(self.length-1, 0, -1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]
        
        if self.direction == 'down':
            self.y[0] += TILE_SIZE
        elif self.direction == 'up':
            self.y[0] -= TILE_SIZE
        elif self.direction == 'left':
            self.x[0] -= TILE_SIZE
        elif self.direction == 'right':
            self.x[0] += TILE_SIZE
        
        self.remove_tail(del_x, del_y)
        self.draw()


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Gra Snake")

        pygame.mixer.init()
        self.play_background_music()

        self.screen = pygame.display.set_mode((SCREEN_X, SCREEN_Y))
        self.screen.fill(SCREEN_COLOUR)
        pygame.draw.rect(self.screen, GAME_COLOUR, GAME_SCREEN)

        self.snake = Snake(self.screen, 1)
        self.snake.draw()
        self.apple = Apple(self.screen)
        self.apple.draw()
    
    def is_collision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2+TILE_SIZE:
            if y1 >= y2 and y1 <y2+TILE_SIZE:
                return True
            
        return False
    
    def play_background_music(self):
        pygame.mixer.music.load("sounds/background.mp3")
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(-1, 0)


    def play_sound(self, sound):
        sound = pygame.mixer.Sound(f"sounds/{sound}")
        pygame.mixer.Sound.play(sound)

    def play(self):
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()

        # snake eating apple
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            self.play_sound('bite.mp3')
            self.snake.increase_length()
            self.apple.generate()
        
        # snake colliding with itself
        for i in range(1, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                self.play_sound('lose.wav')
                raise "Game over"
            
        # snake going outside of the screen
        if not ((SCREEN_X - GAME_X)/2 <= self.snake.x[0] < SCREEN_X - (SCREEN_X - GAME_X)/2 and (SCREEN_Y - GAME_Y)/2 < self.snake.y[0] <= SCREEN_Y - (SCREEN_Y - GAME_Y)/2):
            self.play_sound('lose.wav')
            raise "Hit the boundary"
            
    def show_game_over(self):
        self.screen.fill(SCREEN_COLOUR)
        font = pygame.font.SysFont('arial', 30)
        line1 = font.render(f"Game is over! Your score is {self.snake.length-1}", True, (0, 0, 0))
        self.screen.blit(line1, (200, 300))
        line2 = font.render("To play again press Enter. To exit press Escape!", True, (0, 0, 0))
        self.screen.blit(line2, (200, 350))

        pygame.display.flip()

        pygame.mixer.music.pause()

    def reset(self):
        self.snake = Snake(self.screen, 1)
        self.apple = Apple(self.screen)


    def display_score(self):
        font = pygame.font.SysFont('arial', 30)
        score = font.render(f"Score: {self.snake.length-1}", True, (0, 0, 0))
        self.screen.blit(score, (70, 100))

    def run(self):
        pause = False

        while True:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        exit()
                    
                    elif event.key == K_RETURN:
                        pygame.mixer.music.unpause()
                        pause = False

                    if not pause:
                        if event.key == K_DOWN:
                            if self.snake.direction != 'up':
                                self.snake.move_down()

                        elif event.key == K_UP:
                            if self.snake.direction != 'down':
                                self.snake.move_up()

                        elif event.key == K_LEFT:
                            if self.snake.direction != 'right':
                                self.snake.move_left()

                        elif event.key == K_RIGHT:
                            if self.snake.direction != 'left':
                                self.snake.move_right()

                if event.type == QUIT:
                    pygame.quit()
                    exit()

            try:
                if not pause:
                    self.play()
            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset()

            time.sleep(TIME)


if __name__ == "__main__":

    game = Game()
    game.run()