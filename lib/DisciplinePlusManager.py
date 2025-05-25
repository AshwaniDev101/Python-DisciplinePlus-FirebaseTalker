from lib.managers.excel.excel_sheet_manager import ExcelSheetManager
from lib.managers.firebase.firebase_manager import FirebaseManager

class DisciplinePlusManager:
    def __init__(self):

        self.day_list = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

        file_path = r"S:\Data\temp test game json\xlsx test\DisciplinePlusData.xlsx"
        service_account_key_path = "managers/firebase/key/discipline-plus-serviceAccountKey.json"

        self.firebase_manger = FirebaseManager(service_account_key_path)
        self.excel_sheet_manager = ExcelSheetManager(file_path)

    def upload_excel_to_firebase(self):

        for day in self.day_list:
            initiative_list = self.excel_sheet_manager.get_initiative_list_from_excel(day)
            for initiative in initiative_list:
                print(initiative.title)
            self.firebase_manger.upload_initiative_list_to_firebase(day=day, data_list=initiative_list)

    def clean_firebase_data(self):
        for day in self.day_list:
            self.firebase_manger.clean_initiatives(day)
