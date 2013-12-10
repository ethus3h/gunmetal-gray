#!/usr/bin/env python

from gameobject import GameObject
import statemgr

class StartSpawn(GameObject):
    def __init__(self, scene, name, x, y, mapfile="", spawnpoint="", **kwargs):
        super(StartSpawn, self).__init__(scene, name, x, y, **kwargs)
        self.mapfile = mapfile
        self.spawnpoint = spawnpoint

    def spawnPlayer(self):
        """Create a player object"""
        self.obj_mgr.create("Player", "player", self.x, self.y)
        statemgr.switch("dialog", filename="dialogs/intro.json")

    def debug_draw(self, surface, camera_x, camera_y):
        super(StartSpawn, self).debug_draw(surface, camera_x, camera_y)
