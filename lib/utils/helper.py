

from datetime import datetime



def generateReadableTimestamp():
    now = datetime.now()
    return f"{now.year}-{_two_digits(now.month)}-" \
           f"{_two_digits(now.day)}_" \
           f"{_two_digits(now.hour)}:" \
           f"{_two_digits(now.minute)}." \
           f"{now.microsecond // 1000}_{now.microsecond % 1000}"



def _two_digits(n):
    return str(n).zfill(2)
