import pygame
import time
import math

from utils import scale_image, blit_rotate_center

pygame.init()

GRASS = scale_image(pygame.image.load("imgs/grass.jpg"), 2.5)
TRACK = scale_image(pygame.image.load("imgs/track.png"), 0.9)

FINISH = pygame.image.load("imgs/finish.png")
FINISH_MASK = pygame.mask.from_surface(FINISH)
FINISH_POSITION = (130, 250)

TRACK_BORDER = scale_image(pygame.image.load("imgs/track-border.png"), 0.9)
TRACK_BORDER_MASK = pygame.mask.from_surface(TRACK_BORDER)

RED_CAR = scale_image(pygame.image.load("imgs/red-car.png"), 0.55)

WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racing Game")

FPS = 60 # frames per second
font = pygame.font.Font("freesansbold.ttf",  30)

class AbstractCar:
    def __init__(self, max_vel, rotation_vel):
        self.img = self.IMG # gli assegno questa
        self.max_vel = max_vel
        self.vel = 0
        self.rotation_vel = rotation_vel
        self.angle = 0
        self.x, self.y = self.START_POS
        self.acceleration = 0.1

    def rotate(self, left = False, right = False):
        if left:
            self.angle += self.rotation_vel
        if right:
            self.angle -= self.rotation_vel
    def draw(self, win):
        blit_rotate_center(win, self.img, (self.x, self.y), self.angle)

    def move_forward(self):
        self.vel = min(self.vel + self.acceleration, self.max_vel)
        self.move()

    def move_backward(self):
        self.vel = max(self.vel - self.acceleration, -self.max_vel/2)
        self.move()

    def move(self):
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.vel
        horizontal = math.sin(radians) * self.vel

        self.y -= vertical
        self.x -= horizontal

    def collide1(self, mask, x=0, y=0):
        car_mask = pygame.mask.from_surface(self.img)
        offset = (int(self.x - x), int(self.y - y))
        poi = mask.overlap_area(car_mask, offset) # n of points of intersection
        return poi
    
    def collide2(self, mask, x=0, y=0):
        car_mask = pygame.mask.from_surface(self.img)
        offset = (int(self.x - x), int(self.y - y))
        poi = mask.overlap(car_mask, offset) # point of intersection
        return poi


    def reset(self):
        self.x, self.y = self.START_POS
        self.angle = 0
        self.vel = 0

class PlayerCar(AbstractCar):
    IMG = RED_CAR # userò questa
    START_POS = (180,200)
    
    def reduce_speed(self):
        self.vel = max(self.vel - self.acceleration / 2, 0)
        self.move()

    def bounce(self):
        self.vel = -self.vel / 2
        self.move()

def draw(win, images, player_car, time_race):
    for img, pos in images:
        win.blit(img, pos)
    
    player_car.draw(win)
    text = font.render(str(float(round(time_race, 2))), True, (0,0,0), (250,250,250)) 
    # True devo vederlo
    WIN.blit(text, (0,0))

    pygame.display.update()

def move_player(player_car):
    keys = pygame.key.get_pressed()
    moved = False

    if keys[pygame.K_a]: # se clicco a
        player_car.rotate(left = True)
    if keys[pygame.K_d]: # se clicco d
        player_car.rotate(right = True)
    if keys[pygame.K_w]: # se clicco d
        moved = True
        player_car.move_forward()
    if keys[pygame.K_s]: # se clicco s
        moved = True
        player_car.move_backward()    
    
    if moved:
        return 1
    if not moved:
        player_car.reduce_speed()

def main():
    run = True
    clock = pygame.time.Clock()
    images = [(GRASS, (0,0)), (TRACK, (0,0)), (FINISH, FINISH_POSITION), (TRACK_BORDER, (0,0))]
    player_car = PlayerCar(3,3)
    time_race = 0.
    start = False

    while run:
        clock.tick(FPS)

        draw(WIN, images, player_car, time_race)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            
        move_player(player_car)

        if move_player(player_car) == 1:
            start = True

        if start == True:
            time_race += 0.06

        if player_car.collide1(TRACK_BORDER_MASK) >= 150: # se c'è 150 punti di intersezione
            player_car.bounce()
            
        finish_poi_collide = player_car.collide2(FINISH_MASK, *FINISH_POSITION)
        if finish_poi_collide != None:
            if finish_poi_collide[1] == 0: # quando tocca il traguardo da sopra
                player_car.bounce()
            else: 
                player_car.reset()
                start = False
                print("Finish! \nTime:", round(time_race, 2))
                time_race = 0

    pygame.quit()

main()