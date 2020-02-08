# time horizon: 2 weeks
num_time_periods = 2

# shift types list
shift_types = ['morning', 'afternoon', 'night']

# contract types list
contract_types = ['full_time', 'part_time', 'on_call']

# contracts details
contracts = {'full_time': {'min_assignments': 5, 'max_assignments': 12, 'min_cons_working_days': 1, 'max_cons_working_days': 5,
                            'min_cons_days_off': 1, 'max_cons_days_off': 6, 'max_working_week_ends': 2, 'complete_week_ends': False},
            'part_time': {'min_assignments': 8, 'max_assignments': 12, 'min_cons_working_days': 2, 'max_cons_working_days': 6,
                            'min_cons_days_off': 1, 'max_cons_days_off': 5, 'max_working_week_ends': 2, 'complete_week_ends': True},
            'on_call': {'min_assignments': 0, 'max_assignments': 5, 'min_cons_working_days': 1, 'max_cons_working_days': 5,
                            'min_cons_days_off': 1, 'max_cons_days_off': 14, 'max_working_week_ends': 2, 'complete_week_ends': False}
            }

# skills list
skills = ['head_nurse', 'regular_nurse', 'trainee']

nurses = {0 : {'name': 'Tina', 'contract_type': 'full_time', 'skills': ['head_nurse', 'regular_nurse']},
          1 : {'name': 'Giovanna', 'contract_type': 'part_time', 'skills': ['regular_nurse']},
          2 : {'name': 'Ilaria', 'contract_type': 'on_call', 'skills': ['trainee']},
          3 : {'name': 'Umberto', 'contract_type': 'full_time', 'skills': ['regular_nurse']},
          4 : {'name': 'Ugo', 'contract_type': 'part_time', 'skills': ['trainee']},
          5 : {'name': 'Francesca', 'contract_type': 'full_time', 'skills': ['trainee']},
          6 : {'name': 'Gilberto', 'contract_type': 'full_time', 'skills': ['head_nurse']},
          7 : {'name': 'Elena', 'contract_type': 'part_time', 'skills': ['regular_nurse']},
          8 : {'name': 'Maria', 'contract_type': 'part_time', 'skills': ['trainee']},
          9 : {'name': 'Paolo', 'contract_type': 'on_call', 'skills': ['regular_nurse', 'trainee']},
          10 : {'name': 'Roberta', 'contract_type': 'part_time', 'skills': ['regular_nurse']}
}

# minimum number of consecutive assignments
minimum_consecutive_assignment = {'morning' : 2, 'afternoon' : 3, 'night' : 1}

# maximum number of consecutive assignments
maximum_consecutive_assignment = {'morning' : 3, 'afternoon' : 4, 'night' : 1}

# matrix that represents the shifts succession that are forbidden
forbidden_shifts_succession = {'morning' : {'morning' : False, 'afternoon' : False , 'night' : False},
                               'afternoon' : {'morning' : False, 'afternoon' : False, 'night' : False},
                               'night' : {'morning' : True, 'afternoon' : True, 'night' : True}

                            }

