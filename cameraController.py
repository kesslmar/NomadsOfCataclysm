from direct.showbase.DirectObject import DirectObject
from pandac.PandaModules import *

class CameraController(DirectObject):
    def	__init__(self):
        base.disableMouse()

        self.setupVars()
        self.setupCamera()
        self.setupInput()
        self.setupTasks()

    def setupVars(self):
        self.initZoom = 5			#Camera's initial distance from anchor
        self.zoomInLimit = 1		#Camera's minimum distance from anchor
        self.zoomOutLimit = 1000	#Camera's maximum distance from anchor
        self.moveSpeed = .5			#Rate of movement for the anchor
        self.zoom = None
        self.orbit = None
        self.move = None
        self.move_dict = {
            'foreward': False,
            'back': False,
            'left': False,
            'right': False}

    def setupCamera(self):
        self.camAnchor = render.attachNewNode("Cam Anchor")
        base.camera.reparentTo(self.camAnchor)
        base.camera.setPos(0, -self.initZoom, 0)
        base.camera.lookAt(self.camAnchor)

    def setupInput(self):
        self.accept("wheel_up", self.setZoom, ['in'])
        self.accept("wheel_down", self.setZoom, ['out'])
        self.accept("mouse3", self.setOrbit, [True])
        self.accept("mouse3-up", self.setOrbit, [False])
        self.accept('w', self.setMove, [True, 'foreward'])
        self.accept('w-up', self.setMove, [False, 'foreward'])
        self.accept('s', self.setMove, [True, 'back'])
        self.accept('s-up', self.setMove, [False, 'back'])
        self.accept('a', self.setMove, [True, 'left'])
        self.accept('a-up', self.setMove, [False, 'left'])
        self.accept("d", self.setMove, [True, 'right'])
        self.accept('d-up', self.setMove, [False, 'right'])

    def setupTasks(self):
        taskMgr.add(self.cameraOrbit, "Camera Orbit")
        taskMgr.add(self.cameraZoom, "Camera Zoom")
        taskMgr.add(self.cameraMove, "Camera Move")

    def setOrbit(self, orbit):
        if(orbit == True):
            props = base.win.getProperties()
            winX = props.getXSize()
            winY = props.getYSize()
            if base.mouseWatcherNode.hasMouse():
                mX = base.mouseWatcherNode.getMouseX()
                mY = base.mouseWatcherNode.getMouseY()
                mPX = winX * ((mX+1)/2)
                mPY = winY * ((-mY+1)/2)
            self.orbit = [[mX, mY], [mPX, mPY]]
        else:
            self.orbit = None

    def cameraOrbit(self, task):
        if(self.orbit != None):
            if base.mouseWatcherNode.hasMouse():

                mpos = base.mouseWatcherNode.getMouse()

                base.win.movePointer(0, int(self.orbit[1][0]), int(self.orbit[1][1]))

                deltaH = 90 * (mpos[0] - self.orbit[0][0])
                deltaP = 90 * (mpos[1] - self.orbit[0][1])

                limit = .5

                if(-limit < deltaH and deltaH < limit):
                    deltaH = 0
                elif(deltaH > 0):
                    deltaH - limit
                elif(deltaH < 0):
                    deltaH + limit
                    
                if(-limit < deltaP and deltaP < limit):
                    deltaP = 0
                elif(deltaP > 0):
                    deltaP - limit
                elif(deltaP < 0):
                    deltaP + limit

                newH = (self.camAnchor.getH() + -deltaH)
                newP = (self.camAnchor.getP() + deltaP)
                if(newP < -90): newP = -90
                if(newP > 90): newP = 90
            
                self.camAnchor.setHpr(newH, newP, 0)				
            
        return task.cont
    
    def setZoom(self, zoom):
        if zoom == 'in':
            print('in')
            '''
            props = base.win.getProperties()
            winX = props.getXSize()
            winY = props.getYSize()
            if base.mouseWatcherNode.hasMouse():
                mX = base.mouseWatcherNode.getMouseX()
                mY = base.mouseWatcherNode.getMouseY()
                mPX = winX * ((mX+1)/2)
                mPY = winY * ((-mY+1)/2)
            self.zoom = [[mX, mY], [mPX, mPY]]
            '''
            self.zoom = -0.3
        elif zoom == 'out':
            print('out')
            self.zoom = 0.3
        
    def cameraZoom(self, task):
        if(self.zoom != None):
            if base.mouseWatcherNode.hasMouse():

                #mpos = base.mouseWatcherNode.getMouse()
                
                #base.win.movePointer(0, int(self.zoom[1][0]), int(self.zoom[1][1]))
                
                #deltaY = (mpos[1] - self.zoom[0][1]) * base.camera.getY()
                deltaY = self.zoom

                limit = .5
                
                if(-limit < deltaY and deltaY < limit):
                    deltaY = 0
                elif(deltaY > 0):
                    deltaY - limit
                elif(deltaY < 0):
                    deltaY + limit

                newY = (base.camera.getY() - deltaY)
                if(newY > -self.zoomInLimit): newY = -self.zoomInLimit
                if(newY < -self.zoomOutLimit): newY = -self.zoomOutLimit

                base.camera.setY(newY)				

        return task.cont

    def setMove(self, value, direction):
        self.move_dict.update({direction: value})

    def cameraMove(self, task):
        if self.move_dict['foreward']:
            self.camAnchor.setY(self.camAnchor, self.moveSpeed)
            self.camAnchor.setZ(0)
        if self.move_dict['back']:
            self.camAnchor.setY(self.camAnchor, -self.moveSpeed)
            self.camAnchor.setZ(0)
        if self.move_dict['left']:
            self.camAnchor.setX(self.camAnchor, -self.moveSpeed)
        if self.move_dict['right']:
            self.camAnchor.setX(self.camAnchor, self.moveSpeed)
        return task.cont
