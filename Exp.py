import matplotlib.pyplot as plt

from Model import runGRD

'''SECOND PLOT: FIXED NUM_NURSES'''
# nurses number fixed
# increasing the time_period
time_periods = range(2, 9) # 2-8 weeks
num_nurses = 300
elapsed_times = []
for time_period in time_periods:
    elapsed_time, absolute_gap, relative_gap = runGRD(num_nurses, time_period)
    elapsed_times.append(elapsed_time)

plt.plot(time_periods, elapsed_times)
plt.xlabel('Numero di settimane')
plt.ylabel('Tempo di calcolo')
plt.title("Numero di infermieri: {}".format(num_nurses))
# per fare exp su server
plt.savefig("Time_weeks.png")
plt.clf() # per non fare i grafici sempre sulla stessa figura

'''SECOND PLOT: FIXED TIME_PERIOD'''
# fixed a large time_period
# decreasing the nurses number
time_periods = 8 # weeks
num_nurses = range(15, 316, 30)
elapsed_times = []
for n in num_nurses:
    elapsed_time, absolute_gap, relative_gap = runGRD(n, time_periods)
    elapsed_times.append(elapsed_time)

plt.plot(num_nurses, elapsed_times)
plt.xlabel('Numero di infermieri')
plt.ylabel('Tempo di calcolo')
plt.title("Numero di settimane: {}".format(time_periods))
# per fare exp su server
plt.savefig("Time_nurses.png")
plt.clf() # per non fare i grafici sempre sulla stessa figura 

'''THIRD PLOT: FIXED MAX CALCULATION TIME'''
# fixed maximum time of calculation
# increasing the time_period
time_periods = range(2, 9) # 2-8 weeks
num_nurses = 300
# max time: 30 seconds
max_time = 30 # seconds
relative_gaps = []
for time_period in time_periods:
    elapsed_time, absolute_gap, relative_gap = runGRD(num_nurses, time_period, max_time)
    relative_gaps.append(relative_gap)

plt.plot(time_periods, relative_gaps)
plt.xlabel('Numero di settimane')
plt.ylabel('Gap percentuale')
plt.title("Numero di infermieri: {}, Tempo massimo: {}s".format(num_nurses, max_time))
# per fare exp su server
plt.savefig("Gap_weeks.png")
plt.clf() # per non fare i grafici sempre sulla stessa figura


# fixed maximum time of calculation
# increasing the time_period
time_periods = range(2, 9) # 2-8 weeks
num_nurses = 300
# max time: 30 minutes
max_time = 30*60 # seconds
relative_gaps = []
for time_period in time_periods:
    elapsed_time, absolute_gap, relative_gap = runGRD(num_nurses, time_period, max_time)
    relative_gaps.append(relative_gap)

plt.plot(time_periods, relative_gaps)
plt.xlabel('Numero di settimane')
plt.ylabel('Gap percentuale')
plt.title("Numero di infermieri: {}, Tempo massimo: {}s".format(num_nurses, max_time))
# per fare exp su server
plt.savefig("Gap_weeks.png")
plt.clf() # per non fare i grafici sempre sulla stessa figura
