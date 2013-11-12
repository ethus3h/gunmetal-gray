#!/usr/bin/env python

"""
Simple physics
"""

class Physics:
    def __init__(self, gameobject, mapcollide, solidcollider, friction=0.03, air_resistance=0.0001, bounciness=0.0, gravity = 0.001):
        self.gameobject = gameobject
        self.mapcollide = mapcollide
        self.solidcollider = solidcollider
        self.vx = 0.0
        self.vy = 0.0
        self.friction = friction
        self.air_resistance = air_resistance
        self.bounciness = bounciness
        self.gravity = gravity
        self.force_x = 0.0
        self.force_y = 0.0
        self.jumping = False

    def update(self, td):
        was_on_ground = self.mapcollide.on_ground

        if not self.jumping and was_on_ground:
            self.setForceY(8.0 / (td+0.001))

        self.vx += self.force_x * td
        self.vy += (self.force_y + self.gravity) * td

        x = self.gameobject.x + self.vx * td
        y = self.gameobject.y + self.vy * td

        h_collide, v_collide, tile_x, tile_y = self.mapcollide.move(x,y)
        spr_h_collide, spr_v_collide, spr_x, spr_y = self.solidcollider.move(x,y)

        if self.vx < 0:
            self.gameobject.x = max(tile_x, spr_x)
        else:
            self.gameobject.x = min(tile_x, spr_x)

        if self.vy < 0:
            self.gameobject.y = max(tile_y, spr_y)
        else:
            self.gameobject.y = min(tile_y, spr_y)

        h_collide = h_collide or spr_h_collide
        v_collide = v_collide or spr_v_collide

        # TODO: This is not a good way of doing this.  Refactor and make this a little more sane.
        self.mapcollide.on_ground = self.mapcollide.on_ground or self.solidcollider.hit_bottom
        self.mapcollide.hit_top = self.mapcollide.hit_top or self.solidcollider.hit_top
        self.mapcollide.hit_bottom = self.mapcollide.hit_bottom or self.solidcollider.hit_bottom
        self.mapcollide.hit_left = self.mapcollide.hit_left or self.solidcollider.hit_left
        self.mapcollide.hit_right = self.mapcollide.hit_right or self.solidcollider.hit_right

        if h_collide:
            self.vx = -self.vx * self.bounciness

        if v_collide:
            if self.mapcollide.on_ground:
                self.vx -= self.vx * self.friction * td
                self.jumping = False
            self.vy = -self.vy * self.bounciness

        if not h_collide and not v_collide:
            self.vx -= self.vx * self.air_resistance * td
            self.vy -= self.vy * self.air_resistance * td

        if not self.jumping and not self.mapcollide.on_ground and was_on_ground:
            self.setForceY(0.0)
            # Compensate for the downward velocity
            self.gameobject.y -= 8

    def applyForce(self, x, y):
        self.vx += x
        self.vy += y

    def setForce(self, x, y):
        self.vx = x
        self.vy = y

    def setForceX(self, x):
        self.vx = x

    def setForceY(self, y):
        self.vy = y

    def jump(self, vy):
        self.jumping = True
        self.vy = vy

    def debug_draw(self, surface, camera_x, camera_y):
        import pygame
        pygame.draw.line(surface, (0, 255, 0), (self.gameobject.x + camera_x, self.gameobject.y + camera_y), (self.gameobject.x + self.vx * 100 + camera_x, self.gameobject.y + self.vy * 100 + camera_y))
