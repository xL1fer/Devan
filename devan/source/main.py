from panda3d.core import loadPrcFile
from panda3d.core import *
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
import os, sys

from scene import CScene
from entity import CEntity
from player import CPlayer

# configuration file location
loadPrcFile("config/config.prc")


# our game class
class CGame(ShowBase):

    # constructor
    def __init__(self):
        ShowBase.__init__(self)

        # get current python file location
        self.cur_dir = os.path.abspath(sys.path[0])
        print(self.cur_dir)
        # convert to panda's specific notation
        self.cur_dir = Filename.fromOsSpecific(self.cur_dir).getFullpath()
        print(self.cur_dir)

        #self.disableMouse()
        #self.camera.setPos(0, -30, 0)

        # load scene model
        self.scene = CScene(self.loader, self.render)

        # create player instance
        self.player = CPlayer(self.loader, self.scene.getModel(), self.cur_dir)

        panda = self.loader.loadModel("models/panda")
        panda.setPos(-2,10,0)
        panda.setScale(0.2, 0.2, 0.2)
        panda.reparentTo(self.render)

# main function
def main():
    # create an object for the game and run it
    game = CGame()
    game.run()


# main entry point
if __name__ == '__main__':
    main()
