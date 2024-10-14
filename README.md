# Summary:
This code simulates terrain generation using cellular automata on a grid, where cells represent different biomes (sea, land, sands, sea shore, woods). pygame is used for visualization, while numpy manages the grid structure.

### How it works:
    1. Grid Initialization: The grid is initialized randomly with sea and land cells.
    2. РLayer Rendering: Multiple layers (sea, land, sand, shore, woods) update the grid iteratively based on predefined rules. Cells change types depending on the number of neighboring cells of specific biomes.
    3. Visualization: The grid's state is continuously rendered in pygame, with colors representing different biomes (e.g., blue for sea, green for land).

### To run the project:
```
    python install -r requirements.txt
```

# Краткая сводка:
Этот код симулирует генерацию ландшафта с помощью клеточного автомата на сетке, где клетки представляют разные биомы (море, суша, пески, побережье, леса). Для визуализации используется pygame, а для управления сеткой — numpy.

### Как это работает:
    1. Инициализация сетки: Сетка случайно инициализируется ячейками моря и суши.
    2. Рендеринг слоёв: Несколько слоёв (море, суша, песок, побережье, леса) итеративно обновляют сетку по заранее заданным правилам. Клетки меняют типы в зависимости от числа соседей определённого биома.
    3. Визуализация: Состояние сетки постоянно обновляется и отображается с помощью pygame, при этом каждый биом отображается своим цветом (например, синий для моря, зелёный для суши).

### Для запуска проекта:
```
    python install -r requirements.txt
```

