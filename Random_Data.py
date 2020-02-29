import random
import names
import copy


# SCENARIO

def generate_random_data(num_nurses, num_time_periods):

    # shift types list
    shift_types = ['Morning', 'Afternoon', 'Night']

    # contract types list
    contract_types = ['full_time', 'part_time', 'on_call']

    # skills list
    skills = ['head_nurse', 'regular_nurse', 'trainee']

    #random.seed(10)

    # contracts details
    contracts = {}
    for contract in contract_types:
        dic = {}
        dic['min_assignments'] = num_time_periods - 1
        dic['max_assignments'] = random.randint(6, 7) * num_time_periods
        dic['min_cons_working_days'] = random.randint(1, 3)
        dic['max_cons_working_days'] = min(random.randint(2*dic['min_cons_working_days']+1, 9), 7*num_time_periods)
        dic['min_cons_days_off'] = random.randint(1, 3)
        dic['max_cons_days_off'] = min(random.randint(2*dic['min_cons_days_off']+1, 9), 7*num_time_periods)
        dic['max_working_week_ends'] = min(random.randint(round(num_time_periods*0.6), round(num_time_periods*0.75)), num_time_periods)
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
        #print(dic['skills'])
        nurses[nurse_id] = dic

    # poichè si fa solo giornaliero la cosa dei turni consecutivi e non per shift sta roba non serve

    # # minimum number of consecutive assignments
    # minimum_consecutive_assignment = {'morning' : random.randint(1, 5), 'afternoon' : random.randint(1, 5), 'night' : 1}

    # # maximum number of consecutive assignments
    # maximum_consecutive_assignment = {'morning' : random.randint(2*minimum_consecutive_assignment['morning'], 8), 'afternoon' : 2*random.randint(minimum_consecutive_assignment['afternoon'], 8), 'night' : 1}

    # matrix that represents the shifts succession that are forbidden
    forbidden_shifts_succession = {'Morning' : {'Morning' : False, 'Afternoon' : False , 'Night' : False},
                                'Afternoon' : {'Morning' : False, 'Afternoon' : False, 'Night' : False},
                                'Night' : {'Morning' : True, 'Afternoon' : True, 'Night' : True}

                                }

    # WEEK-DATA

    # single week: 7 days
    week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    days = [day + '-' + str(t) for t in range(num_time_periods) for day in week]

    # minimum and optimum number of nurses
    minimum_nurses = {}
    optimum_nurses = {}
    num_skills = len(skills)
    num_shifts = len(shift_types)
    range_for_shift = {"Morning": (max(num_nurses//(num_skills * num_shifts * 4), 1), int(1.4 * max(num_nurses//(num_skills * num_shifts * 4), 1))),
                       "Afternoon": (max(num_nurses//(num_skills * num_shifts * 4), 1), int(1.4 * max(num_nurses//(num_skills * num_shifts * 4), 1))),
                       "Night": (max(num_nurses//(num_skills * num_shifts * 5), 1), int(1.4 * max(num_nurses//(num_skills * num_shifts * 5), 1)))
                      }
    print("num_nurses", num_nurses)
    print("num_time_periods", num_time_periods)
    print("rfs", range_for_shift)
    for day in days:
        for shift in shift_types:
            for skill in skills:
                minimum_nurses[day, shift, skill] = random.randint(*range_for_shift[shift])
                optimum_nurses[day, shift, skill] = random.randint(minimum_nurses[day, shift, skill], minimum_nurses[day, shift, skill] + 2)


    # nurse requests: not to work that day in that shift
    permit_requests = []
    nr = int(num_nurses * num_time_periods / 4)
    num_requests = random.randint(nr//2, nr)

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
        dic['last_shift'] = ['Morning', 'Afternoon', 'Night', None, None][random.randint(0, 4)]
        if dic['last_shift'] is None:
            dic['num_cons_shift_sametype'] = 0
            dic['num_cons_shift'] = 0
            dic['num_cons_days_off'] = random.randint(1, 3)
        else:
            dic['num_cons_shift_sametype'] = random.randint(1, 3)
            dic['num_cons_shift'] = random.randint(dic['num_cons_shift_sametype'], 5)
            dic['num_cons_days_off'] = 0
        
        dic['num_worked_week_ends'] = random.randint(0, 1)
        dic['num_worked_shifts'] = random.randint(dic['num_worked_week_ends'], 8)

        history[nurse_id] = dic
    
    return history, nurses, contracts, days, minimum_nurses, forbidden_shifts_succession, optimum_nurses, permit_requests, shift_types, contract_types, skills

