

class CEntity():

    # constructor
    def __init__(self, loader, parent, model_path):

        # load model file
        self.__model = loader.loadModel(model_path)

        # reparent entity
        self.__model.reparentTo(parent)


    # model getter
    def getModel(self):
        return self.__model