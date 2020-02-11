import json
import os
import names

# tira fuori le info dal file json e le restituisce come dizionario
def get_json_content(file):
    with open(file, "rt") as f:
        j = json.load(f)
    return j


def decode_history(history_json):

    nh = history_json["nurseHistory"]
    history = {}

    for h in nh:
        nurse_id = h["nurse"]

        dic = {}
        dic["last_shift"] = h["lastAssignedShiftType"]
        # dic['num_cons_shift_sametype'] = ...
        dic['num_cons_shift'] = h["numberOfConsecutiveAssignments"]
        dic['num_cons_days_off'] = h["numberOfConsecutiveDaysOff"]
        dic['num_worked_week_ends'] = h["numberOfWorkingWeekends"]
        dic['num_worked_shifts'] = h["numberOfAssignments"]

        history[nurse_id] = dic

    return history


def decode_scenario(scenario_json):
    # lista di dizionari
    cs = scenario_json["contracts"]
    contract_types = []
    contracts = {}
    for c in cs:
        if c['id'] not in contract_types:
            contract_types.append(c['id'])
        contracts[c['id']] = {}

        contracts[c['id']]['min_assignments'] = c['minimumNumberOfAssignments']
        contracts[c['id']]['max_assignments'] = c['maximumNumberOfAssignments']
        contracts[c['id']]['min_cons_working_days'] = c['minimumNumberOfConsecutiveWorkingDays']
        contracts[c['id']]['max_cons_working_days'] = c['maximumNumberOfConsecutiveWorkingDays']
        contracts[c['id']]['min_cons_days_off'] = c['minimumNumberOfConsecutiveDaysOff']
        contracts[c['id']]['max_cons_days_off'] = c['maximumNumberOfConsecutiveDaysOff']
        contracts[c['id']]['max_working_week_ends'] = c['maximumNumberOfWorkingWeekends']
        contracts[c['id']]['complete_week_ends'] = bool(c['completeWeekends'])

    fs = scenario_json['forbiddenShiftTypeSuccessions']
    forbidden_shifts_succession = {}
    shift_types = []
    for f in fs:
        shift_type = f['precedingShiftType']
        if shift_type not in shift_types:
            shift_types.append(shift_type)
            forbidden_shifts_succession[shift_type] = {}

    for shift_type_before in shift_types:
        for shift_type_after in shift_types:
            forbidden_shifts_succession[shift_type_before][shift_type_after] = False

    for f in fs:
        nextShifts = f['succeedingShiftTypes']
        for nextShift in nextShifts:
            forbidden_shifts_succession[f['precedingShiftType']][nextShift] = True
    
    skills = scenario_json["skills"] 

    ns = scenario_json["nurses"]
    nurses = {}
    for n in ns:
        nurse_id = n['id']
        nurses[nurse_id] = {}
        nurses[nurse_id]['contract_type'] = n['contract']
        nurses[nurse_id]['skills'] = n['skills']
        nurses[nurse_id]['name'] = names.get_first_name()
    
    return contracts, forbidden_shifts_succession, nurses, shift_types, skills


def decode_week(week_json, w, shift_types):

    days = [day + '-' + str(w) for day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']]
    minimum_nurses = {}
    optimum_nurses = {}

    rs = week_json["requirements"]
    for r in rs:
        shift = r["shiftType"]
        skill = r["skill"]
        for key in r:
            if "requirement" not in key:
                continue
            day = key[len("requirementOn"):] + "-" + str(w)
            minimum_nurses[day, shift, skill] = r[key]["minimum"]
            optimum_nurses[day, shift, skill] = r[key]["optimal"]

    permit_requests = []
    prs = week_json["shiftOffRequests"]
    for pr in prs:
        nurse_id = pr['nurse']
        day = pr['day'] + "-" + str(w)
        shift = pr['shiftType']
        if shift == 'Any':
            for s in shift_types:
                permit_requests.append((nurse_id, day, s))
        else:
            permit_requests.append((nurse_id, day, shift))

    return days, minimum_nurses, optimum_nurses, permit_requests


def read_data(num_nurses, num_time_periods):
    s = "n{0:0=3d}w".format(num_nurses) + str(num_time_periods)
    dir = os.path.join("Real_Data", s)

    # per catturare nome file della storia
    history_file = os.path.join(dir, "H0-"+s+"-0.json")
    # richiamo la funzione per catturare le info del json
    # è un dizionario che rappresenta contenuto del json
    history_json = get_json_content(history_file)

    history = decode_history(history_json)

    scenario_file = os.path.join(dir, "Sc-"+s+".json")
    scenario_json = get_json_content(scenario_file)

    contracts, forbidden_shifts_succession, nurses, shift_types, skills = decode_scenario(scenario_json)
    contract_types = contracts.keys()

    days = []
    minimum_nurses = {}
    optimum_nurses = {}
    permit_requests = []
    for w in range(4):
        week_file = os.path.join(dir, "WD-"+s+"-{}.json".format(w))
        week_json = get_json_content(week_file)
        # specifici per una settimana
        ds, mn, om, pr = decode_week(week_json, w, shift_types)

        # quelli completi per tutto il periodo
        days.extend(ds)
        minimum_nurses.update(mn)
        optimum_nurses.update(om)
        permit_requests.extend(pr)

    return history, nurses, contracts, days, minimum_nurses, forbidden_shifts_succession, optimum_nurses, permit_requests, shift_types, contract_types, skills
