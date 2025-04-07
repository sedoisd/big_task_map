import sys
import traceback

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap

from geocode import get_map, get_ll, get_spn, get_address, get_postal_code
from io import BytesIO
from PIL import Image

from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow


class MapMiniProgram(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui_files/un.ui', self)

        # variable
        self.object_to_find = 'Тольятти, ленинский проспект 20'
        self.ll = list(get_ll(self.object_to_find))
        self.spn = 0.002
        self.theme = 'light'
        self.pt = ''
        self.flag_display_postal_code = True
        self.flag_search = False
        self.is_get_postal_code = False

        # exe
        self._update_map()
        # self.radio_light_theme.setChecked(True)
        self.line_search.setPlaceholderText('Введите адрес для поиска')

        # bind
        self.line_search.returnPressed.connect(self.object_search_by_line)
        self.button_search.clicked.connect(self.object_search_by_line)
        self.button_search_reset.clicked.connect(self.search_reset)
        self.radio_light_theme.toggled.connect(self.switch_theme)
        # self.radio_dark_theme.toggled.connect(self.switch_theme)
        self.radio_postal_enabled.toggled.connect(self.switch_postal_code)

    def switch_theme(self):
        if self.radio_light_theme.isChecked():
            self.theme = 'light'
        elif self.radio_dark_theme.isChecked():
            self.theme = 'dark'
        self._update_map()

    def object_search_by_line(self):
        self.object_to_find = self.line_search.text()
        self.object_search()

    def object_search(self, flag_click=False):
        try:
            if not flag_click:
                self.ll = list(get_ll(self.object_to_find))
                self.pt = f'{self.ll[0]},{self.ll[1]},pm2rdm'
                self.spn = get_spn(self.object_to_find)
                self._update_map()
            self.search_address = get_address(self.object_to_find)
            address = f'Адрес обьекта: {self.search_address}'
            self.is_get_postal_code = self.try_get_postal_code()
            if self.flag_display_postal_code and self.is_get_postal_code:
                address += f', {self.search_postal_code}'
            self.label_address.setText(address)
            self.flag_search = True
            print(address)
        except Exception:
            # print(traceback.print_exc())
            self.line_search.setText('')
            self.line_search.setPlaceholderText('Ничего не удалось найти')
            self.label_address.setText('Адрес обьекта: -')


    def try_get_postal_code(self):
        try:
            self.search_postal_code = get_postal_code(self.object_to_find)
            return True
        except Exception:
            return False

    def search_reset(self):
        self.pt = ''
        self.line_search.setText('')
        self.line_search.setPlaceholderText('Введите адрес для поиска')
        self.label_address.setText('Адрес обьекта: -')
        self._update_map()
        self.flag_search = False
        self.is_get_postal_code = False

    def switch_postal_code(self):
        self.flag_display_postal_code = not self.flag_display_postal_code
        if self.flag_search:
            address = f'Адрес обьекта: {self.search_address}'
            if self.is_get_postal_code and self.flag_display_postal_code:
                address += f', {self.search_postal_code}'
            self.label_address.setText(address)

    def search_by_left_click_mouse(self, x, y):
        dx_from_center = 310 - x
        dy_from_center = 230 - y
        map_x = round(self.ll[0] - self.spn / 190 * dx_from_center, 7) # 190
        map_y = round(self.ll[1] + self.spn / 310 * dy_from_center, 7) # 310
        self.search_reset()
        self.pt = f'{map_x},{map_y},pm2rdm'
        self._update_map()
        self.object_to_find = f'{map_x},{map_y}'
        self.object_search(flag_click=True)

    def mousePressEvent(self, event):
        x, y = event.pos().x(), event.pos().y()
        # print(f"Координаты:{x}, {y}")
        if 10 <= x <= 610 and 10 <= y <= 460:
            if event.button() == Qt.MouseButton.LeftButton:
                # print("Левая")
                self.search_by_left_click_mouse(x, y)
            elif event.button() == Qt.MouseButton.RightButton:
                print("Правая")

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_PageDown:
            self.spn *= 2
            if self.spn > 60:
                self.spn = 60
        elif event.key() == Qt.Key.Key_PageUp:
            self.spn /= 2
            if self.spn < 0.0005:
                self.spn = 0.0005
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
        try:
            params_static = {'ll': f'{self.ll[0]},{self.ll[1]}',
                             'spn': f'{self.spn},{self.spn}',
                             'theme': self.theme,
                             'pt': self.pt,
                             'size': '600,450'}
            resp = get_map(params_static)
            im = BytesIO(resp.content)
            # print(im) # io bytes object
            opened_image = Image.open(im)
            opened_image.save('map.png')
            image = QPixmap('map.png')
            self.image_label.setPixmap(image)
            # opened_image.show()
        except Exception:
            print('Ошибка')
            pass



def except_hook(a, b, c):
    sys.__excepthook__(a, b, c)


if __name__ == '__main__':
    sys.__excepthook__ = except_hook
    app = QApplication(sys.argv)
    ex = MapMiniProgram()
    ex.show()
    sys.exit(app.exec())
