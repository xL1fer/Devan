class CEntity():

    # constructor
    def __init__(self, loader, parent, model_path, texture):

        self.__model = loader.loadModel(model_path)     # load static model file
        self.__model.reparentTo(parent)                 # reparent entity
        self.__speed = 50.0                             # entity base speed

        if texture is not None:
            self.__model.setTexture(texture, 1)

    # model getter
    def getModel(self):
        return self.__model

    # position getter
    def getPos(self):
        return self.__model.getPos()

    # speed getter
    def getSpeed(self):
        return self.__speed

    # speed setter
    def setSpeed(self, speed):
        self.__speed = speed

    # set model scale
    def setScale(self, sx, sy, sz):
        self.__model.setScale(sx, sy, sz)

    # set model color
    def setColor(self, r, g, b, a):
        self.__model.setColor(r, g, b, a)

    # set model position
    def setPos(self, x, y, z):
        self.__model.setPos(x, y, z)

    # set model rotation (y = yaw, p = pitch, r = roll)
    def setRotation(self, y, p, r):
        self.__model.setHpr(y, p, r)