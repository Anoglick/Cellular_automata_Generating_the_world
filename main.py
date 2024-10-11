import sys
import pygame as pg
from generations import Manager
import settings as ss

class App:
    def __init__(self):
        self.screen = pg.display.set_mode(ss.SCREEN_SIZE)
        self.clock = pg.time.Clock()
        self.biomes = Manager(app=self, pg=pg)

    def run(self):
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        self.biomes.layer_management()

            pg.display.update()
            self.clock.tick(ss.FPS) 

if __name__ == '__main__':
    app = App()
    app.run()

