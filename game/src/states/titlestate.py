#!/usr/bin/env python

"""
The title state shows the title screen and let's the player select either a new game or continuing.
"""

from states import State
import statemgr
import assets
import statevars
import ui

class TitleState(State):
    """Base class for all game states to derive from"""
    def __init__(self):
        super(TitleState, self).__init__()
        self.image = assets.getImage("graphics/title.png")
        self.ui = ui.UI(220, 170)
        self.ui.add(ui.Button(0, 0, "Continue", self.btnContinue))
        self.ui.add(ui.Button(0, 20, "New Game", self.btnNewGame))

    def btnContinue(self):
        """Called when player selects Continue.  Loads the old save file then starts playing."""
        statevars.load("saves/save_1.json")
        statemgr.transition_switch("play", "Blink", "Spotlight")

    def btnNewGame(self):
        """Called when the player selects New Game.  Clear state variables, save them, then starts playing."""
        statevars.new_file("saves/save_1.json")
        statemgr.transition_switch("play", "Blink", "Spotlight")

    def gainFocus(self, previous, previous_name, *args, **kwargs):
        """What should be done when the state gets focus.  Previous is the state that had focus before this one."""
        pass

    def loseFocus(self, next, next_name, *args, **kwargs):
        """What should be done when the state loses focus.  Next is the new state that is being switched to."""
        pass

    def update(self, td):
        """Update user interface"""
        self.ui.update(td)

    def draw(self, surface):
        surface.blit(self.image, (0,0))
        self.ui.draw(surface)

    def debug_draw(self, surface):
        pass

    def event(self, event):
        """Should return true if game is still playing and false if the window should close"""
        return True
