# Write your code here
import json
import itertools
from LineStop import LineStop
from Line import Line


def main():
    text = ''
    while True:
        line = input()
        if ']' not in line:
            text = text + line
        else:
            text = text + line
            break
    decoder = json.JSONDecoder()
    in_json = decoder.decode(text)
    lines = create_lines(in_json)
    # Print Errors
    # print_errors(lines)

    # Print Bus Lines Info
    # print_lines_info(lines)

    # Print stops info
    # print_stops_info(lines)

    # Print schedule errors
    # print_errors_schedule(lines)

    # Print conflict errors
    check_stops_type(lines)

def create_lines(in_json):
    lines = {}
    for elt in in_json:
        if elt["bus_id"] not in lines.keys():
            lines[elt["bus_id"]] = Line([elt])
        else:
            lines[elt["bus_id"]].add_stop(elt)
    return lines


def print_lines_info(lines):
    print('Line names and number of stops:')
    for line_key in lines.keys():
        print('bus_id: ', line_key, ", stops: ", str(lines[line_key].n_stops))


def get_stops_info(lines):
    is_ok = True
    info_stops = {"Start stops": [], "Transfer stops": [], "Finish stops": [], "On-demand stops": []}
    transfer = []
    for line_key in lines.keys():
        start, finish, demand, valid = lines[line_key].check_line()
        if not valid:
            is_ok = False
            info_stops = line_key
            break
        else:
            transfer.append(set(lines[line_key].line_stops_names))
            info_stops["Start stops"].append(start[0])
            info_stops["Finish stops"].append(finish[0])
            info_stops["On-demand stops"] += demand
    if is_ok:
        my_iter = itertools.combinations(transfer, 2)
        iter_list = [[elt[0], elt[1]] for elt in my_iter]
        inter = [set.intersection(*combi) for combi in iter_list]
        union = set.union(*inter)
        info_stops["Transfer stops"] = list(union)
        info_stops["Start stops"] = list(set(info_stops["Start stops"]))
        info_stops["Finish stops"] = list(set(info_stops["Finish stops"]))
        info_stops["On-demand stops"] = list(set(info_stops["On-demand stops"]))
    return is_ok, info_stops


def check_stops_type(lines):
    conflict_stops = []
    is_ok, info_stops = get_stops_info(lines)
    if is_ok:
        other_stops = list(set(info_stops["Transfer stops"] + info_stops["Start stops"] + info_stops["Finish stops"]))
        for stop in info_stops["On-demand stops"]:
            if stop in other_stops:
                conflict_stops.append(stop)
        print('On demand stops test:')
        if len(conflict_stops) == 0:
            print('OK')
        else:
            print('Wrong stop type: ', list(set(conflict_stops)))


def print_stops_info(lines):
    is_ok, info_stops = get_stops_info(lines)
    if is_ok:
        for info in info_stops.keys():
            info_stops[info] = list(set(info_stops[info]))
            info_stops[info].sort()
            print(info, ": ", int(len(info_stops[info])), " ", info_stops[info])
    else:
        print("There is no start or end stop for the line: ", str(info_stops))


def print_errors_schedule(lines):
    for line_id in lines.keys():
        is_ok, stop = lines[line_id].check_time_schedule()
        if not is_ok:
            print("bus_id line ", line_id, ": wrong time on station ", stop)


def print_errors(in_json):
    errors = {}
    for elt in in_json:
        line = LineStop(elt)
        if len(errors) < 1:
            errors = line.add_errors()
        else:
            errors = line.add_errors(errors)
    total = 0
    for key in errors.keys():
        total += errors[key]
    print("Type and required field validation: ", str(total), ' errors')
    for key in errors.keys():
        print(key, ": ", str(errors[key]))


if __name__ == "__main__":
    main()
