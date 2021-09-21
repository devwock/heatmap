from excel_importer import ExcelImporter
from heatmap_generator import HeatmapGenerator


def main():
    data = ExcelImporter.get_data()
    HeatmapGenerator.run(data)


if __name__ == "__main__":
    main()
