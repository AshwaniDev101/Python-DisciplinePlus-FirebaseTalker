from lib.models.app_time import AppTime

class StudyBreak:
    def __init__(self, title='Break', completion_time = AppTime(0, 0)):
        # Ensure title is a string, not an AppTime
        self.title = title if isinstance(title, str) else 'Break'
        self.completion_time = completion_time

    def to_map(self):
        return {
            'title': self.title,  # Safe: always a string
            'completionTime': self.completion_time.to_map()
        }

    @classmethod
    def from_map(cls, data):
        return cls(
            title=data.get('title', 'Break'),
            completion_time=AppTime.from_map(data['completionTime'])
        )
