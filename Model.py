from gurobipy import *
from Data import *

# model constructor
model = Model('Nurse_Competition')

# VARIABLE
nurses_ids = nurses.keys()
# variable which tell me if a nurse i is assigned to j shift in y day
assignment = model.addVars(nurses_ids, shift_types, days, vtype=GRB.BINARY, name='Assignment')

# HARD CONSTRAINTS 

# H1: SINGLE ASSIGNMENT PER DAY
# constraint that checks if the number of shifts is less equal to 1
model.addConstrs((quicksum(assignment[nurse_id, shift, day] for shift in shift_types) <= 1
                 for nurse_id in nurses_ids
                 for day in days), name='H1')


# H2:UNDERSTAFFING
# constraint that checks if the number of nurses is at least equal to the minimum one
model.addConstrs((quicksum(assignment[nurse_id, shift, day] for nurse_id in nurses_ids if skill in nurses[nurse_id]['skills']) >= minimum_nurses[day, shift, skill]
                 for shift in shift_types
                 for day in days
                 for skill in skills), name='H2')


# H3: SHIFT TYPE SUCCESSIONS
# constraint that checks if the assignment of a shift type in 2 consecutive days is legal
model.addConstrs(((assignment[nurse_id, shiftA, days[d]] + assignment[nurse_id, shiftB, days[d+1]] <= 1)
                for nurse_id in nurses_ids
                for d in range(len(days)-1) # to avoid out of bounds
                for shiftA in shift_types
                for shiftB in shift_types
                if forbidden_shifts_succession[shiftA][shiftB]), name='H3')

# SOFT CONSTRAINTS 

# S1: INSUFFICIENT STAFFING FOR OPTIMAL COVERAGE
use_penalty_S1 = model.addVars(shift_types, skills, days, vtype=GRB.BINARY, name='S1')
model.addConstrs(((use_penalty_S1[shift, skill, day] == 0) >> (quicksum(assignment[nurse_id, shift, day] for nurse_id in nurses_ids if skill in nurses[nurse_id]['skills']) >= optimum_nurses[day, shift, skill])
                                for shift in shift_types
                                for day in days
                                for skill in skills))

model.addConstrs(((use_penalty_S1[shift, skill, day] == 1) >> (quicksum(assignment[nurse_id, shift, day] for nurse_id in nurses_ids if skill in nurses[nurse_id]['skills']) <= optimum_nurses[day, shift, skill])
                                for shift in shift_types
                                for day in days
                                for skill in skills))

penalty_S1 = quicksum(use_penalty_S1[shift, skill, day] * (optimum_nurses[day, shift, skill] - quicksum(assignment[nurse_id, shift, day] for nurse_id in nurses_ids if skill in nurses[nurse_id]['skills']))
                                for shift in shift_types
                                for day in days
                                for skill in skills)


# S2: CONSECUTIVE ASSIGNMENTS
# binary variable that tell me if a nurse has worked that day
worked_day = model.addVars(nurses_ids, days, vtype=GRB.BINARY, name='Worked_Day')
# binary variable that tell me if a nurse should have worked that day
required_worked_day = model.addVars(nurses_ids, days, vtype=GRB.BINARY, name='Required_Worked_Day')

# contraint --> or
model.addConstrs(worked_day[nurse_id, day] >= assignment[nurse_id, shift, day]
                for nurse_id in nurses_ids
                for shift in shift_types
                for day in days)

# in case I have all 0 I want worked_day = 0
model.addConstrs(worked_day[nurse_id, days[d]] <= quicksum(assignment[nurse_id, shift, days[d]] for shift in shift_types) + assignment[nurse_id, 'night', days[d-1]]
                for nurse_id in nurses_ids
                for d in range(1, len(days)))

# contraint about nights: a night is equal to two consecutive days
model.addConstrs(worked_day[nurse_id, days[d+1]] >= assignment[nurse_id, 'night', days[d]]
                for nurse_id in nurses_ids
                for d in range(len(days) - 1))

# contraints that link the two biry variables: worked_day and required_worked_day
model.addConstrs(required_worked_day[nurse_id, day] >= worked_day[nurse_id, day]
                for nurse_id in nurses_ids
                for day in days)

