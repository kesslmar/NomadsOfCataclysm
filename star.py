


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

        world.galaxy_objects.append(self)

    def getPos(self):
        return self.model.getPos(base.render)