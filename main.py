import math
import pygame
import random
import sys
from Wall import Wall
from Player import Player
pygame.init()
#VARIABLES
m_width, m_height = 2400, 600
width, height = 800,600
background_color = (63,63,116)
empty = (0,0,0,0)
gravity = 2  # przyspieszenie grawitacyjne
dt = 1 # Krok czasowy
h = 200
xh = 100
v0 = 5
vx = 2
font = pygame.font.Font('freesansbold.ttf', 20)
prev_colliding = True
fall = False
camera_offset = 20
prev_x = 0

#SURFACES
screen = pygame.display.set_mode((width, height))
surface = pygame.Surface((width, height), pygame.SRCALPHA)
surface_walls = pygame.Surface((m_width, m_height), pygame.SRCALPHA)
surface_objects = pygame.Surface((m_width, m_height), pygame.SRCALPHA)
surface_interface = pygame.Surface((m_width, m_height), pygame.SRCALPHA)
#IMAGES
wall = pygame.image.load("wall.png")
wall = pygame.transform.scale(wall, (50, 50))
#MAP
walls = []
map = open("map.txt", "r")
text = []
for line in map:
    text.append(line)
text = '\n'.join(text)

def draw_map():
    mapx = 0
    mapy = 0
    for line in text.split('\n'):
        for char in line:
            if char == "-":
                surface_walls.blit(wall, (mapx, mapy))
                walls.append(Wall(mapx,mapy,50,50))
            mapx += 50
            if mapx >= m_width:
                mapx = 0
                mapy += 50

def draw_interface():
    text_h = font.render("Max height: " + str(h), True,(255,99,194))
    text_x = font.render("Max distance: " + str(xh), True,(255,99,194))
    text_v = font.render("v0: " + str(v0), True,(255,99,194))
    text_g = font.render("g: " + str(gravity),True,(255,99,194))
    surface_interface.blit(text_h, (10,10))
    surface_interface.blit(text_x, (10, 40))
    surface_interface.blit(text_v, (10, 70))
    surface_interface.blit(text_g, (10, 100))

def is_colliding():
    for wall1 in walls:
        if wall1.isCollidingCircle(p1):
            return True
    return False


if __name__ == '__main__':
    draw_map()
    p1 = Player(100, 530, 0, 0, 0, 0, surface_objects)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_z:
                    h += 10
                elif event.key == pygame.K_x:
                    if h>10:
                        h -= 10
                elif event.key == pygame.K_a:
                    xh += 10
                elif event.key == pygame.K_s:
                    if xh > 10:
                        xh -= 10
        keys_pressed = pygame.key.get_pressed()
        surface.fill(background_color)
        surface_objects.fill(empty)
        surface_interface.fill(empty)
        p1.drawCircle()
        gravity = -2*h * (pow(vx,2)/pow(xh,2))
        v0 = 2*h*(vx/xh)
        if keys_pressed[pygame.K_LEFT]:
            if not p1.is_jumping:
                p1.velocityx = -2
        elif keys_pressed[pygame.K_RIGHT]:
            if not p1.is_jumping:
                p1.velocityx = 2
        elif not p1.is_jumping:
            p1.velocityx = 0
        if keys_pressed[pygame.K_SPACE]:
            p1.jump(v0)
        if fall is False:
            if p1.update(gravity, dt, is_colliding()) is True:
                fall = True
        else:
            p1.fall(gravity, dt)
        curr = is_colliding()
        if curr is False and prev_colliding is True and p1.is_jumping is False:
            fall = True
        prev_colliding = curr
        for wall in walls:
            if wall.isCollidingCircle(p1):
                separation_vector = [0, 0]
                pom = (15 - wall.distance) / wall.distance
                vector_x = p1.x - wall.clamp_x
                vector_y = p1.y - wall.clamp_y
                separation_vector[0] = vector_x * pom
                separation_vector[1] = vector_y * pom
                if p1.velocityx > 0:
                    p1.x += separation_vector[0]
                elif p1.velocityx < 0:
                    p1.x -= separation_vector[0]
                p1.y += separation_vector[1]
                if p1.is_jumping:
                    p1.stop_jump(gravity, dt)
                    fall = True
                else:
                    fall = False
        camera_offset += prev_x-p1.x
        prev_x = p1.x
        draw_interface()
        screen.blit(surface,(0,0))
        screen.blit(surface_walls, (camera_offset/1.5, 0))
        screen.blit(surface_objects, (camera_offset/1.5,0))
        screen.blit(surface_interface, (0, 0))
        pygame.display.flip()
