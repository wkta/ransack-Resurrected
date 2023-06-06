import os
from math import ceil

import pyved_engine as pyv

from internal.DISPLAY.menu import openWindow
from ..DISPLAY import text
from ..UTIL import const, colors


pygame = pyv.pygame


class StoryState:
    def __init__(self, ref_display, ref_iface, ref_director, ref_fx, refgame):
        """

        :param ref_display: Display obj
        :param ref_iface: interface recv from interface
        :param ref_director: (loadDirector)
        :param ref_fx: FX object recv from game
        :param refgame: reference to game object (so we can change the state manually)
        """
        self.ref_game = refgame

        self.screen = pyv.get_surface()
        self.curr_msg = None
        self.ref_disp = ref_display
        self.ref_iface = ref_iface
        self.ref_fx = ref_fx
        self.director = ref_director

    def set_message(self, msg):
        self.curr_msg = msg

    def enter_state(self):
        if self.curr_msg is not None and len(self.curr_msg)>0:
            storyBoxWin = openWindow(self.screen, 350, 300)
            self.storyBox = pygame.transform.scale(storyBoxWin,
                                              (int(ceil(storyBoxWin.get_width() * const.scaleFactor)),
                                               int(ceil(storyBoxWin.get_height() * const.scaleFactor))))
            self.msg_ = text.Text(self.curr_msg, os.getcwd() + "/FONTS/devinne.ttf", 14, colors.white, colors.gold, True, 30)
        else:
            self.curr_msg = None

    def update_chunk(self):
        """
        method supposed to show a blocking popup over the rest of the game GUI.
        Tom:this needs Refactoring! -> no more 2nd-level order game loops!
        """
        # ------------------------
        # init-like Chunck of code
        # ------------------------
        if self.curr_msg is None:
            self.ref_game.neostate = 'game'
            return

        # -------------------------
        # update-like Chunk of code
        # -------------------------
        for ev in pygame.event.get():  # previously,game used pygame.event.wait().type != pygame.MOUSEBUTTONDOWN ...
            if ev.type == pygame.MOUSEBUTTONDOWN:
                print('force stop display story0')
                self.director.setEvent(0)
                self.ref_game.neostate = 'game'
                return  # exit the curr loop

        self.storyBox.blit(self.msg_, ((self.storyBox.get_width() / 2) - (self.msg_.get_width() / 2),
                             (self.storyBox.get_height() / 2) - (self.msg_.get_height() / 2) + 41))
        self.screen.blit(self.storyBox, (0, 41))
        # TODO remake this
        self.ref_disp.displayOneFrame(self.ref_iface, self.ref_fx)
        pyv.flip()  # we need to updtae gfx mem
