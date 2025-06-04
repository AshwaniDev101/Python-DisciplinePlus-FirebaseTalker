from lib.models.app_time import AppTime
from lib.models.study_break import StudyBreak
from lib.utils.helper import generateReadableTimestamp


class Initiative:
    def __init__(self, title, completion_time, index, id=None, dynamic_time=None,
                 is_complete=False, study_break=None):
        self.id = id or generateReadableTimestamp()
        self.title = title
        self.completion_time = completion_time
        self.dynamic_time = dynamic_time or AppTime(0, 0)
        self.is_complete = is_complete
        self.study_break = study_break or StudyBreak()
        self.index = index



    def to_map(self):
        return {
            'id': self.id,
            'title': self.title,
            'isComplete': self.is_complete,
            'dynamicTime': self.dynamic_time.to_map(),
            'completionTime': self.completion_time.to_map(),
            'studyBreak': self.study_break.to_map(),
            'index': self.index
        }

    @classmethod
    def from_map(cls, data):
        return cls(
            id=data.get('id'),
            title=data.get('title', ''),
            completion_time=AppTime.from_map(data.get('completionTime', {'hour': 0, 'minute': 0})),
            dynamic_time=AppTime.from_map(data.get('dynamicTime', {'hour': 0, 'minute': 0})),
            is_complete=data.get('isComplete', False),
            study_break=StudyBreak.from_map(data.get('studyBreak', {})),
            index=data.get('index', 0)
        )
