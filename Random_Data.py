import random
import names
import copy
# SCENARIO

# time horizon: 2 weeks
num_time_periods = 2
num_nurses = 100

# shift types list
shift_types = ['morning', 'afternoon', 'night']

# contract types list
contract_types = ['full_time', 'part_time', 'on_call']

# skills list
skills = ['head_nurse', 'regular_nurse', 'trainee']

# weights
lambdaS1 = 30
lambdaS2_min = 15
lambdaS2_max = 30
lambdaS3 = 30
lambdaS4 = 10
lambdaS5 = 30
lambdaS6 = 20
lambdaS7 = 30

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
    num_skills = random.randint(1, len(skills)-1)
    sk = copy.deepcopy(skills)
    random.shuffle(sk)
    dic['skills'] = sk[:num_skills]
    nurses[nurse_id] = dic


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
