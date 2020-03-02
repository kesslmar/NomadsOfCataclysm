from direct.showbase.DirectObject import DirectObject
from direct.gui.OnscreenImage import OnscreenImage
from panda3d.core import *
from direct.gui.DirectGui import DirectFrame, DirectScrolledFrame, DirectLabel, DGG


class ScrolledItemSelector(DirectObject):
    '''Touch optimised list that holds a set of items. By clicking on one you select it and return
    its Value with get_selected(). To add an item simply use add_item(). You can also pass a
    function with the 'command' field that gets called on a selection switch'''

    def __init__(self,
                 frame_size=(1, 1.5),
                 frame_color=(0.2, 0.2, 0.2, 0.8),
                 pos=(0, 0, 0),
                 item_v_padding=0.02,
                 item_h_padding=0.04,
                 item_scale=1,
                 item_side_ratio=0.2,
                 item_background=(0.3, 0.3, 0.3, 1),
                 item_background_active=(0.6, 0.6, 0.6, 1),
                 command=lambda: None
                 ):

        self.f_x, self.f_y = frame_size
        self.c_x = self.f_x
        self.c_y = self.f_y

        self.item_v_padding = item_v_padding
        self.item_h_padding = item_h_padding
        self.item_scale = item_scale
        self.item_background = item_background
        self.item_background_active = item_background_active

        self.frame = DirectScrolledFrame(
            frameSize=(-self.f_x / 2, self.f_x / 2, -self.f_y / 2, self.f_y / 2),
            canvasSize=(-self.c_x / 2, self.c_x / 2, -self.c_y / 2, self.c_y / 2),
            frameColor=frame_color,
            pos=pos,
            scrollBarWidth=(0),
            manageScrollBars=False,
            state=DGG.NORMAL)

        self.frame.verticalScroll.destroy()
        self.frame.horizontalScroll.destroy()
        self.frame.bind(DGG.WITHIN, self._start_listening)
        self.frame.bind(DGG.WITHOUT, self._stop_listening)

        self.canvas = self.frame.getCanvas()

        self.i_x = self.f_x * (1 - item_h_padding)
        self.i_y = self.f_y * item_side_ratio
        self.i_size = (-self.i_x / 2, self.i_x / 2, -self.i_y / 2, self.i_y / 2)

        self.i_start = self.c_y / 2 + self.i_y / 2

        self.active_item = None
        self.item_list = []
        self.value_list = []

        self.start_mY = None
        self.old_mY = None
        self.m_diff = 0
        self.is_scrolling = False
        self.command = command

        messenger.toggleVerbose()

    def _start_listening(self, watcher):
        print('start listening')
        self.accept("mouse1", self._start_scroll)
        self.accept("mouse1-up", self._stop_scroll)

    def _stop_listening(self, watcher):
        print('stop listening')
        self.ignore("mouse1")
        self.ignore("mouse1-up")
        self._stop_scroll()

    def _switch_active_item(self, item, watcher):
        if not self.is_scrolling:
            print('switched')
            if self.active_item is not None:
                self.active_item['frameColor'] = self.item_background
            item['frameColor'] = self.item_background_active
            self.active_item = item
            self.command()

    def _start_scroll(self):
        n = len(self.item_list)
        content_length = (
            (n * (self.i_y + self.item_v_padding)) +  # Size of all elements with padding
            self.item_v_padding)                   # Add one padding for the bottom

        if content_length > self.c_y:
            taskMgr.doMethodLater(0.01, self._scroll_task, 'scroll_task')
            self.start_mY = base.mouseWatcherNode.getMouse().getY()
            self.old_mY = self.start_mY

    def _stop_scroll(self):
        taskMgr.remove('scroll_task')
        taskMgr.doMethodLater(0.01, self._scroll_fade_task, 'scrollfadetask')
        self.is_scrolling = False

    def _scroll_task(self, task):
        mY = base.mouseWatcherNode.getMouse().getY()
        old_c = self.canvas.getZ()
        self.m_diff = self.old_mY - mY
        n = len(self.item_list)

        if self.m_diff != 0:
            self.is_scrolling = True

        self.c_scroll_start = 0
        self.c_scroll_stop = (
            (n * (self.i_y + self.item_v_padding)) +  # Size of all elements with padding
            self.item_v_padding -                   # Add one padding for the bottom
            self.f_y)                               # Substract the length of the canvas
        self.c_new_pos = (old_c - self.m_diff)

        hits_not_upper_bound = self.c_new_pos >= self.c_scroll_start
        hits_not_lower_bound = self.c_new_pos <= self.c_scroll_stop

        print('canvas : ' + str(self.canvas.getZ()))

        if hits_not_upper_bound and hits_not_lower_bound:
            self.canvas.setZ(self.c_new_pos)
        elif not hits_not_upper_bound:
            self.canvas.setZ(self.c_scroll_start)
        elif not hits_not_lower_bound:
            self.canvas.setZ(self.c_scroll_stop)

        self.old_mY = mY
        return task.again

    def _scroll_fade_task(self, task):
        if self.m_diff is None or abs(self.m_diff) < 0.005:
            self.m_diff = 0
            return task.done

        old_c = self.canvas.getZ()
        n = len(self.item_list)
        self.c_scroll_start = 0
        self.c_scroll_stop = (
            (n * (self.i_y + self.item_v_padding)) +  # Size of all elements with padding
            self.item_v_padding -                     # Add one padding for the bottom
            self.c_y)                                 # Substract the length of the canvas

        hits_not_upper_bound = (old_c - self.m_diff) >= self.c_scroll_start
        hits_not_lower_bound = (old_c - self.m_diff) <= self.c_scroll_stop

        if hits_not_upper_bound and hits_not_lower_bound:
            self.canvas.setZ(old_c - self.m_diff)
            self.m_diff *= 0.85
            return task.again
        elif not hits_not_upper_bound:
            self.canvas.setZ(self.c_scroll_start)
            self.m_diff = 0
            return task.done
        elif not hits_not_lower_bound:
            self.canvas.setZ(self.c_scroll_stop)
            self.m_diff = 0
            return task.done

    def rubberband_task(self, task):
        pass

    def add_item(self,
                 image=None,
                 image_scale=0.15,
                 image_pos=(0, 0, 0),
                 title=None,
                 title_pos=(0, 0, 0),
                 text=None,
                 text_pos=(0, 0, 0),
                 value=None):
        '''Appends an item to the end of the list. It can hold an image,
        title and text. Image: Panda3d path eg. 'models/picture.jpg'.
        Value: The item has function 'get/set_value()' to work with individual
        values of an activated element. Value gets set to the item on adding it.'''

        item_nr = len(self.item_list) + 1
        item_pos = self.i_start - (self.i_y + self.item_v_padding) * item_nr

        item = DirectFrame(
            parent=self.canvas,
            text=str(item_nr),  # Abused as an ID tag
            text_fg=(0, 0, 0, 0),
            frameSize=self.i_size,
            frameColor=self.item_background,
            borderWidth=(0.01, 0.01),
            pos=(0, 0, item_pos),
            relief=DGG.FLAT,
            state=DGG.NORMAL,
            enableEdit=0,
            suppressMouse=0)
        item.bind(DGG.B1RELEASE, self._switch_active_item, [item])

        if image is not None:
            OnscreenImage(  # Add an Image
                image=image,
                pos=image_pos,
                scale=(1 * image_scale, 1, 1 * image_scale),
                parent=(item))

        DirectLabel(parent=item,  # Add a Title
                    text=title,
                    text_scale=self.i_y / 4,
                    text_fg=(1, 1, 1, 1),
                    text_align=TextNode.ALeft,
                    frameColor=(0, 0, 0, 0),
                    pos=title_pos)

        DirectLabel(parent=item,  # Add a Text
                    text=text,
                    text_scale=self.i_y / 5,
                    text_fg=(1, 1, 1, 1),
                    text_align=TextNode.ALeft,
                    frameColor=(0, 0, 0, 0),
                    pos=text_pos)

        self.item_list.append(item)
        self.value_list.append(value)

    def get_active_item(self):
        return self.active_item

    def set_active_item(self, pos):
        self._switch_active_item(self.item_list[pos], None)

    def get_active_id(self):
        return int(self.active_item['text'])

    def get_active_value(self):
        return self.value_list[int(self.active_item['text']) - 1]

    def hide(self):
        '''Triggers the DirectFrame.hide() of the main frame'''

        self.frame.hide()

    def show(self):
        '''Triggers the DirectFrame.show() of the main frame'''

        self.frame.show()

    def clear(self):
        '''Destroys every item that was added to the list'''

        for item in self.item_list:
            item.destroy()
        self.item_list = []
        self.active_item = None
        self.value_list = []
        self.canvas.setZ(0)

    def destroy(self):
        '''Destroys the whole list and every item in it'''

        self.canvas.destroy()
        self.frame.destroy()
