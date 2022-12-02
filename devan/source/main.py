from panda3d.core import loadPrcFile
from panda3d.core import *
from panda3d.physics import *

from direct.showbase.ShowBase import ShowBase
from direct.task import Task

import os, sys
import math

from entity import CEntity
from player import CPlayer

# configuration file location
loadPrcFile("config/config.prc")

# camera modes definitions
FREEROAMINGMODE = True     # free roaming
THIRDPERSONMODE = False     # third person

# keys mapping
key_map = {
    "up": False,
    "down": False,
    "left": False,
    "right": False,
    "camera_mode": False
}


# game class
class CGame(ShowBase):

    # constructor
    def __init__(self):
        ShowBase.__init__(self)

        # initialize settings
        self.settingsInitializer()

        # create scene floor
        self.scene = CEntity(self.loader, self.actor_node_physics, self.cur_dir + "/../resources/cube.obj")
        self.scene.setScale(200.0, 200.0, 0.1)
        self.scene.setColor(0.2, 1.0, 0.6, 1.0)

        # create player instance
        self.player = CPlayer(self.loader, self.actor_node_physics, self.cur_dir + "/../resources/cat_rigged.obj")
        self.player.setScale(0.8, 0.8, 0.8)
        self.player.setPosition(0, 0, 15)
        self.player.setRotation(0, 90, 0)

        # create tasks
        self.taskMgr.add(self.keyboardTask, "KeyboardTask")
        self.taskMgr.add(self.cameraTask, "CameraTask")


    def settingsInitializer(self):
        #########################
        # Folder Directory      #
        #########################

        # get current python file location
        self.cur_dir = os.path.abspath(sys.path[0])
        # convert to panda's specific notation
        self.cur_dir = Filename.fromOsSpecific(self.cur_dir).getFullpath()

        #self.disableMouse()

        #########################
        # Physics               #
        #########################

        # NOTE: NOT WORKING YET !!!!!

        # enable particle system in order to use Physics
        base.enableParticles()

        self.physics_node = NodePath("PhysicsNode")
        self.physics_node.reparentTo(self.render)
        self.actor_node = ActorNode("jetpack-guy-physics")
        self.actor_node_physics = self.physics_node.attachNewNode(self.actor_node)
        base.physicsMgr.attachPhysicalNode(self.actor_node)
        #jetpackGuy = loader.loadModel("models/jetpack_guy")
        #jetpackGuy.reparentTo(anp)
        
        self.actor_node.getPhysicsObject().setMass(136.077)

        #########################
        # Key Events Mapping    #
        #########################

        self.accept("w", self.updateKeyMap, ["up", True])
        self.accept("w-up", self.updateKeyMap, ["up", False])

        self.accept("a", self.updateKeyMap, ["left", True])
        self.accept("a-up", self.updateKeyMap, ["left", False])

        self.accept("s", self.updateKeyMap, ["down", True])
        self.accept("s-up", self.updateKeyMap, ["down", False])

        self.accept("d", self.updateKeyMap, ["right", True])
        self.accept("d-up", self.updateKeyMap, ["right", False])

        self.accept("c", self.updateKeyMap, ["camera_mode", True])
        self.accept("c-up", self.updateKeyMap, ["camera_mode", False])


        #########################
        # Misc                  #
        #########################

        self.camera_mode = THIRDPERSONMODE


    # update key state
    def updateKeyMap(self, key, state):
        key_map[key] = state


    # camera task
    def cameraTask(self, task):

        if (self.camera_mode == THIRDPERSONMODE):
            player_position = self.player.getPosition()
            # camera position
            self.camera.setPos(player_position[0], player_position[1] - 500, player_position[2] + 150)
            # camera looking at player
            self.camera.lookAt(player_position)

        elif (self.camera_mode == FREEROAMINGMODE):
            
            pass

        return task.cont


    # keyboard tasks
    def keyboardTask(self, task):
        dt = globalClock.getDt()

        player_pos = self.player.getPosition()
        camera_pos = self.camera.getPos()

        if key_map["up"]:
            if (self.camera_mode == THIRDPERSONMODE):
                player_pos.y += self.player.getSpeed() * dt
            elif (self.camera_mode == FREEROAMINGMODE):
                pass
        if key_map["left"]:
            if (self.camera_mode == THIRDPERSONMODE):
                player_pos.x -= self.player.getSpeed() * dt
                pass
            elif (self.camera_mode == FREEROAMINGMODE):
            
                pass
        if key_map["down"]:
            if (self.camera_mode == THIRDPERSONMODE):
                player_pos.y -= self.player.getSpeed() * dt
            elif (self.camera_mode == FREEROAMINGMODE):
            
                pass
        if key_map["right"]:
            if (self.camera_mode == THIRDPERSONMODE):
                player_pos.x += self.player.getSpeed() * dt
            elif (self.camera_mode == FREEROAMINGMODE):
            
                pass
        if key_map["camera_mode"]:
            key_map["camera_mode"] = False  # make camera mode only change once per button press
            self.camera_mode = not self.camera_mode

        self.player.setPosition(player_pos.x, player_pos.y, player_pos.z)

        return task.cont


# main function
def main(args):
    # create an object for the game and run it
    game = CGame()
    game.run()


# main entry point
if __name__ == '__main__':
    sys.exit(main(sys.argv))
