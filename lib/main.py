from lib.managers.json.shared_preferences import SharedPreferences
from lib.ui.ApplicationUI import startApplicationUI
# use 'auto-py-to-exe' to build exe
def main():

    # discipline_plus_manager = DisciplinePlusManager()
    # discipline_plus_manager.clean_firebase_data()
    # discipline_plus_manager.upload_excel_to_firebase()

    startApplicationUI()

    print(SharedPreferences.get("excel_file_path"))




if __name__ == '__main__':
    main()

