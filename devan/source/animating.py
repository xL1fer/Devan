from direct.actor.Actor import Actor
from direct.interval.ActorInterval import LerpAnimInterval

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
    def getPos(self):
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

    # set model material
    def setMaterial(self, material, override=1):
        self.__model.setMaterial(material, override)

    # set model shader
    def setShader(self, shader):
        self.__model.setShader(shader)

    # set model shader input
    def setShaderInput(self, key, value):
        self.__model.setShaderInput(key, value)

    # set moving
    def setMoving(self, moving):
        self.__moving = moving

    # set animatio rate
    def setAnimRate(self, animation, rate):
        self.__model.setPlayRate(rate, animation)

    def setAnimLoop(self, animation, startFrame, endFrame):
        self.__model.loop(animation, fromFrame=startFrame, toFrame=endFrame)

    # animations blending
    def setAnimBlend(self, from_anim, to_anim, from_frame=1, to_frame=36,  rate=1, part=None):
        self.__model.enableBlend()
        self.__model.loop(to_anim, partName=part, fromFrame=from_frame, toFrame=to_frame)
        self.__model.setPlayRate(rate, to_anim, partName=part)
        interv = LerpAnimInterval(self.__model, 0.25, from_anim, to_anim, partName=part)
        interv.start()