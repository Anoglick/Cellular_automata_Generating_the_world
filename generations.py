import random
import numpy as np
import settings as ss
from biomes_type import BiomesType

class Manager:
    def __init__(self, app, pg):
        self.classmethod = Auxiliary(app, pg)

        self.app = app
        self.pg = pg
        self.biome = BiomesType
        self.grid = self.classmethod.initialize_grid()

        self.renderers = [
            self.RenderSeaAndLandLayer(self),
            self.RenderSandsLayer(self),
            self.RenderSeaShoreLayer(self),
            self.RenderWoodsLayer(self),
        ]

    def layer_management(self):
        for renderer in self.renderers:
            renderer.create_layout()

    class RenderSeaAndLandLayer:
        def __init__(self, outer_instance):
            self.outer = outer_instance

        def create_layout(self):
            self.outer.classmethod.start_render()
            self.next_lands_sea_count()
        
        def next_lands_sea_count(self):
            for _ in range(ss.GENERATIONS):
                self.next_generation_lands()

        def next_generation_lands(self):
            for row in range(len(self.outer.grid)):
                for col in range(len(self.outer.grid[row])):
                    counter_sea, counter_land = self.outer.classmethod.count_neighbors(self.outer.grid, row, col, self.outer.biome.SEA), self.outer.classmethod.count_neighbors(self.outer.grid, row, col, self.outer.biome.LAND)

                    if self.outer.grid[row][col] == self.outer.biome.LAND:
                        if counter_sea in {3, 6, 7, 8}:
                            self.outer.grid[row][col] = self.outer.biome.SEA
                            self.outer.classmethod.paint_pixel(self.outer.grid[row][col], row, col)
                    
                    elif self.outer.grid[row][col] == self.outer.biome.SEA:
                        if counter_land in {3, 6, 7, 8}:
                            self.outer.grid[row][col] = self.outer.biome.LAND
                            self.outer.classmethod.paint_pixel(self.outer.grid[row][col], row, col)
    
            self.outer.pg.display.update()
    
    class RenderSandsLayer:
        def __init__(self, outer_instance):
            self.outer = outer_instance

        def create_layout(self):
            self.start_border_sands()
            for _ in range(ss.GENERATIONS-100):
                self.next_sands_gen()
            
        def start_border_sands(self):
            for row in range(len(self.outer.grid)):
                for col in range(len(self.outer.grid[row])):
                    counter_sea = self.outer.classmethod.count_neighbors(self.outer.grid, row, col, self.outer.biome.SEA)

                    if self.outer.grid[row][col] == self.outer.biome.LAND:
                        if counter_sea >= 1:
                            self.outer.grid[row][col] = self.outer.biome.SAND
                            self.outer.classmethod.paint_pixel(self.outer.grid[row][col], row, col)
            self.outer.pg.display.update()
    
        def next_sands_gen(self):
            for row in range(len(self.outer.grid)):
                for col in range(len(self.outer.grid[row])):
                    counter_sands = self.outer.classmethod.count_neighbors(self.outer.grid, row, col, self.outer.biome.SAND)

                    if self.outer.grid[row][col] == self.outer.biome.SEA:
                        if counter_sands >= 5:
                            r = random.randint(0, 50)
                            if r == 1:
                                self.outer.grid[row][col] = BiomesType.SAND
                                self.outer.classmethod.paint_pixel(self.outer.grid[row][col], row, col)
            self.outer.pg.display.update()
        
    class RenderSeaShoreLayer:
        def __init__(self, outer_instance):
            self.outer = outer_instance

        def create_layout(self):
            self.start_border_sea_shore()
            for _ in range(ss.GENERATIONS-100):
                self.next_sea_shore_gen()

        def start_border_sea_shore(self):
            for row in range(len(self.outer.grid)):
                for col in range(len(self.outer.grid[row])):
                    counter_sands = self.outer.classmethod.count_neighbors(self.outer.grid, row, col, self.outer.biome.SAND)

                    if self.outer.grid[row][col] == self.outer.biome.SEA:
                        if counter_sands >= 1:
                            self.outer.grid[row][col] = self.outer.biome.SEA_SHORE
                            self.outer.classmethod.paint_pixel(self.outer.grid[row][col], row, col)
            self.outer.pg.display.update()

        def next_sea_shore_gen(self):
            for row in range(len(self.outer.grid)):
                for col in range(len(self.outer.grid[row])):
                    counter_sea_shore = self.outer.classmethod.count_neighbors(self.outer.grid, row, col, self.outer.biome.SEA_SHORE)

                    if self.outer.grid[row][col] == self.outer.biome.SEA:
                        if counter_sea_shore >= 4:
                            r = random.randint(0, 30)
                            if r == 1:
                                self.outer.grid[row][col] = self.outer.biome.SEA_SHORE
                                self.outer.classmethod.paint_pixel(self.outer.grid[row][col], row, col)
            self.outer.pg.display.update()

    class RenderWoodsLayer:
        def __init__(self, outer_instance):
            self.outer = outer_instance

        def create_layout(self):
            self.start_random_woods()
            for _ in range(ss.GENERATIONS-150):
                self.next_woods_gen()

        def start_random_woods(self):
            for row in range(len(self.outer.grid)):
                for col in range(len(self.outer.grid[row])):
                    if self.outer.grid[row][col] == self.outer.biome.LAND:
                        r = random.randint(1, 2)
                        if r == 1:
                            self.outer.grid[row][col] = self.outer.biome.WOODS
                            self.outer.classmethod.paint_pixel(self.outer.grid[row][col], row, col)
            self.outer.pg.display.update()

        def next_woods_gen(self):
            for row in range(len(self.outer.grid)):
                for col in range(len(self.outer.grid[row])):
                    counter_woods, counter_land = self.outer.classmethod.count_neighbors(self.outer.grid, row, col, self.outer.biome.WOODS), self.outer.classmethod.count_neighbors(self.outer.grid, row, col, self.outer.biome.LAND)
                    
                    if self.outer.grid[row][col] == self.outer.biome.LAND:
                        if counter_woods in {3, 6, 7, 8}:
                            self.outer.grid[row][col] = self.outer.biome.WOODS
                            self.outer.classmethod.paint_pixel(self.outer.grid[row][col], row, col)

                    elif self.outer.grid[row][col] == self.outer.biome.WOODS:
                        if counter_land in {3, 6, 7, 8}:
                            self.outer.grid[row][col] = self.outer.biome.LAND
                            self.outer.classmethod.paint_pixel(self.outer.grid[row][col], row, col)
                    
            self.outer.pg.display.update()