# contraint that controls the minimum number of consecutive working days
# case: 0 --> 1 so when the nurse starts to work
model.addConstrs(required_worked_day[nurse_id, days[d+n]] >= (required_worked_day[nurse_id, days[d]] - required_worked_day[nurse_id, days[d-1]])
                for nurse_id in nurses_ids
                for n in range(0, contracts[nurses[nurse_id]['contract_type']]['min_cons_working_days'])
                for d in range(1, len(days) - n))

penalty_S2_min = quicksum(required_worked_day[nurse_id, day] - worked_day[nurse_id, day]
                        for nurse_id in nurses_ids
                        for day in days)


# TODO: contraint that controls the maximum number of consecutive working days --> S2 MAX

# S3: CONSECUTIVE DAYS OFF
required_day_off = model.addVars(nurses_ids, days, vtype=GRB.BINARY, name='Required_Day_Off')

# contraints that link the two biry variables: worked_day and required_day_off
model.addConstrs(required_day_off[nurse_id, day] >= (1 - worked_day[nurse_id, day])
                for nurse_id in nurses_ids
                for day in days)

# contraint that controls the minimum number of consecutive days off
# case: 1 --> 0 so when the nurse ends to work
model.addConstrs(required_day_off[nurse_id, days[d+n]] >= (required_day_off[nurse_id, days[d]] - required_day_off[nurse_id, days[d-1]])
                for nurse_id in nurses_ids
                for n in range(0, contracts[nurses[nurse_id]['contract_type']]['min_cons_days_off'])
                for d in range(1, len(days) - n))

penalty_S3_min = quicksum(required_day_off[nurse_id, day] - (1 - worked_day[nurse_id, day])
                        for nurse_id in nurses_ids
                        for day in days)

# TODO: constraint that controls the maximum number of consecutive days off --> S3 MAX

# S4: PREFERENCES 
penalty_S4 = quicksum(assignment[nurse_id, shift, day] for (nurse_id, day, shift) in permit_requests)


# S5: COMPLETE WEEK-END
saturdays = [d for d in range(len(days)) if "Saturday" in days[d]]
nurses_complete_weekends = [n for n in nurses_ids if contracts[nurses[n]['contract_type']]['complete_week_ends']]
worked_only_saturday = model.addVars(nurses_complete_weekends, saturdays, vtype=GRB.BINARY, name='Worked_Only_Saturday')
worked_only_sunday = model.addVars(nurses_complete_weekends, saturdays, vtype=GRB.BINARY, name='Worked_Only_Sunday')

model.addConstrs(worked_only_saturday[nurse_id, d] >= (worked_day[nurse_id, days[d]] - worked_day[nurse_id, days[d+1]]) for nurse_id in nurses_complete_weekends for d in saturdays)
model.addConstrs(worked_only_sunday[nurse_id, d] >= (worked_day[nurse_id, days[d+1]] - worked_day[nurse_id, days[d]]) for nurse_id in nurses_complete_weekends for d in saturdays)

penalty_S5 = quicksum(worked_only_saturday[nurse_id, d] + worked_only_sunday[nurse_id, d] for nurse_id in nurses_complete_weekends for d in saturdays)


# S6: TOTAL ASSIGNMENTS
use_penalty_S6_min = model.addVars(nurses_ids, vtype=GRB.BINARY, name='S6_min')
use_penalty_S6_max = model.addVars(nurses_ids, vtype=GRB.BINARY, name='S6_max')

model.addConstrs((use_penalty_S6_min[nurse_id] == 0) >> 
        ((quicksum(assignment[nurse_id, shift, day] for shift in shift_types for day in days))
            >= contracts[nurses[nurse_id]['contract_type']]['min_assignments']
        )
        for nurse_id in nurses_ids
)
model.addConstrs((use_penalty_S6_min[nurse_id] == 1) >> 
        ((quicksum(assignment[nurse_id, shift, day] for shift in shift_types for day in days))
            <= contracts[nurses[nurse_id]['contract_type']]['min_assignments']
        )
        for nurse_id in nurses_ids
)

