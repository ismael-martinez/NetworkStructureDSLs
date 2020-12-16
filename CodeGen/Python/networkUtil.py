from math import sin, cos, sqrt, atan2, radians
import numpy as np

# Compare two timestamps by first converting to seconds
# Input:
## timestamp1 (string)
## timestamp2 (string)
# Result: timestamp1_greater (int). 1 if true, -1 if timestamp1 < timestamp2, 0 if equal.
def compare_time(timestamp1, timestamp2):
    hour1 = timestamp1.hour
    min1 = timestamp1.minutes
    sec1 = timestamp1.seconds
    ms1 = timestamp1.milliseconds

    hour2 = timestamp2.hour
    min2 = timestamp2.minutes
    sec2 = timestamp2.seconds
    ms2 = timestamp2.milliseconds

    if hour1 > hour2:
        time1_greater = 1
    elif hour1 < hour2:
        time1_greater = -1
    else:
        if min1 > min2:
            time1_greater = 1
        elif min1 < min2:
            time1_greater = -1
        else:
            if sec1 > sec2:
                time1_greater = 1
            elif sec1 < sec2:
                time1_greater = -1
            else:
                if ms1 > ms2:
                    time1_greater = 1
                elif ms1 < ms2:
                    time1_greater = -1
                else:
                    time1_greater = 0
    return time1_greater

# Computer the geographical distance between two points in meters
# Inputs:
## location1 (float) - class with latitude, longitude attributes
## location2 (float) - class with latitude, longitude attributes
## Result: distance (float) - Distance in meters
def distance_location(location1, location2):
    R = 6373.0 # Radius of earth

    lat1 = location1.latitude
    lat2 = location2.latitude
    lon1 = location1.longitude
    lon2 = location2.longitude

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    d_coord = R*c

    height1 = location1.height
    height2 = location2.height
    dheight = height2 - height1
    dist = sqrt(d_coord**2 + (dheight)**2)
    return dist

# Merge two arrays of pairs together
# Input:
## list_a (N array of pairs) - Original list
## list_b (M array of timestamps)
## q_ids (M array of indices)
# Return: merged list of pairs
def merge_id(list_a, list_b, e_id, q_ids):
    list_c = []
    i = 0
    j = 0
    while i < len(list_a) and j < len(list_b):
        if list_a[i][0] > list_b[j]:
            list_c.append((list_b[j], e_id, q_ids[j]))
            j += 1
        else:
            list_c.append(list_a[i])
            i += 1
    while i < len(list_a):
        list_c.append(list_a[i])
        i += 1
    while j < len(list_b):
        list_c.append((list_b[j], e_id, q_ids[j]))
        j += 1
    return list_c

# Merge two arrays of events together
# Input:
## list_a (N array of events)
## list_b (N array of events)
## Pair (timestamp, id)
# Return: merged list of pairs
def merge_events(list_a, list_b):
    list_c = []
    i = 0
    j = 0
    while i < len(list_a) and j < len(list_b):
        if list_a[i].arrival_times[0] > list_b[j].arrival_times[0]:
            list_c.append(list_b[j])
            j += 1
        else:
            list_c.append(list_a[i])
            i += 1
    while i < len(list_a):
        list_c.append(list_a[i])
        i += 1
    while j < len(list_b):
        list_c.append(list_b[j])
        j += 1
    return list_c

def merge_timestamps(sched, old_sched):
    # Merge
    i, j = 0, 0
    new_sched = []
    while i < len(old_sched) and j < len(sched):
        if compare_time(old_sched[i], sched[j]) < 0:
            new_sched.append(old_sched[i])
            i += 1
        else:
            new_sched.append(sched[j])
            j += 1
    while i < len(old_sched):
        new_sched.append(old_sched[i])
        i += 1
    while j < len(sched):
        new_sched.append(sched[j])
        j += 1
    return new_sched

# DepthFirstSearch
# nodes (dict of node ids)
def depthFirstSearch(nodes):
    all_paths = []
    node_visited_map = {}
    for node in nodes:
        node_visited_map[node] = False

    node_visited = [node_visited_map[key] for key in node_visited_map]
    for node in nodes:
        if all(node_visited):
            break
        [node_visited_map, _, all_paths] = depthFirstSearch_rec(nodes, node, node_visited_map, all_paths)
        node_visited = [node_visited_map[key] for key in node_visited_map]
    return all_paths

def depthFirstSearch_rec(nodes, root, node_visited_map, all_paths):
    root_paths = []
    if node_visited_map[root]:
        return [node_visited_map, [], all_paths]
    node_visited_map[root] = True
    node = root
    root_paths.append([root])
    for nb in nodes[node].neighbours:
        [node_visited_map, paths, all_paths] = depthFirstSearch_rec(nodes, nb[1], node_visited_map, all_paths)
        for p in paths:
            root_paths.append([root] + p)
    for p in root_paths:
        all_paths.append(p)
    return [node_visited_map, root_paths, all_paths]

# Sample from a truncated exponential
# Input
## param_lambda (float > 0) - exponential parameter
## start (float) - beginning of interval
## end (float) - end of interval
def sample_trancated_exponential(param_lambda, start, end):
    norm_constant = np.exp(-param_lambda * start) - np.exp(-param_lambda * end)
    cdf_start = 1 - np.exp(-param_lambda*start)
    u = np.random.random() * norm_constant + cdf_start
    inv_exp_sample = end +  np.log( 1 - norm_constant * u) / param_lambda
    return inv_exp_sample

def sample_truncated_exponential_right_fixed(param_lambda, start, end):
    norm_constant = np.exp(-param_lambda * (end - start)) - 1
    cdf_start = 1 - np.exp(-param_lambda * (end - start))
    u = np.random.random() * norm_constant + cdf_start
    inv_exp_sample =  np.log(1 - norm_constant * u) / param_lambda + end
    return inv_exp_sample

def sample_truncated_exponential_left_fixed(param_lambda, start, end):
    norm_constant = 1 - np.exp(-param_lambda * (end-start))
    cdf_start = 0
    u = np.random.random() * norm_constant + cdf_start
    inv_exp_sample = - np.log(1 - norm_constant * u) / param_lambda + start
    return inv_exp_sample

def sample_truncated_exponential_two_queues_open(param_lambda1, param_lambda2, A, B, start, end):
    param_lambda = param_lambda1 - param_lambda2
    gamma = 1
    if param_lambda2 > param_lambda1:
        gamma = -1
    loc_const = gamma*(A*param_lambda1 - B*param_lambda2) / param_lambda
    if gamma > 0:
        cdf_start = gamma*(1 - np.exp(-gamma*param_lambda * (gamma*start - loc_const)))
        cdf_end = 1 - np.exp(-gamma*param_lambda * (gamma*end - loc_const))
    else:
        cdf_start = np.exp(-param_lambda * (start - loc_const))
        cdf_end = np.exp(-param_lambda * (end - loc_const))

    lower_bound = max(cdf_start, 0)
    upper_bound = min(cdf_end, 1)
    norm_constant = upper_bound - lower_bound
    u = np.random.random() * norm_constant + lower_bound
    inv_exp_sample =  -np.log(1 - norm_constant * u) / param_lambda + loc_const
    return inv_exp_sample