from direct.showbase.DirectObject import DirectObject
from panda3d.core import *
from direct.interval.IntervalGlobal import *

class CameraController(DirectObject):
    def	__init__(self):
        base.disableMouse()

        self.setupVars()
        self.setupCamera()
        self.setupInput()
        self.setupTasks()

    def setupVars(self):
        self.initZoom = 50			# Camera's initial distance from anchor
        self.zoomInLimit = 1		# Camera's minimum distance from anchor
        self.zoomOutLimit = 500     # Camera's maximum distance from anchor
        self.moveSpeed = .2			# Rate of movement for the anchor
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
        taskMgr.add(self.camera_move_task, "Camera Move")

    def setOrbit(self, orbit):
        if orbit:
            props = base.win.getProperties()
            winX = props.getXSize()
            winY = props.getYSize()
            if base.mouseWatcherNode.hasMouse():
                mX = base.mouseWatcherNode.getMouseX()
                mY = base.mouseWatcherNode.getMouseY()
                mPX = winX * ((mX + 1) / 2)
                mPY = winY * ((-mY + 1) / 2)
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
                if(newP < -90):
                    newP = -90
                if(newP > 90):
                    newP = 90

                if(newH < -180):
                    newH += 360
                if(newH > 180):
                    newH -= 360
                self.camAnchor.setHpr(newH, newP, 0)

        return task.cont

    def setZoom(self, zoom):
        if zoom == 'in':
            deltaY = -2
        elif zoom == 'out':
            deltaY = 2

        newY = (base.camera.getY() - deltaY)
        if(newY > -self.zoomInLimit):
            newY = -self.zoomInLimit
        if(newY < -self.zoomOutLimit):
            newY = -self.zoomOutLimit

        base.camera.setY(newY)

    def setMove(self, value, direction):
        self.move_dict.update({direction: value})

    def camera_move_task(self, task):
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

    def reset(self):
        anchorPos = self.camAnchor.getPos()
        anchorHpr = self.camAnchor.getHpr()

        taskMgr.remove('infocamTask')
        taskMgr.remove('buildcamTask')
        transition = Parallel(
            self.camAnchor.posInterval(0.2, Vec3(0, 0, 0), anchorPos),
            self.camAnchor.hprInterval(0.2, Vec3(0, -45, 0), anchorHpr),
            base.camera.posInterval(0.2, Vec3(0, -50, 0), base.camera.getPos())
        )
        transition.start()


    def info_view_to(self, obj):
        taskMgr.remove('buildcamTask')  # in case of coming from Build view
        transition = Sequence(
            Parallel(
                self.camAnchor.posInterval(
                    0.2, obj.getPos(), self.camAnchor.getPos()),
                self.camAnchor.hprInterval(
                    0.2, Vec3(0, -45, 0), self.camAnchor.getHpr()),
                base.camera.posInterval(
                    0.2, Vec3(-1.22 * obj.scale, -5.5 * obj.scale, 0), base.camera.getPos())
            ),
            Func(self._add_follow_cam, 'info', obj)
        )
        transition.start()

    def build_view_to(self, obj):
        taskMgr.remove('infocamTask')
        transition = Sequence(
            Parallel(
                self.camAnchor.posInterval(
                    0.2, obj.getPos(), self.camAnchor.getPos()),
                self.camAnchor.hprInterval(
                    0.2, Vec3(0, 0, 0), self.camAnchor.getHpr()),
                base.camera.posInterval(
                    0.2, Vec3(-0.9 * obj.scale, -3.4 * obj.scale, 0), base.camera.getPos())
            ),
            Func(self._add_follow_cam, 'build', obj)
        )
        transition.start()

    def _add_follow_cam(self, mode, obj):
        taskMgr.add(
                self._follow_cam_task,
                'infocamTask',
                extraArgs=[obj, obj.scale, mode],
                appendTask=True
        )

    def _follow_cam_task(self, obj, scale, mode, task):
        pos = obj.getPos()

        if mode == 'info':
            self.camAnchor.setPos(pos)
            self.camAnchor.setHpr(0, -45, 0)
            base.camera.setPos(-1.22 * scale, -5.5 * scale, 0)
        if mode == 'build':
            self.camAnchor.setPos(pos)
            self.camAnchor.setHpr(0, 0, 0)
            base.camera.setPos(-.9 * scale, -3.4 * scale, 0)
        return task.cont
