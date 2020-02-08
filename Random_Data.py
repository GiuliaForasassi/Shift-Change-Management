import random
import names
import copy
# SCENARIO

def generate_random_data(shift_types, contract_types, skills, num_nurses, num_time_periods):

    #random.seed(10)

    # contracts details
    contracts = {}
    for contract in contract_types:
        dic = {}
        dic['min_assignments'] = random.randint(1, 4)
        dic['max_assignments'] = random.randint(2*dic['min_assignments']+1, 12)
        dic['min_cons_working_days'] = random.randint(1, 3)
        dic['max_cons_working_days'] = random.randint(2*dic['min_cons_working_days']+1, 9)
        dic['min_cons_days_off'] = random.randint(1, 3)
        dic['max_cons_days_off'] = random.randint(2*dic['min_cons_days_off']+1, 9)
        dic['max_working_week_ends'] = random.randint(2, 4)
        dic['complete_week_ends'] = bool(random.randint(0, 1))
        contracts[contract] = dic

    # nurses: dictionary of dictionaries
    nurses = {}
    for nurse_id in range(num_nurses):
        dic = {}
        dic['name'] = names.get_first_name()
        dic['contract_type'] = contract_types[random.randint(0, len(contract_types)-1)]
        r = random.random()
        # head
        if r < 0.1:
            dic['skills'] = [skills[0]]
        # regular
        elif r < 0.6:
            dic['skills'] = [skills[1]]
        # trainee
        elif r < 0.8:
            dic['skills'] = [skills[2]]
        # head + regular
        else:
            dic['skills'] = skills[:2]
        print(dic['skills'])
        nurses[nurse_id] = dic

    # poichè si fa solo giornaliero la cosa dei turni consecutivi e non per shift sta roba non serve

    # # minimum number of consecutive assignments
    # minimum_consecutive_assignment = {'morning' : random.randint(1, 5), 'afternoon' : random.randint(1, 5), 'night' : 1}

    # # maximum number of consecutive assignments
    # maximum_consecutive_assignment = {'morning' : random.randint(2*minimum_consecutive_assignment['morning'], 8), 'afternoon' : 2*random.randint(minimum_consecutive_assignment['afternoon'], 8), 'night' : 1}

    # matrix that represents the shifts succession that are forbidden
    forbidden_shifts_succession = {'morning' : {'morning' : False, 'afternoon' : False , 'night' : False},
                                'afternoon' : {'morning' : False, 'afternoon' : False, 'night' : False},
                                'night' : {'morning' : True, 'afternoon' : True, 'night' : True}

                                }

    # WEEK-DATA

    # single week: 7 days
    week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    days = [day + '-' + str(t) for t in range(num_time_periods) for day in week]

    # minimum and optimum number of nurses
    minimum_nurses = {}
    optimum_nurses = {}
    range_for_shift = {"morning": (10,15), "afternoon": (4,8), "night": (2,4)}
    for day in days:
        for shift in shift_types:
            for skill in skills:
                minimum_nurses[day, shift, skill] = random.randint(*range_for_shift[shift])
                optimum_nurses[day, shift, skill] = random.randint(minimum_nurses[day, shift, skill], minimum_nurses[day, shift, skill] + 2)


    # nurse requests: not to work that day in that shift
    permit_requests = []
    num_requests = random.randint(0, 10)

    all_requests = []
    for nurse_id in range(num_nurses):
        for day in days:
            for shift in shift_types:
                all_requests.append((nurse_id, day, shift))

    random.shuffle(all_requests)
    permit_requests = all_requests[:num_requests]


    # BORDER DATA
    history = {}
    for nurse_id in range(num_nurses):
        dic = {}
        dic['last_shift'] = ['morning', 'afternoon', 'night', None][random.randint(0, 3)]
        if dic['last_shift'] is None:
            dic['num_cons_shift_sametype'] = 0
            dic['num_cons_shift'] = 0
            dic['num_cons_days_off'] = random.randint(0, 3)
        else:
            dic['num_cons_shift_sametype'] = random.randint(0, 3)
            dic['num_cons_shift'] = random.randint(dic['num_cons_shift_sametype'], 5)
            dic['num_cons_days_off'] = 0
        
        dic['num_worked_week_ends'] = random.randint(0, 1)
        dic['num_worked_shifts'] = random.randint(dic['num_worked_week_ends'], 8)

        history[nurse_id] = dic
    
    return history, nurses, contracts, days, minimum_nurses, forbidden_shifts_succession, optimum_nurses, permit_requests