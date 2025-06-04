from lib.managers.excel.excel_sheet_manager import ExcelSheetManager
from lib.managers.firebase.firebase_manager import FirebaseManager
from lib.managers.json.shared_preferences import SharedPreferences


class DisciplinePlusManager:
    def __init__(self):

        self.weekday_name_list = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

        firebase_service_account_key_path = "managers/firebase/key/firebase-discipline-plus-serviceAccountKey.json"

        self.firebase_manger = FirebaseManager(firebase_service_account_key_path)
        self.excel_sheet_manager = ExcelSheetManager(SharedPreferences.get("excel_file_path"))

    def upload_excel_to_firebase(self):

        for weekday_name in self.weekday_name_list:
            # getting data from excel file
            initiative_list = self.excel_sheet_manager.get_initiative_list_from_excel(weekday_name)

            # uploading that data to firebase
            self.firebase_manger.upload_initiative_list_to_firebase(day=weekday_name, data_list=initiative_list)

    def clean_firebase_data(self):
        for day in self.weekday_name_list:
            self.firebase_manger.clean_initiatives(day)
