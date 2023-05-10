import random
from ..SCRIPTS import enemyScr
import random

from ..SCRIPTS import enemyScr


class enemy:
    def __init__(self, name, level):
        self.level = random.randrange(level, level+2)
        if self.level < 1:
            self.level = 1
        self.name = name
        if self.name in enemyScr.pEnemies:
            self.poison = True
        else:
            self.poison = False
        if self.name in enemyScr.dEnemies:
            self.damned = True
        else:
            self.damned = False
        self.maxHP = random.randrange(enemyScr.healthDict[self.name] - 5,
            enemyScr.healthDict[self.name] + 5)
        self.baseAttack = enemyScr.attackDict[self.name]
        self.currHP = self.maxHP

    def getLevel(self):
        return self.level

    def getHP(self):
        return self.currHP

    def getMaxHP(self):
        return maxHP

    def getName(self):
        return self.name

    def getBaseAttack(self):
        return self.baseAttack

    def takeDmg(self, dmg):
        if dmg:
            self.currHP -= dmg
