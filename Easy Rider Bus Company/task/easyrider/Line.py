from LineStop import LineStop
from Time import Time


class Line:
    def __init__(self, json_line):
        self.line_stops = []
        self.line_stops_names = []
        self.line_id = json_line[0]["bus_id"]
        for elt in json_line:
            self.line_stops.append(LineStop(elt))
            self.line_stops_names.append(elt["stop_name"])
        self.n_stops = len(self.line_stops)

    def add_stop(self, stop_json: dict):
        self.line_stops.append(LineStop(stop_json))
        self.line_stops_names.append(stop_json["stop_name"])
        self.n_stops += 1

    def check_line(self):
        is_ok = False
        start_p = []
        final_p = []
        demand_p = []
        for stop in self.line_stops:
            s_type = stop.stop_type
            if s_type == 'S':
                start_p.append(stop.stop_name)
            elif s_type == 'F':
                final_p.append(stop.stop_name)
            elif s_type == 'O':
                demand_p.append(stop.stop_name)
        if len(start_p) == 1 and len(final_p) == 1:
            is_ok = True
        return start_p, final_p, demand_p, is_ok

    def check_time_schedule(self):
        order = []
        for elt in self.line_stops:
            order.append(elt.a_time)
        for i in range(len(order) - 1):
            if not Time(order[i]).le(order[i + 1]):
                return False, self.line_stops[i + 1].stop_name
        return True, 'OK'
