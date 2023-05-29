import pygame

from ..SCRIPTS import mapScr
from ..UTIL import colors, const


# Main graphics engine for Ransack.


class Display:

    def __init__(self, screen, images):
        self.screen = screen
        self.images = images.mapImages
        self.accImages = images.accessories
        self.fog = pygame.Surface((30, 30))
        self.fog.fill(colors.black)
        self.fog.set_alpha(192)

    def displayOneFrame(self, iFace, FX, board=None, game=None, dark=False, smooth=False):
        if game is not None:
            game.updateSprites()
            iFace.update(game)
            # board.blit( game.myHero.showLocation(), (0,50) )
        FX.update(self.screen)
        if board is not None:
            if game.myMap.type in const.darkMaps and dark:
                self.drawDarkness(game.myMap, board)
                # board.blit( self.SS_, (0, 0) )
            # pygame.time.delay(500)
            if smooth:
                pass
            '''
                self.screen.blit( pygame.transform.smoothscale(board,
                                                           (int(ceil(300 * const.scaleFactor)),
                                                            int(ceil(300 * const.scaleFactor)) ) ), (0,0) )
                                                            '''
            '''
            self.screen.blit( pygame.transform.scale(board,
                                                           (int(ceil(300 * const.scaleFactor)),
                                                            int(ceil(300 * const.scaleFactor)) ) ), (100,100) )'''

        # TODO can we fix the display to not call flip that
        #  many times?
        # pygame.display.flip()

    def drawShade(self, map, gameBoard):
        """Takes first two coordinates of hero rect, gameBoard and
        draws darkness
        """
        (topX, topY) = map.topMapCorner
        (px, py) = map.playerXY
        tiles = map.litTiles
        for x in range(map.WINDOWSIZE):
            for y in range(map.WINDOWSIZE):
                if (x + topX, y + topY) in tiles:
                    self.fog.set_alpha(0)
                else:
                    self.fog.set_alpha(140)
                gameBoard.blit(self.fog, ((x) * const.blocksize,
                                          (y) * const.blocksize), area=(0, 0, const.blocksize,
                                                                        const.blocksize))

    # Takes first two coordinates of hero rect, gameBoard and
    # draws darkness
    def drawDarkness(self, map, gameBoard, offset=(0, 0)):
        (oX, oY) = offset
        (topX, topY) = map.oldTopMapCorner
        (px, py) = map.playerXY
        tiles = map.litTiles
        for x in range(-1, map.WINDOWSIZE + 1):
            for y in range(-1, map.WINDOWSIZE + 1):
                if (x + topX, y + topY) not in tiles:
                    # AAfilledRoundedRect(surface,rect,color,radius=0.4)
                    gameBoard.blit(self.fog,
                                   ((x) * const.blocksize - oX,
                                    (y) * const.blocksize - oY),
                                   area=(0, 0, const.blocksize, const.blocksize))

    def redrawMap(self, map_obj, hero, gameBoard):
        """Redraw map on screen from current map matrix
        """
        # self.revealMap()
        (rx, ry, rx2, ry2) = hero.getRect()
        rx = rx / const.blocksize
        ry = ry / const.blocksize
        (topX, topY), (oldTopX, oldTopY) = map_obj.updateWindowCoordinates(hero)
        gameBoard.blit(self.getMapWindow((topX, topY),
                                         map_obj.WINDOWSIZE), (map_obj.WINDOWOFFSET, map_obj.WINDOWOFFSET))
        if map_obj.type in ['dungeon', 'maze', 'fortress']:
            self.drawShade(map_obj, gameBoard)
            # self.drawDarkness(rx, ry, gameBoard)

    def getMapWindow(self, pos, wsize=10):
        """takes map coordinates, returns map window
        """
        (x1, y1) = pos
        window = pygame.Surface((
            wsize * const.blocksize, wsize * const.blocksize))
        window.blit(self.xGameBoard, (-(x1 * const.blocksize),
                                      -(y1 * const.blocksize)))
        return window

    def getScrollingMapWindow(self, pos, wsize=10, darkness=True):
        """ takes pixel coordinates of top left corner of
        DIMxDIM window of xGameBoard, returns map window
        """
        (x1, y1) = pos
        window = pygame.Surface((wsize * const.blocksize,
                                 wsize * const.blocksize))
        window.blit(self.xGameBoard, (-x1, -y1))
        # self.drawDarkness
        return window

    def redrawXMap(self, thismap, light, local=False):
        """draws entire map to DIMxDIM Surface
            light: number of tiles visible from player
        """
        global map_obj
        self.xGameBoard = pygame.Surface((thismap.getDIM() * const.blocksize,
                                          thismap.getDIM() * const.blocksize))
        if thismap.type in const.darkMaps:
            thismap.revealMap(light)
        if local:
            (tX, tY) = thismap.topMapCorner
            rX = range(tX - 1, tX + const.HALFDIM + 1)
            rY = range(tY - 1, tY + const.HALFDIM + 1)
        else:
            (rX, rY) = (range(thismap.getDIM()), range(thismap.getDIM()))
        for x in rX:
            for y in rY:
                fTile = thismap.getTileFG(x, y)
                bTile = thismap.getTileBG(x, y)
                if fTile != const.VOID and thismap.visDict[(x, y)]:
                    # draw background tile first
                    if bTile is not None:
                        self.xGameBoard.blit(self.images[bTile], ((x * const.blocksize), (y * const.blocksize)))
                    # then foreground
                    else:
                        self.xGameBoard.blit(self.images[thismap.defaultBkgd],
                                             ((x * const.blocksize), (y * const.blocksize)))
                    '''
                    if tile > const.BRICK1:
                        shortList = [map.getEntry(tx, ty) for (tx, ty) in map.cardinalNeighbors((x,y))]
                        if const.VOID not in shortList:
                            self.xGameBoard.blit( self.images[ map.defaultBkgd ], ( (x*const.blocksize), (y*const.blocksize) ) )

                    if map.getEntry(x, y) == const.ITEMSDOOR:
                        self.xGameBoard.blit( self.images[128], (x*const.blocksize - const.blocksize, y*const.blocksize - 2*const.blocksize), area = self.images[128].get_rect() )
                    else: self.xGameBoard.blit( self.images[ tile ], ( (x*const.blocksize), (y*const.blocksize) ) )
                    '''
                    self.xGameBoard.blit(self.images[fTile], ((x * const.blocksize), (y * const.blocksize)))
                    # make the trees look thicker
                    # whenever four adjacent trees are drawn one the map, draw
                    # another one in the center

                    nbrL = thismap.getTileFG(x - 1, y)
                    nbrU = thismap.getTileFG(x, y - 1)
                    nbrUL = thismap.getTileFG(x - 1, y - 1)
                    if nbrL in mapScr.pines and nbrU in mapScr.pines and nbrUL in mapScr.pines and fTile in mapScr.pines:
                        self.xGameBoard.blit(self.images[mapScr.pineDict[fTile]],
                                             ((x * const.blocksize) - (const.blocksize / 2),
                                              (y * const.blocksize) - (const.blocksize / 2)))
                    # put accessories on the table
                    if fTile in range(const.TABLE1, const.TABLE3 + 1):
                        try:
                            self.xGameBoard.blit(self.accImages[thismap.grid[x][y].accessory],
                                                 (x * const.blocksize + 10,
                                                  y * const.blocksize + 5))
                        except AttributeError:
                            pass
        if thismap.type == 'village':
            for s in thismap.shops:
                (sX, sY) = s
                self.xGameBoard.blit(self.images[mapScr.siteImgDict[thismap.shops[s][0]][0]],
                                     (sX * const.blocksize - const.blocksize,
                                      sY * const.blocksize - (
                                                  mapScr.siteImgDict[thismap.shops[s][0]][1] * const.blocksize)))

    # draws all pending sprite movements
    def drawSprites(self, hero, map_obj, gameBoard, game=None, dir=None, animated=True):
        DIMEN = map_obj.getDIM()
        # by default, the hero is in the upper left corner of the map
        (newX, newY) = hero.getXY()
        map_obj.setPlayerXY(newX / const.blocksize, newY / const.blocksize)
        # top-left corner of hero sprite location
        (oldX, oldY, c, d) = hero.getRect()
        scrolling = False
        # where is new on-screen location of hero?
        if DIMEN > const.HALFDIM:
            if (5 * const.blocksize <= newX <= (DIMEN - 5) * const.blocksize):
                newX = 5 * const.blocksize
                if dir in ['left', 'right'] and oldX == 5 * const.blocksize:
                    scrolling = True
            if newX > (DIMEN - 5) * const.blocksize:
                if map_obj.getDIM() % 5 == 0:
                    newX = (5 * const.blocksize) + (newX % (5 * const.blocksize))  # + const.blocksize
                else:
                    newX = (5 * const.blocksize) + (newX % (5 * const.blocksize)) + const.blocksize
            if (5 * const.blocksize <= newY <= (DIMEN - 5) * const.blocksize):
                newY = 5 * const.blocksize
                if dir in ['up', 'down'] and oldY == 5 * const.blocksize:
                    scrolling = True
            if newY > (DIMEN - 5) * const.blocksize:
                if map_obj.getDIM() % 5 == 0:
                    newY = (5 * const.blocksize) + (newY % (5 * const.blocksize))  # + const.blocksize
                else:
                    newY = (5 * const.blocksize) + (newY % (5 * const.blocksize)) + const.blocksize
        else:
            newX += (const.HALFDIM - DIMEN) / 2 * const.blocksize
            newY += (const.HALFDIM - DIMEN) / 2 * const.blocksize

        # make the move animated
        if animated:
            if not hero.moving:
                scrolling = False
            if scrolling:
                scrollX, scrollY = const.scrollingDict[dir]
            else:
                (scrollX, scrollY) = (0, 0)
            (px, py) = hero.getXY()
            pos, oldPos = map_obj.updateWindowCoordinates(hero)
            (topX, topY) = pos
            if oldX == newX:
                xAxis = [oldX] * (const.blocksize)
            elif oldX < newX:
                xAxis = range(int(oldX), int(newX), 1)
            else:
                xAxis = range(int(oldX), int(newX), -1)
            if oldY == newY:
                yAxis = [oldY] * int(const.blocksize)
            elif oldY < newY:
                yAxis = range(int(oldY), int(newY), 1)
            elif oldY > newY:
                yAxis = range(int(oldY), int(newY), -1)
            for (idx, (i, j)) in list(enumerate(zip(xAxis, yAxis), start=1)):
                hero.setRect(i, j, const.blocksize, const.blocksize)
                for npc in game.NPCs:
                    if npc.moving:
                        npc.shiftOnePixel(npc.dir, -1)
                        if idx in [6, 12, 21, 27]:
                            npc.takeStep()
                # compensate for scrolling
                if scrolling:
                    for npc in game.NPCs:
                        npc.shiftOnePixel(dir, 1)
                    # self.redrawMap(map, hero, )
                    gameBoard.blit(self.getScrollingMapWindow(
                        ((topX * const.blocksize) + (idx * scrollX) - (const.blocksize * scrollX),
                         (topY * const.blocksize) + (idx * scrollY) - (const.blocksize * scrollY))), (0, 0))

                else:
                    self.redrawMap(map_obj, hero, gameBoard)

                if (idx % 3) == 0:

                    if hero.moving:
                        if idx in [6, 12, 21, 27]:
                            hero.takeStep()
                    self.displayOneFrame(game.myInterface, game.FX, game.gameBoard, game, True)
            hero.moving = False

        for npc in game.NPCs:
            npcdir = npc.dir
            (cX, cY) = npc.getXY()
            (tX, tY) = map_obj.topMapCorner
            (oRX, oRY, oRX2, oRY2) = npc.getRect()
            nRX = cX * const.blocksize - (tX * const.blocksize)
            nRY = cY * const.blocksize - (tY * const.blocksize)
            npc.setRect(nRX, nRY, const.blocksize, const.blocksize)
            npc.moving = False
            if npc.dir == 'up':
                npc.dir = 'down'
        hero.setRect(newX, newY, const.blocksize, const.blocksize)

        if map_obj.type in const.darkMaps:
            self.redrawXMap(map_obj, 2 + hero.hasItem(const.LANTERN), True)
