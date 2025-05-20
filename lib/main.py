from lib.excel_sheet_manager import ExcelSheetManager


def manage_excel():
    path = r"S:\Data\temp test game json\xlsx test\DisciplinePlusData.xlsx"
    manager = ExcelSheetManager(path)

    manager.print_data()

    print("\n🔹 Range B1 to I8:")
    print(manager.read_range("B", "I", 1, 8))

    print("\n🔹 Column B (by letter):")
    print(manager.read_column_by_letter("B"))

    # Optional: write to cell
    # manager.write_cell("B27", "Hello World")







if __name__ == '__main__':
    manage_excel()