model.addConstrs((use_penalty_S6_max[nurse_id] == 0) >> 
        ((quicksum(assignment[nurse_id, shift, day] for shift in shift_types for day in days))
            <= contracts[nurses[nurse_id]['contract_type']]['max_assignments']
        )
        for nurse_id in nurses_ids
)
model.addConstrs((use_penalty_S6_max[nurse_id] == 1) >> 
        ((quicksum(assignment[nurse_id, shift, day] for shift in shift_types for day in days))
            >= contracts[nurses[nurse_id]['contract_type']]['max_assignments']
        )
        for nurse_id in nurses_ids
)

penalty_S6_min = quicksum(use_penalty_S6_min[nurse_id] * 
        (contracts[nurses[nurse_id]['contract_type']]['min_assignments'] 
                - (quicksum(assignment[nurse_id, shift, day] for shift in shift_types for day in days))
        )
        for nurse_id in nurses_ids
)
        
penalty_S6_max = quicksum(use_penalty_S6_max[nurse_id] * 
        ((quicksum(assignment[nurse_id, shift, day] for shift in shift_types for day in days))
                - contracts[nurses[nurse_id]['contract_type']]['max_assignments']
        )

        for nurse_id in nurses_ids
)
        
#S7: TOTAL WORKING WEEK-ENDS
# binary variable, for each nurse and each weekend, which is one if the nurse worked both Saturday and Sunday
worked_weekend = model.addVars(nurses_ids, saturdays, vtype=GRB.BINARY, name='Worked_Weekend')
model.addConstrs(worked_weekend[nurse_id, d] >= assignment[nurse_id, shift, days[d]] 
                for shift in shift_types
                for nurse_id in nurses_ids
                for d in saturdays
)

model.addConstrs(worked_weekend[nurse_id, d] >= assignment[nurse_id, shift, days[d+1]] 
                for shift in shift_types
                for nurse_id in nurses_ids
                for d in saturdays
)

use_penalty_S7 = model.addVars(nurses_ids, vtype=GRB.BINARY)

model.addConstrs((use_penalty_S7[nurse_id] == 0) >> (quicksum(worked_weekend[nurse_id, d] for d in saturdays) 
        <= contracts[nurses[nurse_id]['contract_type']]['max_working_week_ends'])
                for nurse_id in nurses_ids
)
model.addConstrs((use_penalty_S7[nurse_id] == 1) >> (quicksum(worked_weekend[nurse_id, d] for d in saturdays) 
        >= contracts[nurses[nurse_id]['contract_type']]['max_working_week_ends'])
                for nurse_id in nurses_ids
)

penalty_S7 = quicksum(use_penalty_S7[nurse_id] * (quicksum(worked_weekend[nurse_id, d] for d in saturdays) - 
               contracts[nurses[nurse_id]['contract_type']]['max_working_week_ends'])
               for nurse_id in nurses_ids)

# OBJECTIVE FUNCTION
#obj = 0 + lambdaS1 * penalty_S1 + lambdaS2_min * penalty_S2_min + lambdaS3 * penalty_S3_min + lambdaS4 * penalty_S4 + lambdaS5 * penalty_S5 + lambdaS6 * penalty_S6_min + lambdaS6 * penalty_S6_max + lambdaS7 * penalty_S7
obj = lambdaS2_min * penalty_S2_min + lambdaS3 * penalty_S3_min + lambdaS4 * penalty_S4 + lambdaS5 * penalty_S5 + lambdaS7 * penalty_S7
model.setObjective(obj, GRB.MINIMIZE)
model.optimize()

# total_assignements = 0
# for v in model.getVars():
#     #if v.X != 0:
#     #if "Worked_Day" in v.Varname and "Required" not in v.Varname and v.X == 0:
#         print("%s %f\n" % (v.Varname, v.X))
#     #if "Assignment" in v.Varname:
#     #    total_assignements += v.X

#print("total_assignements: " + str(total_assignements))

# OUTPUT SOLUTION FILE
model.write("nurse-competition-output.sol")

