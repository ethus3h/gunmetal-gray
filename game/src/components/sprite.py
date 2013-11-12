#!/usr/bin/env python

"""
Visual sprite components
"""

import pygame
import animation


class StaticSprite(pygame.sprite.Sprite):
    """A still image to be displayed on the screen."""
    def __init__(self, gameobject, image, offset_x=0, offset_y=0):
        pygame.sprite.Sprite.__init__(self)

        self.image = image
        self.rect = image.get_rect()
        self.gameobject = gameobject
        self.offset_x = offset_x
        self.offset_y = offset_y
        gameobject.obj_mgr.visible.add(self)
        self.visible = True

    def update(self, camera_x, camera_y):
        """Update the position of the sprite on the screen"""
        self.rect[0] = int(self.gameobject.x + self.offset_x + camera_x)
        self.rect[1] = int(self.gameobject.y + self.offset_y + camera_y)

    def destroy(self):
        self.gameobject.obj_mgr.visible.remove(self)

    def setVisibility(self, visible):
        if visible and not self.visible:
            self.gameobject.obj_mgr.visible.add(self)
        if not visible and self.visible:
            self.gameobject.obj_mgr.visible.remove(self)
        self.visible = visible

    def debug_draw(self, surface, camera_x, camera_y):
        if self.visible:
            pygame.draw.rect(surface, (255,0,0), self.rect, 1)


class AnimSprite(StaticSprite):
    """An animated graphic to be displayed on the screen."""
    def __init__(self, gameobject, anim, sequence, offset_x=0, offset_y=0):
        StaticSprite.__init__(self, gameobject, anim.getSequence(sequence).frames[0][0], offset_x, offset_y)
        self.animation = anim
        self.cursor = animation.SimpleCursor()
        self.cursor.play(anim.getSequence(sequence))

    def play(self, sequence_name, reset = True):
        """Play the specified animation sequence.  If reset is True the frame number goes back to 0,
otherwise, it attempts to play the new sequence starting at the current frame."""
        self.cursor.play(self.animation.getSequence(sequence_name), reset)

    def updateAnim(self, td):
        """Update the animation and set the sprite's image to the current frame image."""
        self.cursor.update(td)
        self.image = self.cursor.frame
