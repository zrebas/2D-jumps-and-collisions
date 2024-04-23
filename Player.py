import pygame
class Player:
    def __init__(self, x, y, velocityx, velocityy, targetspeedx,targetspeedy, surface):
        self.x = x
        self.y = y
        self.velocityx = velocityx
        self.velocityy = velocityy
        self.targetspeedx = targetspeedx
        self.targetspeedy = targetspeedy
        self.surface = surface
        self.is_jumping = False
        self.is_falling = False
        self.vp = 0

    def drawCircle(self):
        pygame.draw.circle(self.surface, (234,128,222), (self.x, self.y), 15)

    def jump(self, v0):
        if not (self.is_jumping or self.is_falling):
            self.vp = v0
            self.velocityy = v0
            self.is_jumping = True

    def fall(self, gravity, dt):
        self.y -= self.velocityy + (gravity * dt / 2)
        self.velocityy += gravity * dt
    def update(self, gravity, dt, collide):
        self.is_falling = False
        if self.is_jumping:
            self.y -= self.velocityy + (gravity * dt / 2)
            self.velocityy += gravity * dt
            if self.x < 15 or self.x >2480:
                self.stop_jump(gravity, dt)
                return True
            else:
                self.x += self.velocityx
        if not self.is_jumping:
            if self.x <= 15:
                self.x = 16
            elif self.x >= 2380:
                self.x = 2379
            else:
                self.x += self.velocityx
            self.y -= self.velocityy + (gravity * dt / 2)
            if collide is True:
                self.velocityy += gravity * dt
        return False


    def stop_jump(self,gravity, dt):
        self.is_falling = True
        self.is_jumping = False
        self.velocityy = 0
        self.fall(gravity, dt)