optimum_nurses = {
    ('Monday-0', 'morning', 'head_nurse'): 1,
    ('Monday-0', 'morning', 'regular_nurse'): 4,
    ('Monday-0', 'morning', 'trainee'): 3,
    ('Monday-0', 'afternoon', 'head_nurse'): 1,
    ('Monday-0', 'afternoon', 'regular_nurse'): 4,
    ('Monday-0', 'afternoon', 'trainee'): 3,
    ('Monday-0', 'night', 'head_nurse'): 1,
    ('Monday-0', 'night', 'regular_nurse'): 4,
    ('Monday-0', 'night', 'trainee'): 5,
    ('Tuesday-0', 'morning', 'head_nurse'): 1,
    ('Tuesday-0', 'morning', 'regular_nurse'): 5,
    ('Tuesday-0', 'morning', 'trainee'): 2,
    ('Tuesday-0', 'afternoon', 'head_nurse'): 1,
    ('Tuesday-0', 'afternoon', 'regular_nurse'): 4,
    ('Tuesday-0', 'afternoon', 'trainee'): 2,
    ('Tuesday-0', 'night', 'head_nurse'): 1,
    ('Tuesday-0', 'night', 'regular_nurse'): 5,
    ('Tuesday-0', 'night', 'trainee'): 5,
    ('Wednesday-0', 'morning', 'head_nurse'): 1,
    ('Wednesday-0', 'morning', 'regular_nurse'): 4,
    ('Wednesday-0', 'morning', 'trainee'): 2,
    ('Wednesday-0', 'afternoon', 'head_nurse'): 1,
    ('Wednesday-0', 'afternoon', 'regular_nurse'): 2,
    ('Wednesday-0', 'afternoon', 'trainee'): 3,
    ('Wednesday-0', 'night', 'head_nurse'): 1,
    ('Wednesday-0', 'night', 'regular_nurse'): 5,
    ('Wednesday-0', 'night', 'trainee'): 4,
    ('Thursday-0', 'morning', 'head_nurse'): 1,
    ('Thursday-0', 'morning', 'regular_nurse'): 5,
    ('Thursday-0', 'morning', 'trainee'): 3,
    ('Thursday-0', 'afternoon', 'head_nurse'): 1,
    ('Thursday-0', 'afternoon', 'regular_nurse'): 3,
    ('Thursday-0', 'afternoon', 'trainee'): 5,
    ('Thursday-0', 'night', 'head_nurse'): 1,
    ('Thursday-0', 'night', 'regular_nurse'): 5,
    ('Thursday-0', 'night', 'trainee'): 3,
    ('Friday-0', 'morning', 'head_nurse'): 1,
    ('Friday-0', 'morning', 'regular_nurse'): 5,
    ('Friday-0', 'morning', 'trainee'): 4,
    ('Friday-0', 'afternoon', 'head_nurse'): 1,
    ('Friday-0', 'afternoon', 'regular_nurse'): 5,
    ('Friday-0', 'afternoon', 'trainee'): 4,
    ('Friday-0', 'night', 'head_nurse'): 1,
    ('Friday-0', 'night', 'regular_nurse'): 2,
    ('Friday-0', 'night', 'trainee'): 5,
    ('Saturday-0', 'morning', 'head_nurse'): 1,
    ('Saturday-0', 'morning', 'regular_nurse'): 4,
    ('Saturday-0', 'morning', 'trainee'): 4,
    ('Saturday-0', 'afternoon', 'head_nurse'): 1,
    ('Saturday-0', 'afternoon', 'regular_nurse'): 5,
    ('Saturday-0', 'afternoon', 'trainee'): 5,
    ('Saturday-0', 'night', 'head_nurse'): 1,
    ('Saturday-0', 'night', 'regular_nurse'): 4,
    ('Saturday-0', 'night', 'trainee'): 4,
    ('Sunday-0', 'morning', 'head_nurse'): 1,
    ('Sunday-0', 'morning', 'regular_nurse'): 3,
    ('Sunday-0', 'morning', 'trainee'): 4,
    ('Sunday-0', 'afternoon', 'head_nurse'): 1,
    ('Sunday-0', 'afternoon', 'regular_nurse'): 2,
    ('Sunday-0', 'afternoon', 'trainee'): 4,
    ('Sunday-0', 'night', 'head_nurse'): 1,
    ('Sunday-0', 'night', 'regular_nurse'): 2,
    ('Sunday-0', 'night', 'trainee'): 2
}

minimum_nurses = {
    ('Monday-0', 'morning', 'head_nurse'): 1,
    ('Monday-0', 'morning', 'regular_nurse'): 1,
    ('Monday-0', 'morning', 'trainee'): 2,
    ('Monday-0', 'afternoon', 'head_nurse'): 1,
    ('Monday-0', 'afternoon', 'regular_nurse'): 2,
    ('Monday-0', 'afternoon', 'trainee'): 1,
    ('Monday-0', 'night', 'head_nurse'): 1,
    ('Monday-0', 'night', 'regular_nurse'): 1,
    ('Monday-0', 'night', 'trainee'): 1,
    ('Tuesday-0', 'morning', 'head_nurse'): 1,
    ('Tuesday-0', 'morning', 'regular_nurse'): 2,
    ('Tuesday-0', 'morning', 'trainee'): 2,
    ('Tuesday-0', 'afternoon', 'head_nurse'): 1,
    ('Tuesday-0', 'afternoon', 'regular_nurse'): 1,
    ('Tuesday-0', 'afternoon', 'trainee'): 2,
    ('Tuesday-0', 'night', 'head_nurse'): 1,
    ('Tuesday-0', 'night', 'regular_nurse'): 2,
    ('Tuesday-0', 'night', 'trainee'): 2,
    ('Wednesday-0', 'morning', 'head_nurse'): 1,
    ('Wednesday-0', 'morning', 'regular_nurse'): 2,
    ('Wednesday-0', 'morning', 'trainee'): 2,
    ('Wednesday-0', 'afternoon', 'head_nurse'): 1,
    ('Wednesday-0', 'afternoon', 'regular_nurse'): 1,
    ('Wednesday-0', 'afternoon', 'trainee'): 1,
    ('Wednesday-0', 'night', 'head_nurse'): 1,
    ('Wednesday-0', 'night', 'regular_nurse'): 1,
    ('Wednesday-0', 'night', 'trainee'): 2,
    ('Thursday-0', 'morning', 'head_nurse'): 1,
    ('Thursday-0', 'morning', 'regular_nurse'): 2,
    ('Thursday-0', 'morning', 'trainee'): 2,
    ('Thursday-0', 'afternoon', 'head_nurse'): 1,
    ('Thursday-0', 'afternoon', 'regular_nurse'): 1,
    ('Thursday-0', 'afternoon', 'trainee'): 2,
    ('Thursday-0', 'night', 'head_nurse'): 1,
    ('Thursday-0', 'night', 'regular_nurse'): 2,
    ('Thursday-0', 'night', 'trainee'): 1,
    ('Friday-0', 'morning', 'head_nurse'): 1,
    ('Friday-0', 'morning', 'regular_nurse'): 2,
    ('Friday-0', 'morning', 'trainee'): 2,
    ('Friday-0', 'afternoon', 'head_nurse'): 1,
    ('Friday-0', 'afternoon', 'regular_nurse'): 2,
    ('Friday-0', 'afternoon', 'trainee'): 2,
    ('Friday-0', 'night', 'head_nurse'): 1,
    ('Friday-0', 'night', 'regular_nurse'): 1,
    ('Friday-0', 'night', 'trainee'): 2,
    ('Saturday-0', 'morning', 'head_nurse'): 1,
    ('Saturday-0', 'morning', 'regular_nurse'): 1,
    ('Saturday-0', 'morning', 'trainee'): 2,
    ('Saturday-0', 'afternoon', 'head_nurse'): 1,
    ('Saturday-0', 'afternoon', 'regular_nurse'): 2,
    ('Saturday-0', 'afternoon', 'trainee'): 2,
    ('Saturday-0', 'night', 'head_nurse'): 1,
    ('Saturday-0', 'night', 'regular_nurse'): 2,
    ('Saturday-0', 'night', 'trainee'): 1,
    ('Sunday-0', 'morning', 'head_nurse'): 1,
    ('Sunday-0', 'morning', 'regular_nurse'): 1,
    ('Sunday-0', 'morning', 'trainee'): 2,
    ('Sunday-0', 'afternoon', 'head_nurse'): 1,
    ('Sunday-0', 'afternoon', 'regular_nurse'): 1,
    ('Sunday-0', 'afternoon', 'trainee'): 2,
    ('Sunday-0', 'night', 'head_nurse'): 1,
    ('Sunday-0', 'night', 'regular_nurse'): 1,
    ('Sunday-0', 'night', 'trainee'): 1
}

