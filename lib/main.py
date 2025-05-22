from lib.excel_sheet_manager import ExcelSheetManager
from lib.firebase_manager import FirebaseManager
from lib.master_handler import get_initiative_list_from_excel, upload_initiative_list_to_firebase



# Setting up
file_path = r"S:\Data\temp test game json\xlsx test\DisciplinePlusData.xlsx"
serviceAccountKeyPath = "discipline-plus-serviceAccountKey.json"


day_list = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

def upload_excel_to_firebase():

    for day in day_list:
        initiative_list = get_initiative_list_from_excel(day, file_path=file_path)
        upload_initiative_list_to_firebase(serviceAccountKeyPath=serviceAccountKeyPath, day=day,
                                           data_list=initiative_list)

def clean_firebase_data():

    for day in day_list:
        firebase = FirebaseManager(serviceAccountKeyPath)
        firebase.clean_initiatives(day)


def main():
    clean_firebase_data()
    upload_excel_to_firebase()









if __name__ == '__main__':
    main()

