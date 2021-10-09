from excel_importer import ExcelImporter
from heatmap_generator import HeatmapGenerator, DrawMode


def main():
    is_continue = True
    while is_continue:
        is_continue = run()


def run():
    print('히트맵 종류를 선택해주세요.')
    print('1. 등고선형')
    print('2. 격자형')
    value = input("동작을 선택하세요:\n")
    if not value or not value.isnumeric() or int(value) not in (DrawMode.MAP.value, DrawMode.GRID.value):
        print('다시 선택해 주세요.')
        return True
    data = ExcelImporter.get_data()
    HeatmapGenerator.run(data, DrawMode(int(value)))
    return False


if __name__ == "__main__":
    main()
