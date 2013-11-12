#!/usr/bin/env python

"""
Pauses the game and shows a dialog box with text in it.
"""

from gamestate import State
import ui
import assets
import statemgr

class DialogState(State):
    def __init__(self):
        super(DialogState, self).__init__()
        self.old_state_name = ""
        self.old_state = None
        self.image = assets.getImage("graphics/dialog.png")

    def gainFocus(self, previous, previous_name, text="", *args, **kwargs):
        """What should be done when the state gets focus.  Previous is the state that had focus before this one."""
        self.old_state = previous
        self.old_state_name = previous_name
        self.ui = ui.UI(96, 208)
        self.txtbox = ui.ScrollText(16, 8, 256, 33, text, 0.15)
        self.ui.add(self.txtbox)
        self.ui.add(ui.Button(287, 37, "", self.scroll))

    def scroll(self):
        """If the text box is already at the bottom, go back to the old state, else tells the text box to scroll."""
        if self.txtbox.atBottom:
            statemgr.switch(self.old_state_name)
        else:
            self.txtbox.scrollDown()

    def loseFocus(self, next, next_name, *args, **kwargs):
        """What should be done when the state loses focus.  Next is the new state that is being switched to."""
        pass

    def update(self, td):
        """Update the UI"""
        self.ui.update(td)

    def draw(self, surface):
        """Draw the UI"""
        self.old_state.draw(surface)
        surface.blit(self.image, (96,208))
        self.ui.draw(surface)

    def debug_draw(self, surface):
        self.old_state.debug_draw(surface)

    def event(self, event):
        """Should return true if game is still playing and false if the window should close"""
        return True
