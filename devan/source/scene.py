

class CScene():

    # constructor
    def __init__(self, loader, parent):

        self.__model = loader.loadModel("models/environment")

        self.__model.reparentTo(parent)
        self.__model.setScale(0.25, 0.25, 0.25)
        self.__model.setPos(-8, 42, 0)


    # model getter
    def getModel(self):
        return self.__model