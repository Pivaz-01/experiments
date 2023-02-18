import pygame
import math

WIDE, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDE, HEIGHT))

class Ball:
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.vel_x = 0.
        self.vel_y = 0.

    def draw(self, win):
        pygame.draw.circle(win, (0,0,0), (self.x, self.y), self.radius)
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius - 1)

    @staticmethod
    def ballPath(start_x, start_y, vel, timeframe, radius):
        a = 50

        new_x = start_x + vel[0] * timeframe
        new_y = start_y + vel[1] * timeframe

        new_vel_x = vel[0]
        new_vel_y = vel[1] + a * timeframe

        if new_x <= radius or new_x >= 800 - radius:
            new_vel_x = - new_vel_x
        
        if new_y <= radius:
            new_vel_y = - new_vel_y

        return new_x, new_y, new_vel_x, new_vel_y

def redrawWin(ball, line):
    WIN.fill((64,64,64))

    ball.draw(WIN)

    pygame.draw.line(WIN, (255,255,255), line[0], line[1])
    pygame.display.update()

def main():
    radius = 10
    x_in = 400
    y_in = 600 - radius
    WHITE = (255,255,255)
    ball = Ball(x_in, y_in, radius, WHITE)
    flying = False
    time = 0.1

    run = True
    while run:
        if flying:
            if ball.y <= 600 - radius:
                new_data = ball.ballPath(ball.x, ball.y, (ball.vel_x, ball.vel_y), time, radius)
                ball.x = new_data[0]
                ball.y = new_data[1]
                ball.vel_x = new_data[2]
                ball.vel_y = new_data[3]
            else: 
                flying = False
                ball.y = 600 - radius

        pos = pygame.mouse.get_pos()
        line = [(ball.x, ball.y), pos]            
        redrawWin(ball, line)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if flying == False:
                    flying = True
                    p = math.sqrt((line[1][1] - line[0][1])**2 + (line[1][0] - line[0][0])**2) 
                    angle = math.atan2(line[1][1] - line[0][1], line[1][0] - line[0][0])
                    power = p * math.cos(angle), p * math.sin(angle)
                    ball.vel_x = power[0]
                    ball.vel_y = power[1]

    pygame.quit()


main()