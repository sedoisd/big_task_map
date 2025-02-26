import pygame
# from PIL import Image
from geocode import get_map, get_ll, get_spn
from io import BytesIO


class MapMiniProgram:
    def __init__(self, size):
        pygame.init()
        self.screen = pygame.display.set_mode(size)

        # variable
        self.running = True
        self.toponym_to_find = 'Тольятти, спортивная 4Б'
        self.delta = None
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

    def create_map(self, toponym):
        params_static = {'ll': get_ll(toponym, 'str'),
                         'spn': get_spn(toponym, 'str') if self.delta is None else self.delta}
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
