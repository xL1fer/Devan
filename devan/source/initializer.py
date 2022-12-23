from panda3d.core import *

import os
import sys
import random
import math

from entity import CEntity
from animating import CAnimating
from player import CPlayer

# camera modes definitions
FREEROAMINGMODE = True  # free roaming
THIRDPERSONMODE = False  # third person

class CInitializer():

    def __init__():
        pass

    def initSettings(game):
        #########################
        # Folder Directory      #
        #########################

        # get current python file location
        game.cur_dir = os.path.abspath(sys.path[0])
        # convert to panda's specific notation
        game.cur_dir = Filename.fromOsSpecific(game.cur_dir).getFullpath()

        # self.disableMouse()

        #########################
        # Key Events Mapping    #
        #########################

        game.accept("w", game.updateKeyMap, ["w", True])
        game.accept("w-up", game.updateKeyMap, ["w", False])

        game.accept("a", game.updateKeyMap, ["a", True])
        game.accept("a-up", game.updateKeyMap, ["a", False])

        game.accept("s", game.updateKeyMap, ["s", True])
        game.accept("s-up", game.updateKeyMap, ["s", False])

        game.accept("d", game.updateKeyMap, ["d", True])
        game.accept("d-up", game.updateKeyMap, ["d", False])

        game.accept("c", game.updateKeyMap, ["c", True])
        game.accept("c-up", game.updateKeyMap, ["c", False])

        game.accept("space", game.updateKeyMap, ["space", True])
        game.accept("space-up", game.updateKeyMap, ["space", False])

        #########################
        # Misc                  #
        #########################

        # Camera
        game.camera_mode = THIRDPERSONMODE
        game.camera_heading = 0
        game.camera_pitch = 0
        game.camera_speed = 2

    def initTasks(game):
        game.taskMgr.add(game.keyboardTask, "KeyboardTask")
        game.taskMgr.add(game.cameraTask, "CameraTask")
        game.taskMgr.add(game.globalTask, "GlobalTask")

    def initLights(game):
        # ambient light
        game.alight = AmbientLight('alight')
        game.alight.setColor((0.3, 0.3, 0.3, 1))
        game.alnp = game.render.attachNewNode(game.alight)
        game.render.setLight(game.alnp)

        # directional light (simulates the sun)
        game.sun_direction = -60  # 90
        game.sun_speed = 50.0
        game.dlight = DirectionalLight('dlight')
        # game.dlight.setColor((0.8, 0.8, 0.5, 1))
        game.dlight.setColor((0.8, 0.8, 0.6, 1))
        game.dlnp = game.render.attachNewNode(game.dlight)
        game.dlnp.setHpr(0, game.sun_direction, 0)
        game.render.setLight(game.dlnp)

    def initShaders(game):
        game.flatShading = Shader.load(
                                Shader.SL_GLSL,
                                vertex = game.cur_dir + "/shaders/pertriangle.vert",
                                fragment = game.cur_dir + "/shaders/pertriangle.frag"
                            )

        game.gouraudShading = Shader.load(
                                Shader.SL_GLSL,
                                vertex = game.cur_dir + "/shaders/pervertex.vert",
                                fragment = game.cur_dir + "/shaders/pervertex.frag"
                            )

        game.phongShading = Shader.load(
                                Shader.SL_GLSL,
                                vertex = game.cur_dir + "/shaders/perfragment.vert",
                                fragment = game.cur_dir + "/shaders/perfragment.frag"
                            )

    def initMaterials(game):
        game.test_material = Material()
        game.test_material.setShininess(10.0)
        game.test_material.setAmbient((1.0, 0.3, 0.3, 1))
        game.test_material.setSpecular((1.0, 0.3, 0.3, 1))
        game.test_material.setDiffuse((1.0, 0.3, 0.3, 1))

        game.blue_material = Material()
        game.blue_material.setShininess(10.0)
        game.blue_material.setAmbient((0.2, 0.2, 1.0, 1))
        game.blue_material.setSpecular((0.2, 0.2, 1.0, 1))
        game.blue_material.setDiffuse((0.2, 0.2, 1.0, 1))

    def initEntities(game):
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

        game.grass = CEntity(game.loader, game.render, game.cur_dir + "/../resources/grass.gltf")
        game.grass.setScale(6.75, 6.75, 1.0)
        game.grass.setPos(0, 0, -3.25)

        # card box entity
        game.box = CEntity(game.loader, game.render, game.cur_dir + "/../resources/box.gltf")
        game.box.setPos(-1050, -1050, 15)
        game.box.setRotation(70.0, 70.0, 0.0)
        game.box.setScale(2000.0, 2000.0, 2000.0)

        # dumpster entity
        game.box = CEntity(game.loader, game.render, game.cur_dir + "/../resources/dumpster.gltf")
        game.box.setPos(-1080, -900, 0)
        game.box.setRotation(70.0, 0.0, 0.0)
        game.box.setScale(40.0, 40.0, 40.0)

        # spawning some bushes and trees
        game.trees_ud = list()  # upper diagonal
        game.trees_ld = list()  # lower diagonal

        # trees node
        game.trees_node = NodePath("TreesNode")
        game.trees_node.reparentTo(game.render)
        
        for z in range(10):  # divide both diagonals in 10 'divs'
            game.trees_ud.append([])
            game.trees_ld.append([])

            # bushes
            for i in range((z * 2) + 1):
                # upper diagonal
                y_bush = random.randint(-900 + z * 200, -800 + z * 200)
                x_bush = random.randint(-1000, y_bush - 100)
                while True:  # checking distances
                    flag = False
                    for t in game.trees_ud[-1]:
                        dist = math.dist(t[0:2], (x_bush, y_bush))
                        if dist <= 50:
                            flag = True
                            break

                    if flag:
                        y_bush = random.randint(-900 + z * 200, -800 + z * 200)
                        x_bush = random.randint(-1000, y_bush - 100)
                    else:
                        break

                bush_texture = game.loader.loadTexture(game.cur_dir + "/../resources/textures/leaf.jpg")
                bush = CEntity(game.loader, game.render, game.cur_dir + "/../resources/bush.gltf", bush_texture)
                bush.setScale(6.0, 6.0, 6.0)
                bush.setPos(x_bush, y_bush, 1)
                game.trees_ud[-1].append((x_bush, y_bush, 0))


                # lower diagonal
                y_bush2 = random.randint(800 - z * 200, 900 - z * 200)
                x_bush2 = random.randint(y_bush2 + 100, 1000)
                while True:  # checking distances
                    flag = False
                    for t in game.trees_ld[-1]:
                        dist = math.dist(t[0:2], (x_bush2, y_bush2))
                        if dist <= 50:
                            flag = True
                            break

                    if flag:
                        y_bush2 = random.randint(800 - z * 200, 900 - z * 200)
                        x_bush2 = random.randint(y_bush2 + 100, 1000)
                    else:
                        break

                bush_texture = game.loader.loadTexture(game.cur_dir + "/../resources/textures/leaf.jpg")
                bush = CEntity(game.loader, game.render, game.cur_dir + "/../resources/bush.gltf", bush_texture)
                bush.setScale(6.0, 6.0, 6.0)
                bush.setPos(x_bush2, y_bush2, 0)
                game.trees_ld[-1].append((x_bush2, y_bush2, 0))

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
                    for t in game.trees_ud[z]:  # check distance in current 'div'
                        dist = math.dist(t[0:2], (x_tree, y_tree))
                        if t[2] == 0 and dist <= 50:
                            flag = True
                            break
                        if t[2] == 1 and dist <= 150:
                            flag = True
                            break
                    for t in game.trees_ud[z - 1]:  # check distance in previous 'div'
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

                tree = CEntity(game.loader, game.trees_node, game.cur_dir + "/../resources/tree.gltf")
                tree.setScale(1.0, 1.0, 1.0)
                tree.setPos(x_tree, y_tree, 15)
                game.trees_ud[z].append((x_tree, y_tree, 1))


                # lower diagonal
                y_tree = random.randint(800 - z * 200, 900 - z * 200)
                x_tree = random.randint(y_tree + 100, 1000)
                while True:
                    flag = False
                    for t in game.trees_ld[z]:  # check distance in current 'div'
                        dist = math.dist(t[0:2], (x_tree, y_tree))
                        if t[2] == 0 and dist <= 50:
                            flag = True
                            break
                        if t[2] == 1 and dist <= 150:
                            flag = True
                            break
                    for t in game.trees_ld[z - 1]:  # check distance in previous 'div'
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

                tree = CEntity(game.loader, game.trees_node, game.cur_dir + "/../resources/tree.gltf")
                tree.setScale(1.0, 1.0, 1.0)
                tree.setPos(x_tree, y_tree, 15)
                game.trees_ld[z].append((x_tree, y_tree, 1))


        #########################
        # Player                #
        #########################

        # create player instance
        game.player = CPlayer(game.render, game.cur_dir + "/../resources/cat.gltf")
        game.player.setMaterial(game.test_material) # Apply the material to this nodePath
        game.player.setTargetPos(-1000 + game.player.getTargetDist(), -1000, 30)
        game.player.setScale(80, 80, 80)
        game.player.setPos(-1000, -1000, 5)
        game.player.setSpeed(180.0)

        game.player.setShader(game.flatShading)
        game.player.setShaderInput("cameraPosition", game.camera.getPos())

        # game.player.setAnimRate("run", 1.7)
        game.player.setAnimRate("idle", 0.7)
        game.player.setAnimLoop("idle", 1, 36)

        # small particle around player
        game.particle = CEntity(game.loader, game.player.getModel(), game.cur_dir + "/../resources/cube.gltf")
        game.particle.setScale(0.008, 0.008, 0.008)
        game.particle_radius = 0.4
        game.particle_rotation = 0
        game.particle_height = game.player.getPos().z / 20
        game.particle_height_increment = 0.0001
        game.particle.setPos(0, -game.particle_radius / 2, game.particle_height)
        game.particle.setColor(1.0, 0.0, 0.0, 1)

        """
        # auxiliar target visualization
        game.target = CEntity(game.loader, game.render, game.cur_dir + "/../resources/cube.gltf")
        game.target.setPos(game.player.getTargetDist(), 0, 30)
        game.target.setColor(0.8, 0.0, 0.0, 1.0)
        game.target.setSpeed(80.0)
        """

        #########################
        # Misc                  #
        #########################
        game.skullsNode = NodePath("SkullsNode")
        game.skullsNode.reparentTo(game.render)
        game.skullsNode.setScale(0.5, 0.5, 0.5)
        game.skullsNode.setPos(5.0)

        game.skull1 = CEntity(game.loader, game.skullsNode, game.cur_dir + "/../resources/skull.obj")
        game.skull1.setPos(-35.0, 0.0, 0.0)
        game.skull1.setRotation(22.5, 0, 0)
        game.skull1.setShader(game.flatShading)
        game.skull1.setShaderInput("cameraPosition", game.camera.getPos())
        game.skull1.setMaterial(game.blue_material)

        game.skull2 = CEntity(game.loader, game.skullsNode, game.cur_dir + "/../resources/skull.obj")
        game.skull2.setPos(0.0, 35.0, 0.0)
        game.skull2.setShader(game.gouraudShading)
        game.skull2.setShaderInput("cameraPosition", game.camera.getPos())
        game.skull2.setMaterial(game.blue_material)

        game.skull3 = CEntity(game.loader, game.skullsNode, game.cur_dir + "/../resources/skull.obj")
        game.skull3.setPos(35.0, 0.0, 0.0)
        game.skull3.setRotation(-22.5, 0, 0)
        game.skull3.setShader(game.phongShading)
        game.skull3.setShaderInput("cameraPosition", game.camera.getPos())
        game.skull3.setMaterial(game.blue_material)