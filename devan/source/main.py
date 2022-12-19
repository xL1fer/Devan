import random

from panda3d.core import loadPrcFile
from panda3d.core import *
from panda3d.physics import *

from direct.showbase.ShowBase import ShowBase
from direct.task import Task

import os, sys
import math

from entity import CEntity
from animating import CAnimating
from player import CPlayer

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

        # initialize settings     #########
        self.settingsInitializer()

        # initialize materials    #########
        my_material = Material()
        my_material.setShininess(5.0) # Make this material shiny
        my_material.setAmbient((0, 0, 1, 1)) # Make this material blue
        my_material.setSpecular((0, 0, 1, 1))
        my_material.setDiffuse((0, 0, 1, 1))
        my_material.setEmission((0, 0, 1, 1))

        # initialize entities     #########

        #########################
        # Environment           #
        #########################

        # create scene floor entity
        """
        self.scene = CEntity(self.loader, self.render, self.cur_dir + "/../resources/cube.gltf")
        self.scene.setScale(1010.0, 1010.0, 0.1)
        self.scene.setColor(0.2, 1.0, 0.6, 1.0)
        """

        # loading grass / scene floor
        """grass_texture = self.loader.loadTexture(self.cur_dir + "/../resources/grass.jpg")
        self.grass = CEntity(self.loader, self.render, self.cur_dir + "/../resources/grass.obj", grass_texture)
        self.grass.setScale(6.75, 6.75, 0.75)
        self.grass.setPos(0, 0, -3.25)"""

        self.grass = CEntity(self.loader, self.render, self.cur_dir + "/../resources/grass.gltf")
        self.grass.setScale(6.75, 6.75, 1.0)
        self.grass.setPos(0, 0, -3.25)


        # card box entity
        self.box = CEntity(self.loader, self.render, self.cur_dir + "/../resources/box.gltf")
        self.box.setPos(-1050, -1050, 15)
        self.box.setRotation(70.0, 70.0, 0.0)
        self.box.setScale(2000.0, 2000.0, 2000.0)

        # dumpster entity
        self.box = CEntity(self.loader, self.render, self.cur_dir + "/../resources/dumpster.gltf")
        self.box.setPos(-1080, -900, 0)
        self.box.setRotation(70.0, 0.0, 0.0)
        self.box.setScale(40.0, 40.0, 40.0)

        # spawning some bushes and trees
        self.trees_ud = list()  # upper diagonal
        self.trees_ld = list()  # lower diagonal

        # trees node
        self.trees_node = NodePath("TreesNode")
        self.trees_node.reparentTo(self.render)
        
        for z in range(10):  # divide both diagonals in 10 'divs'
            self.trees_ud.append([])
            self.trees_ld.append([])

            # bushes
            for i in range((z * 2) + 1):
                # upper diagonal
                y_bush = random.randint(-900 + z * 200, -800 + z * 200)
                x_bush = random.randint(-1000, y_bush - 100)
                while True:  # checking distances
                    flag = False
                    for t in self.trees_ud[-1]:
                        dist = math.dist(t[0:2], (x_bush, y_bush))
                        if dist <= 50:
                            flag = True
                            break

                    if flag:
                        y_bush = random.randint(-900 + z * 200, -800 + z * 200)
                        x_bush = random.randint(-1000, y_bush - 100)
                    else:
                        break

                bush_texture = self.loader.loadTexture(self.cur_dir + "/../resources/textures/leaf.jpg")
                bush = CEntity(self.loader, self.render, self.cur_dir + "/../resources/bush.gltf", bush_texture)
                bush.setScale(6.0, 6.0, 6.0)
                bush.setPos(x_bush, y_bush, 1)
                self.trees_ud[-1].append((x_bush, y_bush, 0))


                # lower diagonal
                y_bush2 = random.randint(800 - z * 200, 900 - z * 200)
                x_bush2 = random.randint(y_bush2 + 100, 1000)
                while True:  # checking distances
                    flag = False
                    for t in self.trees_ld[-1]:
                        dist = math.dist(t[0:2], (x_bush2, y_bush2))
                        if dist <= 50:
                            flag = True
                            break

                    if flag:
                        y_bush2 = random.randint(800 - z * 200, 900 - z * 200)
                        x_bush2 = random.randint(y_bush2 + 100, 1000)
                    else:
                        break

                bush_texture = self.loader.loadTexture(self.cur_dir + "/../resources/textures/leaf.jpg")
                bush = CEntity(self.loader, self.render, self.cur_dir + "/../resources/bush.gltf", bush_texture)
                bush.setScale(6.0, 6.0, 6.0)
                bush.setPos(x_bush2, y_bush2, 0)
                self.trees_ld[-1].append((x_bush2, y_bush2, 0))

            # spawning a different number of tress considering the length of each 'div'
            if z > 7:
                ind = 4
            elif z > 4:
                ind = 2
            else:
                ind = 1

            # trees
            for i in range(ind):
                # upper diagonal
                y_tree = random.randint(-900 + z * 200, -800 + z * 200)
                x_tree = random.randint(-1000, y_tree - 100)
                while True:
                    flag = False
                    for t in self.trees_ud[z]:  # check distance in current 'div'
                        dist = math.dist(t[0:2], (x_tree, y_tree))
                        if t[2] == 0 and dist <= 50:
                            flag = True
                            break
                        if t[2] == 1 and dist <= 150:
                            flag = True
                            break
                    for t in self.trees_ud[z - 1]:  # check distance in previous 'div'
                        dist = math.dist(t[0:2], (x_tree, y_tree))
                        if t[2] == 0 and dist <= 50:
                            flag = True
                            break
                        if t[2] == 1 and dist <= 150:
                            flag = True
                            break

                    if flag:
                        y_tree = random.randint(-900 + z * 200, -800 + z * 200)
                        x_tree = random.randint(-1000, y_tree - 100)
                    else:
                        break

                tree = CEntity(self.loader, self.trees_node, self.cur_dir + "/../resources/tree.gltf")
                tree.setScale(1.0, 1.0, 1.0)
                tree.setPos(x_tree, y_tree, 15)
                self.trees_ud[z].append((x_tree, y_tree, 1))


                # lower diagonal
                y_tree = random.randint(800 - z * 200, 900 - z * 200)
                x_tree = random.randint(y_tree + 100, 1000)
                while True:
                    flag = False
                    for t in self.trees_ld[z]:  # check distance in current 'div'
                        dist = math.dist(t[0:2], (x_tree, y_tree))
                        if t[2] == 0 and dist <= 50:
                            flag = True
                            break
                        if t[2] == 1 and dist <= 150:
                            flag = True
                            break
                    for t in self.trees_ld[z - 1]:  # check distance in previous 'div'
                        dist = math.dist(t[0:2], (x_tree, y_tree))
                        if t[2] == 0 and dist <= 50:
                            flag = True
                            break
                        if t[2] == 1 and dist <= 150:
                            flag = True
                            break

                    if flag:
                        y_tree = random.randint(800 - z * 200, 900 - z * 200)
                        x_tree = random.randint(y_tree + 100, 1000)
                    else:
                        break

                tree = CEntity(self.loader, self.trees_node, self.cur_dir + "/../resources/tree.gltf")
                tree.setScale(1.0, 1.0, 1.0)
                tree.setPos(x_tree, y_tree, 15)
                self.trees_ld[z].append((x_tree, y_tree, 1))


        #########################
        # Player                #
        #########################

        # create player instance
        self.player = CPlayer(self.render, self.cur_dir + "/../resources/cat.gltf")
        self.player.getModel().setMaterial(my_material) # Apply the material to this nodePath
        self.player.setTargetPos(-1000 + self.player.getTargetDist(), -1000, 30)
        self.player.setScale(80, 80, 80)
        self.player.setPos(-1000, -1000, 5)
        self.player.setSpeed(180.0)

        # self.player.setAnimRate("run", 1.7)
        self.player.setAnimRate("idle", 0.7)
        self.player.getModel().loop("idle", fromFrame=1, toFrame=36)


        # small particle around player
        self.particle = CEntity(self.loader, self.player.getModel(), self.cur_dir + "/../resources/cube.gltf")
        self.particle.setScale(0.005, 0.005, 0.005)
        self.particle_radius = 0.4
        self.particle_height = self.player.getPos().z / 20
        self.particle_height_increment = 0.0001
        self.particle.setPos(0, -self.particle_radius / 2, self.particle_height)
        self.particle.setColor(1.0, 0.0, 0.0, 1)

        """
        # auxiliar target visualization
        self.target = CEntity(self.loader, self.actor_node_physics, self.cur_dir + "/../resources/cube.gltf")
        self.target.setPos(self.player.getTargetDist(), 0, 30)
        self.target.setColor(0.8, 0.0, 0.0, 1.0)
        self.target.setSpeed(80.0)
        """

        # tasks     #######################

        self.taskMgr.add(self.keyboardTask, "KeyboardTask")
        self.taskMgr.add(self.cameraTask, "CameraTask")
        self.taskMgr.add(self.globalTask, "GlobalTask")

        # lights    #######################

        # ambient light
        self.alight = AmbientLight('alight')
        self.alight.setColor((0.3, 0.3, 0.3, 1))
        self.alnp = self.render.attachNewNode(self.alight)
        self.render.setLight(self.alnp)

        # directional light (simulates the sun)
        self.sun_direction = -60  # 90
        self.sun_speed = 50.0
        self.dlight = DirectionalLight('dlight')
        # self.dlight.setColor((0.8, 0.8, 0.5, 1))
        self.dlight.setColor((0.8, 0.8, 0.6, 1))
        self.dlnp = self.render.attachNewNode(self.dlight)
        self.dlnp.setHpr(0, self.sun_direction, 0)
        self.render.setLight(self.dlnp)

        # shaders    ######################

        self.shader1 = Shader.load(
                                Shader.SL_GLSL,
                                vertex = self.cur_dir + "/shaders/perfragment.vert",
                                fragment = self.cur_dir + "/shaders/perfragment.frag"
                            )
        self.player.getModel().setShader(self.shader1)


    def settingsInitializer(self):
        #########################
        # Folder Directory      #
        #########################

        # get current python file location
        self.cur_dir = os.path.abspath(sys.path[0])
        # convert to panda's specific notation
        self.cur_dir = Filename.fromOsSpecific(self.cur_dir).getFullpath()

        # self.disableMouse()

        #########################
        # Physics               #
        #########################

        # NOTE: NOT WORKING YET !!!!!

        # enable particle system in order to use Physics
        base.enableParticles()

        self.physics_node = NodePath("PhysicsNode")
        self.physics_node.reparentTo(self.render)
        self.actor_node = ActorNode("test-physics")
        self.actor_node_physics = self.physics_node.attachNewNode(self.actor_node)
        base.physicsMgr.attachPhysicalNode(self.actor_node)
        # jetpackGuy = loader.loadModel("models/jetpack_guy")
        # jetpackGuy.reparentTo(anp)

        self.actor_node.getPhysicsObject().setMass(136.077)

        #########################
        # Key Events Mapping    #
        #########################

        self.accept("w", self.updateKeyMap, ["w", True])
        self.accept("w-up", self.updateKeyMap, ["w", False])

        self.accept("a", self.updateKeyMap, ["a", True])
        self.accept("a-up", self.updateKeyMap, ["a", False])

        self.accept("s", self.updateKeyMap, ["s", True])
        self.accept("s-up", self.updateKeyMap, ["s", False])

        self.accept("d", self.updateKeyMap, ["d", True])
        self.accept("d-up", self.updateKeyMap, ["d", False])

        self.accept("c", self.updateKeyMap, ["c", True])
        self.accept("c-up", self.updateKeyMap, ["c", False])

        self.accept("space", self.updateKeyMap, ["space", True])
        self.accept("space-up", self.updateKeyMap, ["space", False])

        #########################
        # Misc                  #
        #########################

        # Camera
        self.camera_mode = THIRDPERSONMODE
        self.camera_heading = 0
        self.camera_pitch = 0
        self.camera_speed = 2

    # update key state
    def updateKeyMap(self, key, state):
        key_map[key] = state

        if (self.camera_mode == THIRDPERSONMODE):
            if (key_map["w"] or key_map["a"] or key_map["s"] or key_map["d"]) and not self.player.isMoving():
                self.player.setMoving(True)
                # print(self.player.isMoving())
                self.player.animationBlend("idle", "run", 1, 36, 2.0)

            elif (not key_map["w"] and not key_map["a"] and not key_map["s"] and not key_map[
                "d"]) and self.player.isMoving():
                self.player.setMoving(False)
                # print(self.player.isMoving())
                self.player.animationBlend("run", "idle", 1, 36, 0.7)

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
                    self.player.animationBlend("run", "idle", 1, 36, 0.7)
                    
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

        self.player.getModel().set_shader_input("cameraPosition", self.camera.getPos())

        return task.cont

    # keyboard tasks
    def keyboardTask(self, task):
        dt = globalClock.getDt()

        target_pos = self.player.getTargetPos()
        player_pos = self.player.getPos()
        camera_pos = self.camera.getPos()

        distance = math.sqrt((target_pos[0] - player_pos[0]) ** 2 + (target_pos[1] - player_pos[1]) ** 2)
        # print(distance)

        # TODO: finish cat looking at target

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
        if self.particle_height < 0.12 or self.particle_height > 0.18:
            self.particle_height_increment *= -1

        angle_degrees = task.time * 20.0
        angle_radians = angle_degrees * (math.pi / 180.0)
        self.particle.setPos((self.particle_radius / 8) * math.sin(angle_radians),
                             (-self.particle_radius / 2) - (self.particle_radius / 8) * math.cos(angle_radians),
                             self.particle_height)

        # transparency task       #########
        camera_pos = self.camera.getPos()
        for tree in self.trees_node.getChildren():
            tree_pos = tree.getPos()
            distance = math.sqrt((tree_pos[0] - camera_pos[0]) ** 2 + (tree_pos[1] - camera_pos[1]) ** 2)

            if (distance < 250):
                tree.setAlphaScale(0.3)
            else:
                tree.setAlphaScale(1.0)

        return task.cont


# main function
def main(args):
    # create an object for the game and run it
    game = CGame()
    game.run()


# main entry point
if __name__ == '__main__':
    sys.exit(main(sys.argv))
