from ..UTIL import ticker
from ..DISPLAY import display
from . import director
from ..gamestates import MainState, StoryState


class GlGameModel:
    def __init__(self, clockobj, screen, images, interface_obj, FX, iH, SFX, worldBall, loadTicker=None, loadDirector=None, ldWorld=None):
        self.story_message = None
        self.curr_state = None
        self.curr_state_name = None

        if loadTicker is None:
            adhoc_ticker = ticker.Ticker()
        else:
            adhoc_ticker = loadTicker
        GivenDisplay = display.Display(screen, images)
        if loadDirector is None:
            adhoc_director = director.Director()
        else:
            adhoc_director = loadDirector

        self.neostate = 'game'  # if two are different then gamestate changes!
        # NB. Tom:
        # When should we instantiate other gamestates?
        self.states = {
            'game': MainState(clockobj, screen, GivenDisplay, interface_obj, adhoc_director, FX, iH, SFX, worldBall, adhoc_ticker, ldWorld, self),
            'story': StoryState(GivenDisplay, interface_obj, adhoc_director, FX, self),
        }
        self.curr_state = None

        self.gameOn = True

    def set_state(self, st_name):
        self.curr_state_name = st_name
        self.curr_state = self.states[st_name]
