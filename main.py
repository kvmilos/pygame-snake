import pygame
from pygame.locals import *
import time
import random

TIME = .15
SIZE = 20
S_X = 1200
S_Y = 800
BACKGROUND_COLOUR = (102, 255, 178)

class Apple:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.image = pygame.image.load("sprites/apple.png").convert()
        self.x = SIZE*3
        self.y = SIZE*3

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    def generate(self):
        self.x = random.randint(0,S_X//SIZE-1)*SIZE
        self.y = random.randint(0,S_Y//SIZE-1)*SIZE

class Snake:
    def __init__(self, parent_screen, length):
        self.length = length
        self.parent_screen = parent_screen
        self.part = pygame.image.load("sprites/snake.png").convert()
        self.head_up = pygame.image.load("sprites/snakeU.png").convert()
        self.head_down = pygame.image.load("sprites/snakeD.png").convert()
        self.head_right = pygame.image.load("sprites/snakeR.png").convert()
        self.head_left = pygame.image.load("sprites/snakeL.png").convert()
        self.x = [SIZE]*length
        self.y = [SIZE]*length
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
        self.parent_screen.fill(BACKGROUND_COLOUR)
        head_image = head_images[self.direction]
        self.parent_screen.blit(head_image, (self.x[0], self.y[0]))
        for i in range(1, self.length):
            self.parent_screen.blit(self.part, (self.x[i], self.y[i]))
        pygame.display.flip()

    def move_left(self):
        self.direction = 'left'

    def move_right(self):
        self.direction = 'right'

    def move_up(self):
        self.direction = 'up'

    def move_down(self):
        self.direction = 'down'

    def remove_tail(self, x, y):
        pygame.draw.rect(self.parent_screen, BACKGROUND_COLOUR, (x, y, SIZE, SIZE))
        pygame.display.flip()

    def walk(self):
        del_x, del_y = self.x[self.length-1], self.y[self.length-1]

        for i in range(self.length-1, 0, -1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]
        
        if self.direction == 'down':
            self.y[0] += SIZE
        elif self.direction == 'up':
            self.y[0] -= SIZE
        elif self.direction == 'left':
            self.x[0] -= SIZE
        elif self.direction == 'right':
            self.x[0] += SIZE
        
        self.remove_tail(del_x, del_y)
        self.draw()


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Gra Snake")

        pygame.mixer.init()
        self.play_background_music()

        self.screen = pygame.display.set_mode((S_X, S_Y))
        self.screen.fill(BACKGROUND_COLOUR)
        self.snake = Snake(self.screen, 1)
        self.snake.draw()
        self.apple = Apple(self.screen)
        self.apple.draw()
    
    def is_collision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2+SIZE:
            if y1 >= y2 and y1 <y2+SIZE:
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
        if not (0 <= self.snake.x[0] <= S_X and 0 <= self.snake.y[0] <= S_Y):
            self.play_sound('lose.wav')
            raise "Hit the boundary"
            
    def show_game_over(self):
        self.screen.fill(BACKGROUND_COLOUR)
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
        self.screen.blit(score, (100, 100))

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