permit_requests = [(0, 'Saturday-0', 'morning'),
                   (0, 'Saturday-0', 'afternoon'),
                   (0, 'Saturday-0', 'night'),
                   (1, 'Monday-0', 'morning'),
                   (2, 'Tuesday-0', 'afternoon'),
                   (3, 'Friday-0', 'night'),
                   (4, 'Sunday-0', 'morning'),
                   (5, 'Wednesday-0', 'afternoon'),
                   (6, 'Thursday-0', 'morning'),
                   (7, 'Monday-0', 'afternoon'),
                   (8, 'Friday-0', 'morning'),
                   (9, 'Sunday-0', 'night'),
                   (10, 'Thursday-0', 'morning'),
                   (10, 'Thursday-0', 'afternoon'),
                   (10, 'Thursday-0', 'night')
]

history = {0 : {'last_shift': 'morning', 'num_cons_shift': 2, 'num_cons_shift_sametype': 2, 'num_cons_days_off': 0, 'num_worked_shifts': 6, 'num_worked_week_ends': 2},
          1 : {'last_shift': None, 'num_cons_shift': 0, 'num_cons_shift_sametype': 0, 'num_cons_days_off': 1, 'num_worked_shifts': 1, 'num_worked_week_ends': 1},
          2 : {'last_shift': 'afternoon', 'num_cons_shift': 1, 'num_cons_shift_sametype': 1, 'num_cons_days_off': 0, 'num_worked_shifts': 4, 'num_worked_week_ends': 2},
          3 : {'last_shift': 'morning', 'num_cons_shift': 3, 'num_cons_shift_sametype': 2, 'num_cons_days_off': 0, 'num_worked_shifts': 7, 'num_worked_week_ends': 1},
          4 : {'last_shift': None, 'num_cons_shift': 0, 'num_cons_shift_sametype': 0, 'num_cons_days_off': 3, 'num_worked_shifts': 3, 'num_worked_week_ends': 0},
          5 : {'last_shift': 'morning', 'num_cons_shift': 2, 'num_cons_shift_sametype': 2, 'num_cons_days_off': 0, 'num_worked_shifts': 8, 'num_worked_week_ends': 2},
          6 : {'last_shift': 'afternoon', 'num_cons_shift': 3, 'num_cons_shift_sametype': 1, 'num_cons_days_off': 0, 'num_worked_shifts': 9, 'num_worked_week_ends': 2},
          7 : {'last_shift': 'morning', 'num_cons_shift': 3, 'num_cons_shift_sametype': 1, 'num_cons_days_off': 0, 'num_worked_shifts': 5, 'num_worked_week_ends': 2},
          8 : {'last_shift': 'night', 'num_cons_shift': 3, 'num_cons_shift_sametype': 1, 'num_cons_days_off': 0, 'num_worked_shifts': 3, 'num_worked_week_ends': 3},
          9 : {'last_shift': 'afternoon', 'num_cons_shift': 4, 'num_cons_shift_sametype': 2, 'num_cons_days_off': 0, 'num_worked_shifts': 7, 'num_worked_week_ends': 2},
          10 : {'last_shift': 'morning', 'num_cons_shift': 3, 'num_cons_shift_sametype': 2, 'num_cons_days_off': 0, 'num_worked_shifts': 3, 'num_worked_week_ends': 3}
}