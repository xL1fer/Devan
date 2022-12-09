from direct.actor.Actor import Actor

from entity import CEntity

class CAnimating(CEntity):

    # constructor
    def __init__(self, parent, model_path):

        self.__model = Actor(model_path)    # load animation model file
        self.__model.reparentTo(parent)     # reparent entity
        self.__speed = 50.0                 # entity speed
        self.__moving = False               # movement status

    # model getter
    def getModel(self):
        return self.__model

    # position getter
    def getPosition(self):
        return self.__model.getPos()

    # is moving
    def isMoving(self):
        return self.__moving

    # set model scale
    def setScale(self, sx, sy, sz):
        self.__model.setScale(sx, sy, sz)

    # set model position
    def setPos(self, x, y, z):
        self.__model.setPos(x, y, z)

    # set model rotation (y = yaw, p = pitch, r = roll)
    def setRotation(self, y, p, r):
        self.__model.setHpr(y, p, r)

    # set moving
    def setMoving(self, moving):
        self.__moving = moving

    # set animatio rate
    def setAnimRate(self, animation, rate):
        self.__model.setPlayRate(rate, animation)