class Auxiliary:
    def __init__(self, app, pg):
        self.app = app
        self.pg = pg

    def start_render(self):
        grid = self.initialize_grid()
        for row in range(len(grid)):
            for col in range(len(grid[row])):
                self.paint_pixel(grid[row][col], row, col)
        self.pg.display.update()

    def initialize_grid(self):
        rows = ss.ROWS
        cols = ss.COLS
        grid = np.zeros((rows, cols), dtype=BiomesType)
        
        for row in range(rows):
            for col in range(cols):
                r = random.randint(1, 2)
                grid[row][col] = BiomesType.SEA if (r == 1) else BiomesType.LAND
                self.paint_pixel(grid[row][col], row, col)
        self.pg.display.update()
        return grid

    def paint_pixel(self, biome, row, col, our_color=None):
        if our_color:
            color = our_color
        elif biome == BiomesType.LAND:
            color = ss.COLORS["GREEN"]
        elif biome == BiomesType.LAND:
            color = ss.COLORS["GREEN"]
        elif biome == BiomesType.SEA:
            color = ss.COLORS["BLUE"]
        elif biome == BiomesType.SAND:
            color = ss.COLORS["YELLOW"]
        elif biome == BiomesType.SEA_SHORE:
            color = ss.COLORS["LIGHT_BLUE"]
        elif biome == BiomesType.WOODS:
            color = ss.COLORS["DARK_GREEN"]
        self.pg.draw.rect(self.app.screen, color,
                          (row * ss.CELL_SIZE, col * ss.CELL_SIZE, ss.CELL_SIZE, ss.CELL_SIZE))

    def count_neighbors(self, grid, x, y, biome):
        directions = [
            (-1, 0), (1, 0), (0, -1), (0, 1), 
            (-1, -1), (-1, 1), (1, -1), (1, 1)
        ]
        counter = 0

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]):
                if grid[nx][ny] == biome:
                    counter += 1
        
        return counter
    
    # A useless function so far
    def get_random_color(self):
        return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))