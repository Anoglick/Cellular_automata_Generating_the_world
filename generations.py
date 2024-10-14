from collections import deque
import random
import time
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
            self.RenderNaturalObjectsLayer(self),
            self.RenderPeopleLayer(self)
        ]
        self.render_clouds = self.RenderСloudsLayer(self)
        self.group_manager = self.GroupManager(self)

    def layer_management(self):
        for renderer in self.renderers:
            renderer.create_layout()
            self.render_clouds.create_layout()
    
    class RenderСloudsLayer:
        def __init__(self, outer_instance):
            self.outer = outer_instance
            self.queue = deque()

        def create_layout(self):
            for i in range(ss.GENERATIONS-100):
                self.cloud_shapes(i)
                self.outer.pg.display.update()
            
            if self.queue:
                biome, row, col, color = self.queue.popleft()
                self.outer.classmethod.update_biome(self.outer.grid, row, col, biome, color)
            self.outer.pg.display.update()

        def cloud_shapes(self, i):
            while self.queue:
                biome, row, col, color = self.queue.popleft()
                self.outer.classmethod.update_biome(self.outer.grid, row, col, biome, color)

            width, height = random.randint(5, 15), random.randint(5, 15)
            max_width, max_height = i + width, i + height

            for row in range(len(self.outer.grid)):
                for col in range(len(self.outer.grid[row])):
                    if i <= row < max_width and i <= col < max_height:
                        current_biome = self.outer.grid[row][col]
                        current_color = None
                        if current_biome == self.outer.biome.SETTLEMENTS:
                            current_color = self.outer.group_manager.get_color_from_group(row, col)
                        self.queue.append((current_biome, row, col, current_color))
                        self.outer.classmethod.update_biome(self.outer.grid, row, col, self.outer.biome.CLOUDS)

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

    class RenderNaturalObjectsLayer:
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
                        r = random.randint(1, 10)
                        if r <= 4:
                            self.outer.grid[row][col] = self.outer.biome.WOODS
                        elif r >= 9:
                            self.outer.grid[row][col] = self.outer.biome.STONES
                        self.outer.classmethod.paint_pixel(self.outer.grid[row][col], row, col)
            self.outer.pg.display.update()

        def next_woods_gen(self):
            for row in range(len(self.outer.grid)):
                for col in range(len(self.outer.grid[row])):
                    counter_woods, counter_stones, counter_land = (
                        self.outer.classmethod.count_neighbors(self.outer.grid, row, col, self.outer.biome.WOODS), 
                        self.outer.classmethod.count_neighbors(self.outer.grid, row, col, self.outer.biome.STONES), 
                        self.outer.classmethod.count_neighbors(self.outer.grid, row, col, self.outer.biome.LAND)
                    )
                    
                    if self.outer.grid[row][col] == self.outer.biome.LAND:
                        if counter_woods in {3, 6, 7, 8} and self.outer.grid[row][col] != self.outer.biome.STONES:
                            self.outer.grid[row][col] = self.outer.biome.WOODS
                            self.outer.classmethod.paint_pixel(self.outer.grid[row][col], row, col)
                        elif counter_stones in {3, 5, 7} and self.outer.grid[row][col] != self.outer.biome.WOODS:
                            self.outer.grid[row][col] = self.outer.biome.STONES
                            self.outer.classmethod.paint_pixel(self.outer.grid[row][col], row, col)

                    elif self.outer.grid[row][col] in {self.outer.biome.WOODS, self.outer.biome.STONES}:
                        if counter_land in {3, 6, 7, 8}:
                            self.outer.grid[row][col] = self.outer.biome.LAND
                            self.outer.classmethod.paint_pixel(self.outer.grid[row][col], row, col)

                    
            self.outer.pg.display.update()

    class RenderPeopleLayer:
        def __init__(self, outer_instance):
            self.outer = outer_instance
            self.pos_people = []
        
        def create_layout(self):
            self.gen_pos_people()
            for _ in range(ss.GENERATIONS-100):
                self.gen_people()
                self.outer.pg.display.update()
            
        def gen_pos_people(self):
            for row in range(len(self.outer.grid)):
                for col in range(len(self.outer.grid[row])):
                    r = random.randint(1, 100)
                    if self.outer.grid[row][col] in {self.outer.biome.LAND, self.outer.biome.WOODS, self.outer.biome.STONES} and r == 2:
                        biome = self.outer.grid[row][col]
                        self.pos_people.append((row, col, biome))
                        self.outer.classmethod.update_biome(self.outer.grid, row, col, self.outer.biome.PEOPLE)

        def gen_people(self):
            new_pos_people = []

            for (row, col, biome) in self.pos_people:
                dist, target = self.nearest_distance(row, col)
                if dist > 1:
                    self.outer.classmethod.update_biome(self.outer.grid, row, col, biome)

                    new_row, new_col = self.move_towards(row, col, target)
                    new_biome = self.outer.grid[new_row][new_col]

                    if new_biome not in {self.outer.biome.SEA, self.outer.biome.SEA_SHORE, self.outer.biome.PEOPLE}:
                        self.outer.classmethod.update_biome(self.outer.grid, new_row, new_col, self.outer.biome.PEOPLE)
                        new_pos_people.append((new_row, new_col, new_biome))
                
                elif dist <= 1:
                    group_id, found_group = self.outer.group_manager.find_free_group(row, col)
                    if found_group:
                        if (row, col) not in self.outer.group_manager.groups[group_id]["zone"]:
                            self.outer.group_manager.add_member_to_group(group_id, row, col)
                    else:   
                        self.outer.group_manager.create_group(row, col)
                    new_pos_people.append((row, col, biome))

                else:
                    new_pos_people.append((row, col, biome))
            self.pos_people = new_pos_people

        def nearest_distance(self, row, col):
            dist = float('inf')
            closest_target = None

            for row2, col2, _ in self.pos_people:
                if row2 == row and col2 == col:
                    continue
                dt = abs(row2 - row) + abs(col2 - col)
                if dt < dist:
                    dist = dt
                    closest_target = (row2, col2)
            return dist, closest_target
        
        def move_towards(self, row, col, target):
            target_row, target_col = target

            if row < target_row:
                row += 1
            elif row > target_row:
                row -= 1

            if col < target_col:
                col += 1
            elif col > target_col:
                col -= 1

            return row, col

    class GroupManager:
        def __init__(self, outer_instance):
            self.outer = outer_instance
            self.groups = {}
            self.group_id = 0

        def create_group(self, row, col):
            color = self.outer.classmethod.get_random_color()
            self.groups[self.group_id] = {
                "id": self.group_id,
                "members": 1,
                "zone": set(),
                "color": color
            }
            self.groups[self.group_id]["zone"].add((row, col))
            self.group_id += 1
            self.outer.classmethod.update_biome(self.outer.grid, row, col, self.outer.biome.SETTLEMENTS, color)

        def find_free_group(self, row, col):
            for group_id, group in self.outer.group_manager.groups.items():
                for (zone_row, zone_col) in group["zone"]:
                    if abs(zone_row - row) <= 1 and abs(zone_col - col) <= 1:
                        return group_id, True
                        
            return None, False

        def add_member_to_group(self, group_id, row, col):
            self.outer.classmethod.update_biome(self.outer.grid, row, col, self.outer.biome.SETTLEMENTS, self.groups[group_id]["color"])
            self.groups[group_id]["zone"].add((row, col))
            self.groups[group_id]["members"] += 1

        def get_color_from_group(self, row, col):
            for group in self.groups.values():
                if (row, col) in group['zone']:
                    return group['color']
            return None

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
        if biome == BiomesType.LAND:
            color = ss.COLORS["GREEN"]
        elif biome == BiomesType.SEA:
            color = ss.COLORS["BLUE"]
        elif biome == BiomesType.SAND:
            color = ss.COLORS["YELLOW"]
        elif biome == BiomesType.SEA_SHORE:
            color = ss.COLORS["LIGHT_BLUE"]
        elif biome == BiomesType.WOODS:
            color = ss.COLORS["DARK_GREEN"]
        elif biome == BiomesType.STONES:
            color = ss.COLORS["GREY"]
        elif biome == BiomesType.CLOUDS:
            color = ss.COLORS["WHITE"]
        elif biome == BiomesType.PEOPLE:
            color = ss.COLORS["RED"]
        elif biome == BiomesType.SETTLEMENTS and our_color:
            color = our_color
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

    def check_borders(self, grid, x, y):
        directions = [
            (-1, 0), (1, 0), (0, -1), (0, 1), 
            (-1, -1), (-1, 1), (1, -1), (1, 1)
        ]

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]):
                if nx == len(grid) - 1 or ny == len(grid) - 1 or nx == 0 or ny == 0:
                    return True
        return False
    
    def get_random_color(self):
        return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    def update_biome(self, grid, row, col, biome, color=None):
        grid[row][col] = biome
        self.paint_pixel(grid[row][col], row, col, color)