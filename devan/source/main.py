from panda3d.core import *

from direct.showbase.ShowBase import ShowBase
from direct.task import Task

import sys
import math

from initializer import CInitializer

# configuration file location
loadPrcFile("../config/config.prc")

# camera modes definitions
FREEROAMINGMODE = True  # free roaming
THIRDPERSONMODE = False  # third person

# keys mapping
key_map = {
    "w": False,
    "s": False,
    "a": False,
    "d": False,
    "c": False,
    "space": False
}


# game class
class CGame(ShowBase):

    # constructor
    def __init__(self):
        ShowBase.__init__(self)

        # initialize settings     ###########
        CInitializer.initSettings(self)

        # initialize materials     ##########
        CInitializer.initMaterials(self)

        # initialize shaders    #############
        CInitializer.initShaders(self)

        # initialize entities     ###########
        CInitializer.initEntities(self)

        # initialize lights    ##############
        CInitializer.initLights(self)

        # initialize tasks     ##############
        CInitializer.initTasks(self)


    # update key state
    def updateKeyMap(self, key, state):
        key_map[key] = state

        if (self.camera_mode == THIRDPERSONMODE):
            if (key_map["w"] or key_map["a"] or key_map["s"] or key_map["d"]) and not self.player.isMoving():
                self.player.setMoving(True)
                # print(self.player.isMoving())
                self.player.setAnimBlend("idle", "run", 1, 36, 2.0)

            elif (not key_map["w"] and not key_map["a"] and not key_map["s"] and not key_map[
                "d"]) and self.player.isMoving():
                self.player.setMoving(False)
                # print(self.player.isMoving())
                self.player.setAnimBlend("run", "idle", 1, 36, 0.7)

        if key_map["c"]:
            self.camera_mode = not self.camera_mode

            if (self.camera_mode == THIRDPERSONMODE):
                base.enableMouse()

                # hide mouse cursor
                props = WindowProperties()
                props.setCursorHidden(False)
                base.win.requestProperties(props)

            elif (self.camera_mode == FREEROAMINGMODE):
                # make sure animation does not play when in free roaming mode
                if self.player.isMoving():
                    self.player.setMoving(False)
                    self.player.setAnimBlend("run", "idle", 1, 36, 0.7)
                    
                player_position = self.player.getPos()
                self.camera.setPos(player_position[0], player_position[1], player_position[2] + 50)
                self.camera.setHpr(0, 0, 0)

                base.disableMouse()

                # hide mouse cursor
                props = WindowProperties()
                props.setCursorHidden(True)
                base.win.requestProperties(props)

        if key_map["space"]:
            self.camera_speed = 10
        else:
            self.camera_speed = 2

    # camera task
    def cameraTask(self, task):
        if (self.camera_mode == THIRDPERSONMODE):
            player_position = self.player.getPos()
            # camera position
            self.camera.setPos(player_position[0], player_position[1] - 500, player_position[2] + 150)
            # camera looking at player
            self.camera.lookAt(player_position)

        elif (self.camera_mode == FREEROAMINGMODE):
            # mouse look
            md = base.win.getPointer(0)

            x = md.getX()
            y = md.getY()

            if base.win.movePointer(0, 300, 300):
                self.camera_heading = self.camera_heading - (x - 300) * 0.2
                self.camera_pitch = self.camera_pitch - (y - 300) * 0.2

            self.camera.setHpr(self.camera_heading, self.camera_pitch, 0)

        return task.cont

    # keyboard tasks
    def keyboardTask(self, task):
        dt = globalClock.getDt()

        target_pos = self.player.getTargetPos()
        player_pos = self.player.getPos()
        camera_pos = self.camera.getPos()

        distance = math.sqrt((target_pos[0] - player_pos[0]) ** 2 + (target_pos[1] - player_pos[1]) ** 2)
        # print(distance)

        alpha1 = math.acos((target_pos[0] - player_pos[0]) / distance) * 180 / math.pi
        alpha2 = math.asin((target_pos[1] - player_pos[1]) / distance) * 180 / math.pi

        if alpha2 < 0:
            alpha = 360 - alpha1
        else:
            alpha = alpha1

        if (distance > self.player.getTargetDist()):
            player_pos[0] = target_pos[0] - math.cos(alpha * math.pi / 180) * self.player.getTargetDist()
            player_pos[1] = target_pos[1] - math.sin(alpha * math.pi / 180) * self.player.getTargetDist()

        if key_map["w"]:
            if (self.camera_mode == THIRDPERSONMODE):
                target_pos[1] += self.player.getSpeed() * dt
                # player_pos.y += self.player.getSpeed() * dt
            elif (self.camera_mode == FREEROAMINGMODE):
                self.camera.setY(base.cam, self.camera.getY(base.cam) + self.camera_speed)
        if key_map["a"]:
            if (self.camera_mode == THIRDPERSONMODE):
                target_pos[0] -= self.player.getSpeed() * dt
                # player_pos.x -= self.player.getSpeed() * dt
            elif (self.camera_mode == FREEROAMINGMODE):
                self.camera.setX(base.cam, self.camera.getX(base.cam) - self.camera_speed)
        if key_map["s"]:
            if (self.camera_mode == THIRDPERSONMODE):
                target_pos[1] -= self.player.getSpeed() * dt
                # player_pos.y -= self.player.getSpeed() * dt
            elif (self.camera_mode == FREEROAMINGMODE):
                self.camera.setY(base.cam, self.camera.getY(base.cam) - self.camera_speed)
        if key_map["d"]:
            if (self.camera_mode == THIRDPERSONMODE):
                target_pos[0] += self.player.getSpeed() * dt
                # player_pos.x += self.player.getSpeed() * dt
            elif (self.camera_mode == FREEROAMINGMODE):
                self.camera.setX(base.cam, self.camera.getX(base.cam) + self.camera_speed)

        self.player.setTargetPos(target_pos[0], target_pos[1], target_pos[2])
        self.player.setPos(player_pos.x, player_pos.y, player_pos.z)
        # look at the target cube
        self.player.setRotation(alpha, 0, 0)

        return task.cont

    def globalTask(self, task):
        # day and night cycle     #########
        dt = globalClock.getDt()
        self.sun_direction += self.sun_speed * dt

        if self.sun_direction > 360:
            self.sun_direction = 0

        self.dlnp.setHpr(0, self.sun_direction, 0)

        # particle task           #########
        self.particle_height += self.particle_height_increment
        if self.particle_height < self.player.getPos().z / 20 - 0.02 or self.particle_height > self.player.getPos().z / 20 + 0.02:
            self.particle_height_increment *= -1

        angle_degrees = task.time * 20.0
        angle_radians = angle_degrees * (math.pi / 180.0)
        self.particle.setPos((self.particle_radius / 8) * math.sin(angle_radians),
                             (-self.particle_radius / 2) - (self.particle_radius / 8) * math.cos(angle_radians),
                             self.particle_height)

        self.particle_rotation += 2
        if self.particle_rotation > 360:
            self.particle_rotation = 0

        self.particle.setRotation(self.particle_rotation, self.particle_rotation, 0)

        # transparency task       #########
        camera_pos = self.camera.getPos()
        for tree in self.trees_node.getChildren():
            tree_pos = tree.getPos()
            distance = math.sqrt((tree_pos[0] - camera_pos[0]) ** 2 + (tree_pos[1] - camera_pos[1]) ** 2)

            if (distance < 250):
                tree.setAlphaScale(0.3)
            else:
                tree.setAlphaScale(1.0)

        # skulls rotation task       ######
        player_pos = self.player.getPos()

        self.skulls_rotation += 0.5
        if (self.skulls_rotation > 360):
            self.skulls_rotation = 0

        self.skulls_height += self.skulls_height_increment
        if self.skulls_height < 5 or self.skulls_height > 30:
            self.skulls_height_increment *= -1

        for skull in self.skulls_node.getChildren():
            skull.setHpr(self.skulls_rotation, 0.0, 0.0)
            skull.setZ(self.skulls_height)
            skull_pos = skull.getPos()

            # collect skull
            distance = math.sqrt((skull_pos[0] - player_pos[0]) ** 2 + (skull_pos[1] - player_pos[1]) ** 2)
            if (distance < 40):
                skull.removeNode()

        return task.cont


# main function
def main(args):
    # create an object for the game and run it
    game = CGame()
    game.run()


# main entry point
if __name__ == '__main__':
    sys.exit(main(sys.argv))
