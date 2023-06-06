import os
import pickle
import random

import pyved_engine as pyv
pyv.bootstrap_e()


# --------------------
#  on purpose disabling pygame.display.flip,
#  to make sure that we always call pyv.flip() -> use the custom game engine!
# --------------------
def brokendef():
    raise NotImplementedError


pyv.pygame.display.flip = brokendef


from internal.classes.GlGameModel import GlGameModel
from internal.DISPLAY import interface, effects, menu, display, text
from internal.HERO import hero_creator
from internal.IMG import images
from internal.SND import sfx
from internal.UTIL import colors, load_image, button
from internal.UTIL import inputHandler
from internal.gamestates import MainState


pygame = pyv.pygame
android = False
game_model = None
mixer = None
# Set the height and width of the screen
# cfac = 1.0
# screenSize = [1280, 720]  # [720, 700]
# screen = pygame.display.set_mode(screenSize)
screen = scr_size = None
stored_avatar = None

# const.setScaleFactor(1)
pyv.init(1)
# pygame.init()
pygame.mixer.init()
mixer = pygame.mixer
pygame.display.set_caption("Ransack")
pygame.key.set_repeat(100, 100)
images.preload_all()
clock = pygame.time.Clock()
random.seed(os.urandom(1))
FX = iH = iFace = None
SFX = sfx.sfx(mixer)
D = display.Display(screen, images)

# this is the static game world i.e. non-generated world
# loaded once at startup and used thereafter
myWorldBall = None
selection = 0
options = ['Begin New Game', 'Load Saved Game', 'Credits', 'Exit']
buttons = []
ifaceImg, r = load_image.load_image(os.path.join('MENU', 'interface_m.png'), None)
logo, r = load_image.load_image('logo.png', None)


def endScreen(game, msg):
    spi = os.getcwd() + "/FONTS/SpinalTfanboy.ttf"
    dev = os.getcwd() + "/FONTS/devinne.ttf"
    got = os.getcwd() + "/FONTS/gothic.ttf"
    dScreen = pygame.Surface((screen.get_width(), screen.get_width()))
    dScreen.fill(colors.black)
    msgText = text.Text(msg, os.getcwd() + "/FONTS/Squealer.ttf", 18,
                        colors.white, colors.gold)
    dScreen.blit(text.Text("Game Over", spi, 72, colors.red, colors.black),
                 (50, 0))
    font = pygame.font.Font("./FONTS/devinne.ttf", 18)
    if game.myHero.level < 4:
        dScreen.blit(text.Text("Nice Try, loser!", dev, 18,
                               colors.white, colors.black), (50, 200))
    elif game.myHero.level >= 4 and game.myHero.level < 10:
        dScreen.blit(text.Text("Not bad... for a beginner!", dev, 18,
                               colors.white, colors.black), (50, 350))
    dScreen.blit(text.Text("Level reached: {}".format(game.myHero.level),
                           got, 18, colors.white, colors.black), (50, 500))
    dScreen.blit(text.Text("{} days, {}:{}.{}".format(
        game.Ticker.getDays(),
        game.Ticker.getHours() % 24,
        game.Ticker.getMins() % 60,
        game.Ticker.getSecs()),
        got, 14, colors.white,
        colors.black), (50, 250))
    '''
    screen.blit(pygame.transform.scale(dScreen, (int(ceil(300 * 2.4)),
                                                 int(ceil(300 * 2.4)))),
                                                 (0, 0) )
                                                 '''
    screen.blit(dScreen, (0, 0))

    # pygame.display.flip()
    pyv.flip()

    while pygame.event.wait().type != pygame.MOUSEBUTTONDOWN:
        pass


def gameloop(game_obj):
    # self.myMenu.displayStory(
    # self.Director.setEvent(0)
    game_obj.curr_state.enter_state()
    game_obj.curr_updatefunc = game_obj.curr_state.update_chunk

    while game_obj.gameOn:
        while game_obj.curr_state_name == game_obj.neostate:
            game_obj.curr_updatefunc()

        # this was not working anyway
        # self.myInterface.state = 'mainmenu'

        # game state change
        st_name = game_obj.neostate
        game_obj.curr_initfunc = game_obj.states[st_name].enter_state
        game_obj.curr_initfunc()

        game_obj.curr_updatefunc = game_obj.states[st_name].update_chunk
        game_obj.curr_state_name = st_name

    # TODO fix this, endgame condition
    # return self.won


def init_game_model():
    global screen, scr_size, FX, iH, iFace
    global buttons, game_model, stored_avatar

    screen = pyv.get_surface()
    scr_size = screen.get_size()

    # - prelim -
    FX = effects.effects(clock, screen)
    iH = inputHandler.inputHandler(FX)
    iFace = interface.Interface(screen, iH)

    y = 350
    if pygame.font:
        font = pygame.font.Font("./FONTS/chancery.ttf", 60)
    for o in options:
        line = font.render(o, 1, colors.white, colors.black)
        buttons.append(
            button.Button(((screen.get_width() / 2) - (line.get_width() / 2), y), o)
        )
        y += 75

    game_model = GlGameModel(clock, screen, images, iFace, FX, iH, SFX, myWorldBall)
    game_model.set_state('game')
    print('CC')


# - deprecated?
# def loadWorld():
#     try:
#         if android:
#             pass
#         loadedWorld = gzip.GzipFile(os.getcwd() + '/MAP/WORLDS/MainWorld', 'rb', 1)
#         myWorldBall = pickle.load(loadedWorld)
#         loadedWorld.close()
#         # self.installWorldBall(ball, context)
#     except IOError as io_err:
#         print('Cannot load world: {}'.format(io_err))
#         return


