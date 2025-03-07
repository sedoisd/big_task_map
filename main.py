import sys

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap

from geocode import get_map, get_ll
from io import BytesIO
from PIL import Image

from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QRadioButton


class MapMiniProgram(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui_files/un.ui', self)

        # variable
        self.toponym_to_find = 'Тольятти, ленинский проспект 20'
        self.ll = list(get_ll(self.toponym_to_find))
        self.spn = 0.002
        self.theme = 'light'

        # exe
        self._update_map()
        self.radio_light_theme.setChecked(True)

        # bind
        self.radio_light_theme.toggled.connect(self.switch_theme)
        # self.radio_dark_theme.toggled.connect(self.switch_theme)

    def switch_theme(self):
        if self.radio_light_theme.isChecked():
            self.theme = 'light'
        elif self.radio_dark_theme.isChecked():
            self.theme = 'dark'
        self._update_map()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_PageDown and self.spn < 60:
            self.spn *= 2
        elif event.key() == Qt.Key.Key_PageUp and self.spn > 0.00025:
            self.spn /= 2
        if event.key() == Qt.Key.Key_Up:
            self.ll[1] += self.spn / 2
        elif event.key() == Qt.Key.Key_Down:
            self.ll[1] -= self.spn / 2
        elif event.key() == Qt.Key.Key_Left:
            self.ll[0] -= self.spn / 2
        elif event.key() == Qt.Key.Key_Right:
            self.ll[0] += self.spn / 2
        if self.ll[0] > 180:
            self.ll[0] = -180 + (self.ll[0] - 180) + 1
        elif self.ll[0] < -180:
            self.ll[0] = 180 - abs(self.ll[0] + 180) - 1
        if self.ll[1] > 85:
            self.ll[1] = 85
        elif self.ll[1] < -75:
            self.ll[1] = -75
        self._update_map()

    def _update_map(self):
        params_static = {'ll': f'{self.ll[0]},{self.ll[1]}',
                         'spn': f'{self.spn},{self.spn}',
                         'theme': self.theme,
                         'size': '600,450'}
        resp = get_map(params_static)
        im = BytesIO(resp.content)
        # print(im) # io bytes object
        # im.seek(0)
        opened_image = Image.open(im)
        opened_image.save('map.png')
        image = QPixmap('map.png')
        self.image_label.setPixmap(image)
        # opened_image.show()


# def except_hook(a, b, c):
#     sys.__excepthook__(a, b, c)


if __name__ == '__main__':
    # sys.__excepthook__ = except_hook
    app = QApplication(sys.argv)
    ex = MapMiniProgram()
    ex.show()
    sys.exit(app.exec())
