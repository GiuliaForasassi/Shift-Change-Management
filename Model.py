from gurobipy import *
import datetime
from beautifultable import BeautifulTable
from timeit import default_timer as timer
import os

from Constants import *
from Random_Data import *
from Preprocessing import *
from Read_Data import read_data

def runRealData(num_nurses, num_time_periods, max_time=None, id_h=0, id_first_w=0):
        history, nurses, contracts, days, minimum_nurses, forbidden_shifts_succession, optimum_nurses, permit_requests, shift_types, contract_types, skills = read_data(num_nurses, num_time_periods, id_h, id_first_w)
        return runM(history, nurses, contracts, days, minimum_nurses, forbidden_shifts_succession, optimum_nurses, permit_requests, shift_types, contract_types, skills, max_time)

def runGRD(num_nurses, num_time_periods, max_time=None):
        history, nurses, contracts, days, minimum_nurses, forbidden_shifts_succession, optimum_nurses, permit_requests, shift_types, contract_types, skills = generate_random_data(num_nurses, num_time_periods)
        return runM(history, nurses, contracts, days, minimum_nurses, forbidden_shifts_succession, optimum_nurses, permit_requests, shift_types, contract_types, skills, max_time)
        
def runM(history, nurses, contracts, days, minimum_nurses, forbidden_shifts_succession, optimum_nurses, permit_requests, shift_types, contract_types, skills, max_time=None):
        lambdaS1, lambdaS2_min, lambdaS2_max, lambdaS3, lambdaS4, lambdaS5, lambdaS6, lambdaS7 = get_constants()
        start = timer()
        history = preprocess_history(history, contracts, nurses)

        # model constructor
        model = Model('Nurse_Competition')

        # VARIABLE
        nurses_ids = nurses.keys()
        # variable which tell me if a nurse i is assigned to j shift in y day
        assignment = model.addVars(nurses_ids, shift_types, days, vtype=GRB.BINARY, name='Assignment')

        # HARD CONSTRAINTS 

        '''H1'''
        # H1: SINGLE ASSIGNMENT PER DAY
        # constraint that checks if the number of shifts is less equal to 1
        model.addConstrs((quicksum(assignment[nurse_id, shift, day] for shift in shift_types) <= 1
                        for nurse_id in nurses_ids
                        for day in days), name='H1')

        '''H2'''
        # H2:UNDERSTAFFING
        # constraint that checks if the number of nurses is at least equal to the minimum one
        model.addConstrs((quicksum(assignment[nurse_id, shift, day] for nurse_id in nurses_ids if skill in nurses[nurse_id]['skills']) >= minimum_nurses[day, shift, skill]
                        for shift in shift_types
                        for day in days
                        for skill in skills), name='H2')

        '''H3'''
        # H3: SHIFT TYPE SUCCESSIONS
        # constraint that checks if the assignment of a shift type in 2 consecutive days is legal
        model.addConstrs(((assignment[nurse_id, shiftA, days[d]] + assignment[nurse_id, shiftB, days[d+1]] <= 1)
                        for nurse_id in nurses_ids
                        for d in range(len(days)-1) # to avoid out of bound
                        for shiftA in shift_types
                        for shiftB in shift_types
                        if forbidden_shifts_succession[shiftA][shiftB]), name='H3')

        # SOFT CONSTRAINTS 

        '''S1'''
        # S1: INSUFFICIENT STAFFING FOR OPTIMAL COVERAGE
        penalty_S1 = model.addVars(shift_types, skills, days, vtype=GRB.INTEGER, name='S1')

        model.addConstrs(penalty_S1[shift, skill, day] >= 0 for shift in shift_types for skill in skills for day in days)

        # when the costraint is not respected 
        model.addConstrs((penalty_S1[shift, skill, day] >= (optimum_nurses[day, shift, skill] - quicksum(assignment[nurse_id, shift, day]
                        for nurse_id in nurses_ids if skill in nurses[nurse_id]['skills']))) for skill in skills for shift in shift_types for day in days)

        penalty_S1_tot = quicksum(penalty_S1[shift, skill, day] for shift in shift_types for skill in skills for day in days)


        # S2: CONSECUTIVE ASSIGNMENTS
        # binary variable that tell me if a nurse has worked that day
        worked_day = model.addVars(nurses_ids, days, vtype=GRB.BINARY, name='Worked_Day')
        # binary variable that tell me if a nurse should have worked that day
        required_worked_day = model.addVars(nurses_ids, days, vtype=GRB.BINARY, name='Required_Worked_Day')

        '''S2 MIN'''
        # S2 MIN
        # contraint --> or
        model.addConstrs(worked_day[nurse_id, day] >= assignment[nurse_id, shift, day]
                        for nurse_id in nurses_ids
                        for shift in shift_types
                        for day in days)

        # in case I have all 0 I want worked_day = 0
        model.addConstrs(worked_day[nurse_id, days[d]] <= quicksum(assignment[nurse_id, shift, days[d]] for shift in shift_types)# + assignment[nurse_id, 'Night', days[d-1]]
                        for nurse_id in nurses_ids
                        for d in range(1, len(days)))

        # # contraint about nights: a night is equal to two consecutive days
        # model.addConstrs(worked_day[nurse_id, days[d+1]] >= assignment[nurse_id, 'Night', days[d]]
        #                 for nurse_id in nurses_ids
        #                 for d in range(len(days) - 1))

        # contraints that link the two binary variables: worked_day and required_worked_day
        model.addConstrs(required_worked_day[nurse_id, day] >= worked_day[nurse_id, day]
                        for nurse_id in nurses_ids
                        for day in days)

        # contraint that controls the minimum number of consecutive working days
        # case: 0 --> 1 so when the nurse starts to work
        model.addConstrs(required_worked_day[nurse_id, days[d+n]] >= (required_worked_day[nurse_id, days[d]] - required_worked_day[nurse_id, days[d-1]])
                        for nurse_id in nurses_ids
                        for n in range(0, contracts[nurses[nurse_id]['contract_type']]['min_cons_working_days'])
                        for d in range(1, len(days) - n))

        # case in which the first day the nurse works
        model.addConstrs(required_worked_day[nurse_id, days[n]] >= required_worked_day[nurse_id, days[0]]
                        for nurse_id in nurses_ids
                        for n in range(1, contracts[nurses[nurse_id]['contract_type']]['min_cons_working_days'] - history[nurse_id]['num_cons_shift']))

        # constraint that manage the case in which there are a number of worked days < min_worked_days
        # if in the next assignement are all 0, I have to pay 
        model.addConstrs(required_worked_day[nurse_id, days[0]] == 1
                        for nurse_id in nurses_ids
                        if 0 < history[nurse_id]['num_cons_shift'] < contracts[nurses[nurse_id]['contract_type']]['min_cons_working_days'])

        penalty_S2_min_tot = quicksum(required_worked_day[nurse_id, day] - worked_day[nurse_id, day]
                                for nurse_id in nurses_ids
                                for day in days)

        '''S2 MAX'''
        # S2 MAX 
        # constraint that controls the maximum number of consecutive working days --> S2 MAX
        penalty_S2_max = model.addVars(nurses_ids, days, vtype=GRB.BINARY)
        # constraints that manage the new assignments (not the history)
        model.addConstrs((penalty_S2_max[nurse_id, days[d]] >= (quicksum(worked_day[nurse_id, days[i]] for i in range(d - contracts[nurses[nurse_id]['contract_type']]['max_cons_working_days'], d+1))
                                                - contracts[nurses[nurse_id]['contract_type']]['max_cons_working_days']))
                                                for nurse_id in nurses_ids
                                                for d in range(contracts[nurses[nurse_id]['contract_type']]['max_cons_working_days'], len(days)))

        # constraints that manage the history
        # this constraint enforce the first penalty to be 1 when history==max and worked_day[0]==1
        for nurse_id in nurses_ids:
                if history[nurse_id]['num_cons_shift'] > 0:
                        m = contracts[nurses[nurse_id]['contract_type']]['max_cons_working_days']
                        h = history[nurse_id]['num_cons_shift']
                        model.addConstr(penalty_S2_max[nurse_id, days[m-h]] >= (h - m + quicksum(worked_day[nurse_id, days[g]] for g in range(0, m-h+1))))

                        # this constraint enforce the penalty to be 1 when the previous penalty is 1 and the related worked_day is 1
                        model.addConstrs((penalty_S2_max[nurse_id, days[d]] >= worked_day[nurse_id, days[d]] + penalty_S2_max[nurse_id, days[d-1]] - 1)
                                                                for d in range(m-h+1, m))

        penalty_S2_max_tot = quicksum(penalty_S2_max[nurse_id, day] for nurse_id in nurses_ids for day in days)

        # S3: CONSECUTIVE DAYS OFF
        required_day_off = model.addVars(nurses_ids, days, vtype=GRB.BINARY, name='Required_Day_Off')

        '''S3 MIN'''
        # S3 MIN
        # constraints that link the two binary variables: worked_day and required_day_off
        model.addConstrs(required_day_off[nurse_id, day] >= (1 - worked_day[nurse_id, day])
                        for nurse_id in nurses_ids
                        for day in days)

        # constraint that controls the minimum number of consecutive days off
        # case: 1 --> 0 so when the nurse ends to work
        model.addConstrs(required_day_off[nurse_id, days[d+n]] >= (required_day_off[nurse_id, days[d]] - required_day_off[nurse_id, days[d-1]])
                        for nurse_id in nurses_ids
                        for n in range(0, contracts[nurses[nurse_id]['contract_type']]['min_cons_days_off'])
                        for d in range(1, len(days) - n))

        model.addConstrs(required_day_off[nurse_id, days[n]] >= required_day_off[nurse_id, days[0]]
                        for nurse_id in nurses_ids
                        for n in range(0, contracts[nurses[nurse_id]['contract_type']]['min_cons_days_off'] - history[nurse_id]['num_cons_days_off']))

        # constraint that manage the case in which there are a number of days-off (history) < min_days_off
        # if in the next assignement are all 1, I have to pay 
        model.addConstrs(required_day_off[nurse_id, days[0]] == 1
                        for nurse_id in nurses_ids
                        if 0 < history[nurse_id]['num_cons_days_off'] < contracts[nurses[nurse_id]['contract_type']]['min_cons_days_off'])

        penalty_S3_min = quicksum(required_day_off[nurse_id, day] - (1 - worked_day[nurse_id, day])
                                for nurse_id in nurses_ids
                                for day in days)

        '''S3 MAX'''
        # S3 MAX
        # constraint that controls the maximum number of consecutive days off --> S3 MAX
        penalty_S3_max = model.addVars(nurses_ids, days, vtype=GRB.BINARY)
        model.addConstrs((penalty_S3_max[nurse_id, days[d]] >= (quicksum(1 - worked_day[nurse_id, days[i]] for i in range(d - contracts[nurses[nurse_id]['contract_type']]['max_cons_days_off'], d+1))
                                                - contracts[nurses[nurse_id]['contract_type']]['max_cons_days_off']))
                                                for nurse_id in nurses_ids
                                                for d in range(contracts[nurses[nurse_id]['contract_type']]['max_cons_days_off'], len(days)))

        # constraints that manage the history
        # this constraint enforce the first penalty to be 1 when history==max and worked_day[0]==0
        for nurse_id in nurses_ids:
                if history[nurse_id]['num_cons_days_off'] > 0:
                        m = contracts[nurses[nurse_id]['contract_type']]['max_cons_days_off']
                        h = history[nurse_id]['num_cons_days_off']
                        model.addConstr(penalty_S3_max[nurse_id, days[m-h]] >= (h - m + quicksum(1 - worked_day[nurse_id, days[g]] for g in range(0, m-h+1))))

                        # this constraint enforce the penalty to be 1 when the previous penalty is 1 and the related worked_day is 1
                        model.addConstrs((penalty_S3_max[nurse_id, days[d]] >= (1 - worked_day[nurse_id, days[d]]) + penalty_S3_max[nurse_id, days[d-1]] - 1)
                                                                for d in range(m-h+1, m))
        
        penalty_S3_max_tot = quicksum(penalty_S3_max[nurse_id, day] for nurse_id in nurses_ids for day in days)

        '''S4'''
        # S4: PREFERENCES 
        penalty_S4 = quicksum(assignment[nurse_id, shift, day] for (nurse_id, day, shift) in permit_requests)

        '''S5'''
        # S5: COMPLETE WEEK-END
        saturdays = [d for d in range(len(days)) if "Saturday" in days[d]]
        nurses_complete_weekends = [n for n in nurses_ids if contracts[nurses[n]['contract_type']]['complete_week_ends']]
        worked_only_saturday = model.addVars(nurses_complete_weekends, saturdays, vtype=GRB.BINARY, name='Worked_Only_Saturday')
        worked_only_sunday = model.addVars(nurses_complete_weekends, saturdays, vtype=GRB.BINARY, name='Worked_Only_Sunday')

        model.addConstrs(worked_only_saturday[nurse_id, d] >= (worked_day[nurse_id, days[d]] - worked_day[nurse_id, days[d+1]]) for nurse_id in nurses_complete_weekends for d in saturdays)
        model.addConstrs(worked_only_sunday[nurse_id, d] >= (worked_day[nurse_id, days[d+1]] - worked_day[nurse_id, days[d]]) for nurse_id in nurses_complete_weekends for d in saturdays)

        penalty_S5 = quicksum(worked_only_saturday[nurse_id, d] + worked_only_sunday[nurse_id, d] for nurse_id in nurses_complete_weekends for d in saturdays)

        '''S6'''
        # S6: TOTAL ASSIGNMENTS
        penalty_S6 = model.addVars(nurses_ids, vtype=GRB.INTEGER, name='S6_min')

        model.addConstrs(penalty_S6[nurse_id] >= 0 for nurse_id in nurses_ids)
        model.addConstrs(penalty_S6[nurse_id] >= (contracts[nurses[nurse_id]['contract_type']]['min_assignments'] 
                        - quicksum(worked_day[nurse_id, day] for day in days))
                        for nurse_id in nurses_ids)
                        
        model.addConstrs(penalty_S6[nurse_id] >= (quicksum(worked_day[nurse_id, day] for day in days) 
                        - contracts[nurses[nurse_id]['contract_type']]['max_assignments'])
                        for nurse_id in nurses_ids)

        penalty_S6_tot = quicksum(penalty_S6[nurse_id] for nurse_id in nurses_ids)

        '''S7'''
        #S7: TOTAL WORKING WEEK-ENDS
        # binary variable, for each nurse and each weekend, which is one if the nurse worked both Saturday and Sunday
        worked_weekend = model.addVars(nurses_ids, saturdays, vtype=GRB.BINARY, name='Worked_Weekend')
        model.addConstrs(worked_weekend[nurse_id, d] >= worked_day[nurse_id, days[d]] 
                        for nurse_id in nurses_ids
                        for d in saturdays)

        model.addConstrs(worked_weekend[nurse_id, d] >= worked_day[nurse_id, days[d+1]] 
                        for nurse_id in nurses_ids
                        for d in saturdays)

        penalty_S7 = model.addVars(nurses_ids, vtype=GRB.INTEGER)

        model.addConstrs(penalty_S7[nurse_id] >= 0 for nurse_id in nurses_ids)
        model.addConstrs(penalty_S7[nurse_id] >= quicksum(worked_weekend[nurse_id, d] for d in saturdays) 
                        - contracts[nurses[nurse_id]['contract_type']]['max_working_week_ends']
                        for nurse_id in nurses_ids)


        penalty_S7_tot = quicksum(penalty_S7[nurse_id] for nurse_id in nurses_ids)

        '''OBJECTIVE FUNCTION'''
        # OBJECTIVE FUNCTION
        #obj = 0 + lambdaS1 * penalty_S1 + lambdaS2_min * penalty_S2_min + lambdaS3 * penalty_S3_min + lambdaS4 * penalty_S4 + lambdaS5 * penalty_S5 + lambdaS6 * penalty_S6_min + lambdaS6 * penalty_S6_max + lambdaS7 * penalty_S7
        obj = lambdaS1 * penalty_S1_tot + lambdaS2_min * penalty_S2_min_tot + lambdaS2_max * penalty_S2_max_tot + lambdaS3 * (penalty_S3_min + penalty_S3_max_tot) + lambdaS4 * penalty_S4 + lambdaS5 * penalty_S5 + lambdaS6 * penalty_S6_tot + lambdaS7 * penalty_S7_tot
        model.setObjective(obj, GRB.MINIMIZE)
        #model.Params.MIPGap = 50 * 10 ** -2
        if max_time is not None:
                model.Params.TimeLimit = max_time

        model.optimize()

        print("vars",model.NumVars)
        print("varsInt",model.NumIntVars)
        print("varsBin",model.NumBinVars)
        print("constrsLin", model.NumConstrs)
        print("constrQ", model.NumQConstrs)
        print("constrsSOS", model.NumSOS)
        print("constrsGen", model.NumGenConstrs)
        print("model", model)

        end = timer()

        #TIME
        #x = datetime.datetime.now()
        first_day = datetime.datetime(2020, 3, 2)

        datetimes = [first_day + datetime.timedelta(days=d) for d in range(len(days))]
        datetimes_str = [date.strftime("%a %d %b %y") for date in datetimes]

        # OUTPUT DISPLAY
        table = BeautifulTable()
        table.set_style(BeautifulTable.STYLE_SEPARATED)
        table.max_table_width = 70
        table.column_headers = ["Nurse"] + datetimes_str
        for nurse_id in nurses_ids:
                nurse_shifts = []
                for day in days:
                        letter = " "
                        for shift in shift_types:
                                if assignment[nurse_id, shift, day].X == 1:
                                        letter = shift.upper()[0]
                                        break
                        nurse_shifts.append(letter)

                table.append_row([nurses[nurse_id]['name']] + nurse_shifts)
        print(table)


        # OUTPUT SOLUTION FILE
        time = timer()
        if not os.path.exists("result"):
                os.makedirs("result")
        f_name = os.path.join("result", str(time) + ".txt")
        with open(f_name, 'w') as file:
                print(table,file=file)
        model.write(os.path.join("result", "{}_nurse-competition-output.sol".format(time)))

        elapsed_time = end - start
        absolute_gap = model.ObjVal - model.ObjBound
        relative_gap = model.MIPGap

        return elapsed_time, absolute_gap, relative_gap

















# total_assignements = 0
# for v in model.getVars():
#     #if v.X != 0:
#     #if "Worked_Day" in v.Varname and "Required" not in v.Varname and v.X == 0:
#         print("%s %f\n" % (v.Varname, v.X))
#     #if "Assignment" in v.Varname:
#     #    total_assignements += v.X

#print("total_assignements: " + str(total_assignements))


# for nurse_id in nurses_ids:
#         for shift in shift_types:
#                 for day in days:
#                         print(assignment[nurse_id, shift, day].X)
