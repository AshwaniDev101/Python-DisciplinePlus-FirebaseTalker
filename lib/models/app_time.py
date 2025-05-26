class AppTime:
    def __init__(self, hour, minute):
        self.hour = hour
        self.minute = minute

    def remaining_time(self):
        if self.hour == 0:
            return f"{self.minute}m"
        if self.minute == 0:
            return f"{self.hour}h"
        return f"{self.hour}h {self.minute}m"

    def __str__(self):
        # display_hour = 12 if self.hour % 12 == 0 else self.hour % 12
        # period = 'PM' if self.hour >= 12 else 'AM'
        # return f"{str(self.hour).zfill(2)}:{str(self.minute).zfill(2)}"
        return f"{str(int(self.minute))}"

    @property
    def is_zero(self):
        return self.hour == 0 and self.minute == 0

    def to_map(self):
        return {
            'hour': self.hour,
            'minute': self.minute
        }

    @classmethod
    def from_map(cls, data):
        return cls(
            data['hour'],
            data['minute']
        )