def loadSavedGame(titleScreen):
    raise NotImplementedError
    # if android:
    #     android.hide_keyboard()
    # try:
    #     FX.displayLoadingMessage(titleScreen, 'Loading game file...')
    #     savFile = gzip.GzipFile('ransack0.sav', 'rb', 1)
    #     FX.displayLoadingMessage(titleScreen, 'Loading saved game...')
    #     ball = pickle.load(savFile)
    #     savFile.close()
    #     Game = game.game(images, screen, clock, iFace,
    #                      FX, iH, titleScreen, SFX, myWorldBall,
    #                      ball[0], ball[1], ball[2], ball[3])
    #     FX.fadeOut(0)
    #     iFace.state = 'game'
    #     if Game.mainLoop():
    #         endScreen(Game, "You Win!")
    #     else:
    #         endScreen(Game, "Game Over.")
    #     FX.fadeOut(0)
    # except IOError as err:
    #     print('loadSavedGame error: {}'.format(err))


def showCredits():
    creditsMenu = menu.menu(screen, iH, D, iFace, FX, SFX)
    creditsMenu.displayStory(
        "Ransack - An RPG Roguelike. All game code, story (if you can call it"
        " that!) and artwork, with the exclusion of fonts, created by"
        " D. Allen. dsallen7@gmail.com Powered by Python - www.python.org"
        " Game engine built with Pygame - pygame.org and ported to Android"
        " using PGS4a - pygame.renpy.org/")
    creditsMenu.displayStory(
        "Fonts used in game: Steelfish, Sqeualer by Ray"" Larabie,"
        " Typodermic Fonts - http://www.dafont.com/ typodermic.d1705 Gothic"
        " and Chancery by URW Software. urwpp.de/")
    creditsMenu.displayStory(
        "I'm a big fan of all the classic roguelikes, and"" cult favorites"
        " like Castle of the Winds and Moraff's World, as well as"
        " Japanese-style RPGs, from Final Fantasy to Suikoden to Pokemon."
        " So, you could call this a melting pot of all my gaming influences.")
    creditsMenu.displayStory(
        "This is a work in progress. I thank you for"" playing and if you"
        " notice any bugs or errors, have any ideas for improvments or"
        " enhancenments please drop me a line!")


def paint():
    titleScreen = pygame.Surface((scr_size[0], scr_size[1]))
    menuBox = pygame.Surface((300, 300))
    menuBox.fill(colors.black)
    menuBox.set_colorkey(colors.black)
    clock.tick(20)
    screen.fill(colors.black)
    screen.blit(titleScreen, (0, 0))
    screen.blit(logo, ((screen.get_width() // 2) - (logo.get_width() // 2), 100))
    if pygame.font:
        font = pygame.font.Font("./FONTS/SpinalTfanboy.ttf", 48)
        for b in buttons:
            screen.blit(b.img, (b.locX, b.locY))
            # line = font.render(options[i], 1, colors.white, colors.black)
            # menuBox.blit(line, (30, (i * line.get_height())))
    # menuBox = pygame.Surface( (450,450) )
    # menuBox.fill( colors.black )
    # menuBox.set_colorkey(colors.black)


def main():
    global game_model
    init_game_model()
    while True:
        selected_button = None

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                (mX, mY) = pygame.mouse.get_pos()
                for b in buttons:
                    if b.hit(mX, mY):
                        selected_button = b.msg
        # logic update
        if selected_button == 'Begin New Game':
            char_creator = hero_creator.Creator()
            char_creator.mainLoop(screen)  # /!\ blocking
            game_model.curr_state.set_hero(char_creator.created_hero)
            game_model.curr_state.pre_launch_game()

            print('Begin New Game {}x{}'.format(scr_size[0], scr_size[1]))
            gameloop(game_model)  # ver 3
            # ver 2 -- start_new_game(screen)
            # ver 1 -- pygame.Surface(screenSize[0], screenSize[1])
        elif selection == 'Load Saved Game':
            loadSavedGame(pygame.Surface((scr_size[0], scr_size[1])))
        elif selection == 'Credits':
            showCredits()
        elif selection == 'Exit':
            FX.fadeOut(0)
            os.sys.exit()

        # font = pygame.font.Font(os.getcwd() + "/FONTS/courier.ttf", 28)
        # if android:
        #     screen.blit(font.render(str(android.get_dpi()), 1, colors.white,
        #                             colors.black), (0, 0))
        paint()
        # pygame.display.flip()
        pyv.flip()


if __name__ == '__main__':
    from internal import MAP as legacyMAP
    # fix imports for piclk ok
    import sys
    sys.modules['MAP'] = legacyMAP
    try:
        # '''
        # if android:
        #     MW = android.assets.open('WORLDS/MainWorld')
        # else:
        #     MW = open('assets/WORLDS/MainWorld', 'r')
        #     '''
        MW = open('assets/WORLDS/MainWorld', 'rb')
        loadedWorld = MW
        myWorldBall = pickle.load(loadedWorld)
        # print myWorldBall
        loadedWorld.close()
    except pickle.UnpicklingError as err:
        print('Cannot load MainWorld: {}'.format(err))
        os.sys.exit()
    except IOError as err:
        print('Cannot load MainWorld: {}'.format(err))
        os.sys.exit()
    main()
