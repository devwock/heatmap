from enum import Enum

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as img
from PIL import Image
from matplotlib.colors import LinearSegmentedColormap
import scipy.ndimage.filters as filters

import variables


class DrawMode(Enum):
    MAP = 1
    GRID = 2


class HeatmapGenerator:
    TEMPLATE_HEATMAP_PATH = variables.TEMPLATE_FOLDER + variables.TEMPLATE_HEATMAP_FILE
    heatmap_width = None
    heatmap_height = None

    @classmethod
    def run(cls, data, mode=DrawMode.MAP):
        if not data:
            print('좌표 데이터가 없습니다.')
            return
        cls.initialize()
        refine_data = cls.data_to_coords(data, mode)
        cls.draw(refine_data, mode)

    @classmethod
    def initialize(cls):
        image = Image.open(cls.TEMPLATE_HEATMAP_PATH)
        cls.heatmap_width, cls.heatmap_height = image.size
        image.close()
        plt.register_cmap(cmap=cls.get_color_map())

    @classmethod
    def get_array_size(cls, mode):
        # 향후 모드 추가되면 여기 추가할 것
        if mode == DrawMode.MAP:
            rows = cls.heatmap_height
            columns = cls.heatmap_width
        else:
            rows = variables.GRID_HEATMAP_ROWS
            columns = variables.GRID_HEATMAP_COLUMNS
        return rows, columns

    @classmethod
    def data_to_coords(cls, data, mode):
        refined_data = {}
        height, width = cls.get_array_size(mode)
        for key, value in data.items():
            if len(value) == 0:
                continue
            coord_data = np.zeros(height * width)
            coord_data = coord_data.reshape((height, width))
            for coord_tuple in value:
                coord = cls.convert_coord(coord_tuple, height, width)
                if coord:
                    x = round(coord[0])
                    y = round(coord[1])
                    coord_data[y][x] += 1
            refined_data[key] = coord_data
        return refined_data

    @classmethod
    def convert_coord(cls, coord_tuple, height, width):
        x = coord_tuple[0]
        y = coord_tuple[1]
        division = coord_tuple[2]
        if x is None or y is None:
            return None
        if division == 'r':
            x = 1 - x
            y = 1 - y
        w = width - 1
        h = height - 1
        return x * w, abs(y * h - h)

    @classmethod
    def draw(cls, data, mode):
        for key, value in data.items():
            plt.figure(figsize=cls.get_figure_size()).add_axes([0, 0, 1, 1])
            plt.imshow(img.imread(cls.TEMPLATE_HEATMAP_PATH))
            if mode == DrawMode.MAP:
                value = filters.gaussian_filter(value, sigma=variables.GAUSSIAN_SIGMA)
                plt.imshow(value, cmap='jet_alpha', aspect="auto")
            else:
                fig, ax = plt.subplots()
                rows, columns = value.shape
                ax.set_xticks(np.arange(columns))
                ax.set_yticks(np.arange(rows))
                for i in range(rows):
                    for j in range(columns):
                        ax.text(j, i, value[i, j], ha="center", va="center", color="black")
                ax.imshow(value, cmap='jet_alpha', aspect="auto")
            plt.axis('off')
            plt.savefig(f'{variables.OUTPUT_FOLDER}{key}.png', bbox_inches='tight', pad_inches=0)
            plt.close()
            print(f'Save {variables.OUTPUT_FOLDER}{key}.png complete')

    @classmethod
    def get_color_map(cls):
        ncolors = 256
        color_array = plt.get_cmap('jet')(range(ncolors))
        color_array[:, -1] = np.linspace(0.0, 1.0, ncolors)
        color_map = LinearSegmentedColormap.from_list(name='jet_alpha', colors=color_array)
        return color_map

    @classmethod
    def get_figure_size(cls):
        dpi = plt.rcParams['figure.dpi']
        im_data = img.imread(cls.TEMPLATE_HEATMAP_PATH)
        height, width, depth = im_data.shape
        figure_size = width / float(dpi), height / float(dpi)
        return figure_size

