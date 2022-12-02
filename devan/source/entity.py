class CEntity():

    # constructor
    def __init__(self, loader, parent, model_path):

        # load model file
        self.__model = loader.loadModel(model_path)

        # reparent entity
        self.__model.reparentTo(parent)

        # entity speed
        self.__speed = 50.0

    # model getter
    def getModel(self):
        return self.__model

    # position getter
    def getPosition(self):
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
    def setPosition(self, x, y, z):
        self.__model.setPos(x, y, z)

    # set model rotation (H = heading, p = pitch, r = roll)
    def setRotation(self, H, p, r):
        self.__model.setHpr(H, p, r)