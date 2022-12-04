from entity import CEntity

# subclass of entity
class CPlayer(CEntity):

    # constructor
    def __init__(self, loader, parent, path):

        super().__init__(loader, parent, path)

        # target is a simple abstraction to help "smoother" player's movements
        self.__target_x = 0.0
        self.__target_y = 0.0
        self.__target_z = 0.0

        self.__target_distance = 20.0

    # get target position
    def getTargetPos(self):
        return [self.__target_x, self.__target_y, self.__target_z]

    # get target position
    def getTargetDist(self):
        return self.__target_distance

    # set target position
    def setTargetPos(self, x, y, z):
        self.__target_x = x
        self.__target_y = y
        self.__target_z = z

    # set target distance
    def setTargetDist(self, d):
        self.__target_distance = d