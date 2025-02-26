import pygame
# from PIL import Image
from geocode import get_map, get_ll
from io import BytesIO


class MapMiniProgram:
    def __init__(self, size):
        pygame.init()
        self.screen = pygame.display.set_mode(size)

        # variable
        # self.values_motion =
        self.running = True
        self.toponym_to_find = 'Тольятти, ленинский проспект 20'
        self.ll = list(get_ll(self.toponym_to_find))
        self.scale_z = 18
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
            if event.key == pygame.K_PAGEUP and self.scale_z < 21:
                self.scale_z += 1
            elif event.key == pygame.K_PAGEDOWN and self.scale_z > 1:
                self.scale_z -= 1
            self.image_map = self.create_map(self.toponym_to_find)
            if event.key == pygame.K_UP:
                self.ll[1] += 0.001 * (21 - self.scale_z)
            elif event.key == pygame.K_DOWN:
                self.ll[1] -= 0.001 * (21 - self.scale_z)
            elif event.key == pygame.K_LEFT:
                self.ll[0] -= 0.001 * (21 - self.scale_z)
            elif event.key == pygame.K_RIGHT:
                self.ll[0] += 0.001 * (21 - self.scale_z)
            print(self.scale_z)
    def create_map(self, toponym):
        params_static = {'ll': f'{self.ll[0]},{self.ll[1]}',
                         'z': self.scale_z,
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
