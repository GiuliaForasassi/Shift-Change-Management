import matplotlib.pyplot as plt

from Model import runRealData

time_periods = [4, 8] # weeks
num_nurses = [30, 40, 50, 60, 80, 100, 120]



'''SECOND PLOT: FIXED MAX CALCULATION TIME'''
# fixed maximum time of calculation
max_time = 60 # 60 seconds
for t in time_periods:
    relative_gaps = []
    for n in num_nurses:
        elapsed_time, absolute_gap, relative_gap = runRealData(n, t, max_time)
        relative_gaps.append(relative_gap)

    plt.plot(num_nurses, relative_gaps, label=str(t)+"weeks")

plt.legend()
plt.xlabel('Numero di infermieri')
plt.ylabel('Gap percentuale')
plt.title("Tempo massimo: {}s".format(max_time))
# per togliere il float in valori interi delle x
plt.xticks(time_periods)
# per fare exp su server
plt.savefig("Gap_60sec.png")
plt.clf() # per non fare i grafici sempre sulla stessa figura



'''THIRD PLOT: FIXED MAX CALCULATION TIME (WIDE)'''
# fixed maximum time of calculation
max_time = 60 * 30 # 30 minutes
for t in time_periods:
    relative_gaps = []
    for n in num_nurses:
        elapsed_time, absolute_gap, relative_gap = runRealData(n, t, max_time)
        relative_gaps.append(relative_gap)

    plt.plot(num_nurses, relative_gaps, label=str(t)+"weeks")

plt.legend()
plt.xlabel('Numero di infermieri')
plt.ylabel('Gap percentuale')
plt.title("Tempo massimo: {}s".format(max_time))
# per togliere il float in valori interi delle x
plt.xticks(time_periods)
# per fare exp su server
plt.savefig("Gap_30min.png")
plt.clf() # per non fare i grafici sempre sulla stessa figura



'''FIRST PLOT: ...'''
# fixed a large time_period
# decreasing the nurses number
for t in time_periods:
    elapsed_times = []
    for n in num_nurses:
        elapsed_time, absolute_gap, relative_gap = runRealData(n, t)
        elapsed_times.append(elapsed_time)

    plt.plot(num_nurses, elapsed_times, label=str(t)+"weeks")

plt.legend()
plt.xlabel('Numero di infermieri')
plt.ylabel('Tempo di calcolo (s)')
plt.title("....")
# per fare exp su server
plt.savefig("Time.png")
plt.clf() # per non fare i grafici sempre sulla stessa figura 