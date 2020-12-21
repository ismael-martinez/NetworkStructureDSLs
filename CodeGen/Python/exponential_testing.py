from networkUtil import *
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

prev_event_next_queue = [4, 5.5]
next_event_current_queue = [6, 8]
current_event_current_queue = [5, 6]
current_event_next_queue = [6.2,7]
lower_bound = 5
upper_bound = 7
cq_service_rate = 2.5
nq_service_rate = 2.7

Z = partition_probabilities(lower_bound, upper_bound, cq_service_rate, nq_service_rate, current_event_current_queue, current_event_next_queue,prev_event_next_queue, next_event_current_queue)

data = []
for i in range(10000):
    z = 0
    u = np.random.random()
    if u < Z[0]:
        z = 0
    elif u < Z[0] + Z[1]:
        z = 1
    else:
        z = 2

    d = sample_truncated_exponential_two_queues_open(z, lower_bound, upper_bound, cq_service_rate, nq_service_rate, current_event_current_queue, current_event_next_queue,prev_event_next_queue, next_event_current_queue)
    data.append(d)

datapoints = len(data)
bins_d = 50
#hist, bin_edges = np.histogram(data, bins=bins_d)

sns.distplot(data, hist=True, norm_hist=True, kde=False, bins=bins_d, color='#0000FF')
plt.title(r'Sampling from $[5,7], \ \ \mu_{q_e} = 2, \ \mu_{q_{\pi(e)}}=3$')
plt.vlines(5.5, ymin = 0, ymax = 0.8, color='red', linestyles='dashed')
plt.text(5.5, 0.82, r'$P^D$', fontsize=14)
plt.vlines(6.2, ymin = 0, ymax = 0.8, color='red', linestyles='dashed')
plt.text(6.2, 0.82, r'$P^A$', fontsize=14)
#plt.hist(data, bins=bin_edges[:-1], alpha=0.5, label='Sampling over partitions', edgecolor='black')
plt.show()