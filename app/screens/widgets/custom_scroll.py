from kivy.uix.scrollview import ScrollView
from kivy.lang import Builder


class CustomScroll(ScrollView):

    def _update_effect_x(self, *args):
        vp = self._viewport
        if not vp or not self.effect_x:
            return
        sw = vp.width - self.width
        if sw < 1:
            return
        sx = self.effect_x.scroll / float(sw)
        self.scroll_x = -sx
        self._trigger_update_from_scroll()

    def _update_effect_y(self, *args):
        vp = self._viewport
        if not vp or not self.effect_y:
            return
        sh = vp.height - self.height
        if sh < 1:
            return
        sy = self.effect_y.scroll / float(sh)
        self.scroll_y = -sy
        self._trigger_update_from_scroll()
