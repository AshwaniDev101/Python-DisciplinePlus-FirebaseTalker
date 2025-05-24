from lib.managers.firebase_manager import FirebaseManager
from lib.excel_to_firebase import get_initiative_list_from_excel, upload_initiative_list_to_firebase
from lib.ui.ApplicationUI import startApplicationUI


def upload_excel_to_firebase(day_list,serviceAccountKeyPath,file_path):

    for day in day_list:
        initiative_list = get_initiative_list_from_excel(day, file_path=file_path)
        for ini in initiative_list:
            print(ini.title)
        upload_initiative_list_to_firebase(serviceAccountKeyPath=serviceAccountKeyPath, day=day,
                                           data_list=initiative_list)

def clean_firebase_data(day_list,serviceAccountKeyPath):

    for day in day_list:
        firebase = FirebaseManager(serviceAccountKeyPath)
        firebase.clean_initiatives(day)








def main():

    file_path = r"S:\Data\temp test game json\xlsx test\DisciplinePlusData.xlsx"
    serviceAccountKeyPath = "discipline-plus-serviceAccountKey.json"

    day_list = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    # clean_firebase_data(day_list=day_list,serviceAccountKeyPath=serviceAccountKeyPath)
    # upload_excel_to_firebase(day_list=day_list,serviceAccountKeyPath=serviceAccountKeyPath,file_path=file_path)

    startApplicationUI()









if __name__ == '__main__':
    main()

