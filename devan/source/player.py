from entity import CEntity

# subclass of entity
class CPlayer(CEntity):

    # constructor
    def __init__(self, loader, parent, path):

        super().__init__(loader, parent, path + "/../resources/cat_rigged.fbx")