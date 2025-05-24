from lib.managers.excel_sheet_manager import ExcelSheetManager
from lib.managers.firebase_manager import FirebaseManager
from lib.models.app_time import AppTime
from lib.models.initiative import Initiative
from lib.models.study_break import StudyBreak


def get_initiative_list_from_excel(week_name:str,file_path:str):

    manager = ExcelSheetManager(file_path)
    pos = manager.find_cell_position(week_name)
    df = manager.read_range_with_column_number(pos[1], pos[1]+2, 2, 30)


    # Filter out NaN with is not string but a datatype of panda
    df = df.dropna(subset=[df.columns[0]])

    initList = []

    for i, (title, duration, break_time) in enumerate(df.itertuples(index=False, name=None)):

        init = Initiative(title=title, completion_time=AppTime(0, duration),
                          study_break=StudyBreak(AppTime(0, break_time)), index=i)
        initList.append(init)
        print(f"this got added {init.to_map()}")


    return initList



def upload_initiative_list_to_firebase(serviceAccountKeyPath:str,day:str, data_list):
    firebase = FirebaseManager(serviceAccountKeyPath)
    firebase.batch_add_initiatives(day=day,initiatives=data_list)
