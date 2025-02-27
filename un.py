import pygame
# from PIL import Image
from geocode import get_map, get_ll
from io import BytesIO


class MapMiniProgram:
    def __init__(self, size):
        pygame.init()
        self.screen = pygame.display.set_mode(size)

        # variable
        self.running = True
        self.toponym_to_find = 'Тольятти, ленинский проспект 20'
        self.ll = list(get_ll(self.toponym_to_find))
        self.spn = 0.002
        self.image_map = self.create_map(self.toponym_to_find)

        # exe
        self.run()

    def run(self):
        while self.running:
            for event in pygame.event.get():
                self.event_handling(event)
            self.screen.fill((0, 0, 0))
            self.screen.blit(self.image_map, (0, 0))
            pygame.display.flip()
        pygame.quit()

    def event_handling(self, event):
        if event.type == pygame.QUIT:
            self.running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_PAGEUP and self.spn > 0.00025:
                self.spn /= 2
            elif event.key == pygame.K_PAGEDOWN and self.spn < 60:
                self.spn *= 2
            if event.key == pygame.K_UP:
                self.ll[1] += self.spn / 2
            elif event.key == pygame.K_DOWN:
                self.ll[1] -= self.spn / 2
            elif event.key == pygame.K_LEFT:
                self.ll[0] -= self.spn / 2
            elif event.key == pygame.K_RIGHT:
                self.ll[0] += self.spn / 2
            if self.ll[0] > 180:
                self.ll[0] = -180 + (self.ll[0] - 180) + 1
            elif self.ll[0] < -180:
                self.ll[0] = 180 - abs(self.ll[0] + 180) - 1
            if self.ll[1] > 85:
                self.ll[1] = 85
                # self.ll[1] = -90 + (self.ll[1] - 90) + 1
            elif self.ll[1] < -75:
                self.ll[1] = -75
                # self.ll[1] = 90 - abs(self.ll[1] + 90) - 1
                # устроитьь подсчет до макс точки каждого мастаба широт а 75 первый предел
            print(self.spn, self.ll, self.spn)
            self.image_map = self.create_map(self.toponym_to_find)

    def create_map(self, toponym):
        params_static = {'ll': f'{self.ll[0]},{self.ll[1]}',
                         # 'z': self.scale_z,
                         'spn': f'{self.spn},{self.spn}',
                         'size': '600,450'}
        resp = get_map(params_static)
        im = BytesIO(resp.content)
        im.seek(0)
        # opened_image = Image.open(im)
        # opened_image.show()
        surface = pygame.image.load(im)
        return surface


if __name__ == '__main__':
    screen_size = 600, 450
    program = MapMiniProgram(screen_size)
