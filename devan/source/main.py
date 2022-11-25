from panda3d.core import loadPrcFile
from panda3d.core import *
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
import os, sys

# configuration file location
loadPrcFile("config/config.prc")


# our game class
class CGame(ShowBase):

    # constructor
    def __init__(self):
        ShowBase.__init__(self)

        # get current python file location
        self.cur_dir = os.path.abspath(sys.path[0])
        # convert to panda's specific notation
        self.cur_dir = Filename.fromOsSpecific(self.cur_dir).getFullpath()

        #self.disableMouse()
        #self.camera.setPos(0, -30, 0)





# main function
def main():
    # create an object for the game and run it
    game = CGame()
    game.run()


# main entry point
if __name__ == '__main__':
    main()
