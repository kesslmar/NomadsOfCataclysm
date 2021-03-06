from panda3d.core import *


class Star():

    def __init__(self, world, name, model_path, texture, scale):

        self.world = world
        self.name = name
        self.scale = scale

        self.model = loader.loadModel(model_path)
        self.model.setTexture(loader.loadTexture(texture), 1)
        self.model.reparentTo(render)
        self.model.setScale(scale * world.sizescale)
        self.model.setTag('clickable', 'yes')
        self.model.setPythonTag('instance', self)

        self.light = PointLight('starlight')
        self.lightpath = self.model.attachNewNode(self.light)
        self.lightpath.setPos(0, 0, 0)
        self.light.setColorTemperature(5000)
        render.setLight(self.lightpath)
        self.model.clearLight(self.lightpath)

        world.galaxy_objects.append(self)

    def getPos(self):
        return self.model.getPos(base.render)
