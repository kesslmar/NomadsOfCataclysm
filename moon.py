


class Moon():
    def __init__(self, world, name, model_path, texture, orbit_root, 
             scale, distance, athmosphere, wind, rescources):

        self.world = world
        self.name = name
        self.scale = scale
        self.distance = distance
        self.athmosphere = athmosphere
        self.wind = wind
        self.rescources = rescources

        self.energy_cap = 0
        self.energy_usg = 0
        self.population = 0
        self.habitation_cap = 0
        self.probed = False
        self.colonised = False
        self.goods = {}
        self.messages = {}
        self.slots = {
                'RESC':{'1':None, '2':None, '3':None, '4':None, '5':None},
                'PROD':{'1':None, '2':None, '3':None, '4':None, '5':None},
                'ENRG':{'1':None, '2':None, '3':None, '4':None, '5':None},
                'DEV': {'1':None, '2':None, '3':None, '4':None, '5':None},
                'HAB': {'1':None, '2':None, '3':None, '4':None, '5':None}
            }

        self.model = loader.loadModel(model_path)
        self.model.setTexture(loader.loadTexture(texture), 1)
        self.model.reparentTo(orbit_root)
        self.model.setPos(distance * world.orbitscale, 0, 0)
        self.model.setScale(scale * world.sizescale)
        self.model.setTag('clickable', 'yes')
        self.model.setPythonTag('instance', self)

        world.galaxy_objects.append(self)

    def getPos(self):
        return self.model.getPos(base.render)