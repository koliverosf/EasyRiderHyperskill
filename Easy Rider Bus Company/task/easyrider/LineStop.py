import re


class LineStop:

    def __init__(self, json_data: dict):
        self.stop_id = json_data["stop_id"]
        self.stop_name = json_data["stop_name"]
        self.next_stop = json_data["next_stop"]
        self.a_time = json_data["a_time"]
        self.stop_type = json_data["stop_type"]

    def add_errors(self, dic={"stop_name": 0, "stop_type": 0, "a_time": 0}):
        if self.stop_name == "" or not isinstance(self.stop_name, str) or not self.check_formats('stop_name'):
            dic["stop_name"] += 1
        if not isinstance(self.stop_type, str) or not self.check_formats('stop_type'):
            dic["stop_type"] += 1
        if self.a_time == "" or not isinstance(self.a_time, str) or not self.check_formats('a_time'):
            dic["a_time"] += 1
        return dic

    def check_formats(self, value: str):
        is_ok = False
        capital_pattern = r'[A-Z][a-z]+'
        suffix_pattern = r'(Road|Avenue|Boulevard|Street)'
        if value == 'stop_name' and ' ' in self.stop_name:
            s_name = re.split(r' ', self.stop_name)
            if re.match(capital_pattern, s_name[0]) and re.match(suffix_pattern, s_name[-1]):
                is_ok = True
        elif value == 'stop_type':
            if self.stop_type in 'SOF' and len(self.stop_type) < 2:
                is_ok = True
        elif value == 'a_time' and ':' in self.a_time:
            s_hour = re.split(r':', self.a_time)
            if len(s_hour) == 2 and len(s_hour[0]) == 2 and \
                    len(s_hour[1]) == 2 and int(s_hour[0]) < 24 and int(s_hour[1]) < 60:
                is_ok = True
        return is_ok

    def same_as(self, line_stop):
        self.stop_id = line_stop.stop_id
