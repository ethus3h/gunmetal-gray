#!/usr/bin/env python

"""
The playing part of the game, with the level, player, and other stuff all moving around.
"""

from states.gamestate import State
import scene
import inputs
import statemgr
import energybar
import statevars
import pygame
import assets
import music

class PlayState(State):
    def __init__(self):
        super(PlayState, self).__init__()
        self.init = True
        self.help_text="""                                  ~yellow~*** HELP ***~white~
In ~yellow~Cat Astro Fee ~white~you play as an astronaut who happens to
also be a cat.  Why is he a cat?  For the pun, of course!
On each planet, he has to collect enough ~yellow~coins ~white~to pay to
get past the ~yellow~space toll booths~white~.

Controls can be configured in ~yellow~data/config.json~white~, but the
default settings are ~yellow~keyboard ~white~with the '~yellow~ARROW KEYS~white~' to move,
'~yellow~Z~white~' to jump, '~yellow~X~white~' to shoot, and '~yellow~ENTER~white~' to pause the game.
~yellow~EMTs~white~ (Emergency Medical Teleporters) are used to save your
progress and act as checkpoints you can respawn at after
losing all your health.
Watch out for enemies, spikes, lava, and other hazards.
If you take damage, a refreshing ~yellow~Fish Soda~white~ refills a
little bit of health.
After collecting all the ~yellow~coins~white~ in the level, return to the
~yellow~space ship~white~ to blast off and head to the next planet!
"""
        self.scene = None

    def setPlayer(self, player):
        """Link up player object with the health bar"""
        self.energy_bar.setHealth(player.health)

    def respawn(self):
        """Reload the level when the player respawns"""
        statevars.load()
        self.start()

    def start(self):
        """Initialization for the play state"""
        # The player's energy bar
        self.energy_bar = energybar.EnergyBar(None, 4, 4)

        # Get the map state variable
        map_file = statevars.variables.get("map_file")
        map = statevars.variables.get("maps").get(map_file)

        if map is None:
            # Since there is no map variable (like when playing a new game), we'll create one and start at the start.
            map = {
                "events":[]
            }
            statevars.variables["maps"][map_file] = map

        if self.scene is not None:
            # Get rid of old scene
            self.scene.destroy()

        # Create the scene by loading the specified map file
        self.scene = scene.Scene(self, map_file)

        # Get the spawn point for the player.  It would be None if the player has not saved in this map yet.
        spawn = statevars.variables.get("spawn")
        if spawn is not None:
            # Spawn the player at the specified spawn point
            obj = self.scene.object_mgr.get(spawn)
            obj.call("spawnPlayer")

    def gainFocus(self, previous, previous_name, *args, **kwargs):
        """What should be done when the state gets focus.  Previous is the state that had focus before this one."""
        if self.init:
            self.init = False
            self.start()
        music.play_level_music()

    def loseFocus(self, next, next_name, *args, **kwargs):
        """What should be done when the state loses focus.  Next is the new state that is being switched to."""
        pass

    def update(self, td):
        # Pause the game if the player presses the pause button
        if inputs.getPausePress():
            statemgr.switch("pause")

        self.scene.update(td)
        self.energy_bar.update()

    def draw(self, surface):
        self.scene.draw(surface)

        # Energy bar and coins amount
        self.energy_bar.draw(surface)

    def debug_draw(self, surface):
        self.scene.debug_draw(surface)

    def event(self, event):
        """Should return true if game is still playing and false if the window should close"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F1:
                statemgr.switch("dialog", text=self.help_text)
        return True
