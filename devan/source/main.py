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

        # create scene instance
        self.scene = CEntity(self.loader, self.render, self.cur_dir + "/../resources/cube.obj")

        self.scene.getModel().setScale(150.0, 150.0, 0.1)

        self.scene.getModel().setColor(0.2, 1.0, 0.6, 1.0)

        # create player instance
        self.player = CPlayer(self.loader, self.render, self.cur_dir)

# main function
def main():
    # create an object for the game and run it
    game = CGame()
    game.run()


# main entry point
if __name__ == '__main__':
    main()
