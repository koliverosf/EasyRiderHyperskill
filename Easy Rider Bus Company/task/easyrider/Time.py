import re


class Time:
    def __init__(self, time_str):
        self.hours, self.minutes = re.split(r':', time_str)

    def le(self, time_str):
        s_time1 = re.split(r':', time_str)
        return int(self.hours) * 60 + int(self.minutes) < int(s_time1[0]) * 60 + int(s_time1[1])
