#!/usr/bin/env python

from gameobject import GameObject
from components import StaticSprite, SpriteCollide
import statemgr
import assets

class Cave(GameObject):
    def __init__(self, scene, name, x, y, mapfile="", spawnpoint="", cavetype="entrance", **kwargs):
        super(Cave, self).__init__(scene, name, x, y, **kwargs)
        self.mapfile = mapfile
        self.spawnpoint = spawnpoint

        if cavetype == "entrance":
            self.sprite = StaticSprite(self, assets.getImage("graphics/cave_entrance.png"), layer=0)
        else:
            self.sprite = StaticSprite(self, assets.getImage("graphics/cave_exit.png"),  layer=0)
        self.collider = SpriteCollide(self, 64-16, 32, 32, 96)

    def init(self):
        """Initiation code."""
        self.obj_mgr.normal_update.append(self)
        self.collider.addToGroup(self.obj_mgr.interactive)

    def destroy(self):
        """Clean up code."""
        self.sprite.destroy()
        self.obj_mgr.normal_update.remove(self)
        self.collider.removeFromGroup(self.obj_mgr.interactive)

    def spawnPlayer(self):
        """Create a player object"""
        player = self.obj_mgr.create("Player", "player", self.x+96, self.y+64)
        player.spawn("door")

    def spriteCollide(self, gameobject, collider):
        pass

    def interact(self, obj):
        obj.call("enterDoor")
        statemgr.get("play").transitionMap(self.mapfile, self.spawnpoint)

    def debug_draw(self, surface, camera_x, camera_y):
        super(Cave, self).debug_draw(surface, camera_x, camera_y)
        self.sprite.debug_draw(surface, camera_x, camera_y)
        self.collider.debug_draw(surface, camera_x, camera_y)
