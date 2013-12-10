#!/usr/bin/env python

from gameobject import GameObject
from components import AnimSprite, SpriteCollide
import statevars
import assets

class Outhouse(GameObject):
    def __init__(self, scene, name, x, y, **kwargs):
        super(Outhouse, self).__init__(scene, name, x, y, **kwargs)
        self.sprite = AnimSprite(self, assets.getSpriteAnim("anims/outhouse.json"), "closed", layer=0)
        self.collider = SpriteCollide(self, 67, 56, 25, 103)
        self.state = 0

    def init(self):
        self.scene.normal_update.append(self)
        self.collider.addToGroup(self.obj_mgr.interactive)

    def destroy(self):
        self.scene.normal_update.remove(self)
        self.collider.removeFromGroup(self.obj_mgr.interactive)

    def spriteCollide(self, gameobject, collider):
        pass

    def interact(self, obj):
        self.state = 1
        self.sprite.play("opening")
        obj.call("doHeal", 1000)
        statevars.save()
        return True

    def update(self, td):
        self.sprite.updateAnim(td)
        if self.state == 1:
            if not self.sprite.cursor.playing:
                self.state = 2
                self.sprite.play("closing")
        elif self.state == 2:
            if not self.sprite.cursor.playing:
                self.state = 0
                self.sprite.play("closed")

    def debug_draw(self, surface, camera_x, camera_y):
        super(Outhouse, self).debug_draw(surface, camera_x, camera_y)
        self.sprite.debug_draw(surface, camera_x, camera_y)
        self.collider.debug_draw(surface, camera_x, camera_y)
