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

def merge_timestamps_attr(sched_attr, old_sched):
    # Merge
    i, j = 0, 0
    new_sched = []

    # Expand attributes to all timestamps of curr_sched
    curr_attr = [sched_attr[c] for c in range(1, len(sched_attr))]
    curr_sched = []
    for cs in sched_attr[0]:
        sched_attr_row = [cs] + curr_attr
        curr_sched.append(sched_attr_row)


    while i < len(old_sched) and j < len(curr_sched):
        if compare_time(old_sched[i][0], curr_sched[j][0]) < 0:
            new_sched.append(old_sched[i])
            i += 1
        else:
            new_sched.append(curr_sched[j])
            j += 1
    while i < len(old_sched):
        new_sched.append(old_sched[i])
        i += 1
    while j < len(curr_sched):
        new_sched.append(curr_sched[j])
        j += 1
    return new_sched

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

# Input:
## section (int 0,1,2 for left, middle, right
## lower_bound (float) -- Truncation begin
## upper_bound (float) -- Truncation end
## service_rate_current_queue (float >= 0)
## service_rate_next_queue (float >= 0)
## current_queue_current_event ([float] size 2) -- [arrival, departure]
## next_queue_current_event ([float] size 2) -- [arrival, departure]
## next_queue_previous_event ([float] size 2) -- [arrival, departure]
## current_queue_next_event ([float] size 2) -- [arrival, departure]
# Output: Sample for d
def sample_truncated_exponential_two_queues_open(section, lower_bound, upper_bound, service_rate_current_queue, service_rate_next_queue, current_queue_current_event, next_queue_current_event ,next_queue_previous_event, current_queue_next_event):
    [current_queue_current_event, next_queue_current_event, next_queue_previous_event, current_queue_next_event] = set_new_bounds(lower_bound, upper_bound,current_queue_current_event, next_queue_current_event, next_queue_previous_event, current_queue_next_event)
    [current_queue_current_arrival, current_queue_current_departure] = current_queue_current_event
    [next_queue_current_arrival, next_queue_current_departure] = next_queue_current_event
    [next_queue_previous_arrival, next_queue_previous_departure] = next_queue_previous_event
    [current_queue_next_arrival, current_queue_next_departure] = current_queue_next_event

    # Valid partitions
    partitions = []
    if lower_bound <= next_queue_previous_departure <= upper_bound:
        partitions.append(next_queue_previous_departure)
    if lower_bound <= current_queue_next_arrival <= upper_bound:
        partitions.append(current_queue_next_arrival)
    partitions.sort()


    if section == 0: # left most
        if service_rate_current_queue == 0:
            u = np.random.random()*(upper_bound - lower_bound) + lower_bound
            return u

        partition_point = min(partitions + [upper_bound])
        cdf_upper = 1 - np.exp(-service_rate_current_queue * (partition_point - current_queue_current_arrival))
        cdf_lower = 1 - np.exp(-service_rate_current_queue * (lower_bound - current_queue_current_arrival))
        u = np.random.random()*(cdf_upper - cdf_lower) + cdf_lower
        inv = -np.log(1-u)/service_rate_current_queue + current_queue_current_arrival
        return inv

    if section == 2: # Right most
        if service_rate_next_queue == 0:
            u = np.random.random() * (upper_bound - partitions[1]) + partitions[1]
            return  u
        partition_point = max(partitions)
        cdf_start = np.exp(service_rate_next_queue * (partition_point - next_queue_current_departure))
        cdf_upper = 1
        u = np.random.random() * (cdf_upper - cdf_start) + cdf_start
        inv = np.log(u) / service_rate_next_queue + next_queue_current_departure
        return inv

    if section == 1:
        if service_rate_current_queue == service_rate_next_queue:
            u = np.random.random() * (partitions[1] - partitions[0]) + partitions[0]
            return u
        if next_queue_previous_departure == max(partitions):
            u = np.random.random()*(partitions[1] - partitions[0]) + partitions[0]
            return u
        else:
            gamma = 1
            if service_rate_current_queue < service_rate_next_queue:
                gamma = -1
                service_rate =  service_rate_next_queue - service_rate_current_queue
            else:
                service_rate = service_rate_current_queue - service_rate_next_queue
            if service_rate_next_queue == 0:
                loc_const = current_queue_current_arrival
            else:
                loc_const = gamma * (
                    current_queue_current_arrival * service_rate_current_queue - next_queue_current_departure * service_rate_next_queue) / service_rate

            if service_rate_next_queue == 0:
                cdf_start = 1 - np.exp(service_rate_current_queue * (lower_bound - current_queue_current_arrival))
                u = np.random.random()*(1-cdf_start) + cdf_start
                u = max(1.0e-10, u)
                u = min(0.9999, u)
                inv = - np.log(1-u) + partitions[0]
                return inv
            if gamma > 0:
                cdf_start = 1 - np.exp(-service_rate* (lower_bound - loc_const))
                cdf_end = 1 - np.exp(-service_rate * (upper_bound - loc_const))
            else:
                cdf_start = np.exp(service_rate * (lower_bound - loc_const))
                cdf_end = np.exp(service_rate * (upper_bound - loc_const))

            lower_bound =  max(cdf_start, 0)
            upper_bound =  min(cdf_end, 1)
            norm_constant = upper_bound - lower_bound
            u = np.random.random() * norm_constant + cdf_start
            if gamma > 0:
                u = max(1.0e-10, u)
                u = min(0.9999, u)
                inv =  -np.log(1 - u) / service_rate + loc_const
            else:
                u = max(1.0e-10, u)
                u = min(0.9999, u)
                inv = np.log(u) / service_rate + loc_const
                return inv
            return inv

    # # Depermine bounds of previous and next items
    # cq_ne_arrival = current_queue_next_event[0]
    # cq_ne_departure = current_queue_next_event[1]
    # if cq_ne_arrival >= end:
    #     param_lambda = -param_lambda2
    # else:
    #     param_lambda = param_lambda1 - param_lambda2
    # if param_lambda == 0: # Return uniform
    #     u = np.random.random()*(end-start) + start
    #     return u
    #
    # gamma = 1
    # if param_lambda2 > param_lambda1:
    #     gamma = -1
    # loc_const = gamma*(A*param_lambda1 - B*param_lambda2) / param_lambda
    # if cq_ne_arrival >= end:
    #     loc_const += gamma*param_lambda1(cq_ne_arrival - cq_ne_departure)/param_lambda
    # else:
    #     loc_const += -gamma * param_lambda1(cq_ne_departure) / param_lambda
    #
    #
    # if gamma > 0:
    #     cdf_start = 1 - np.exp(-gamma*param_lambda * (gamma*start - loc_const))
    #     cdf_end = 1 - np.exp(-gamma*param_lambda * (gamma*end - loc_const))
    # else:
    #     cdf_start = np.exp(-param_lambda * (start + loc_const))
    #     cdf_end = np.exp(-param_lambda * (end + loc_const))
    #
    # lower_bound =  max(cdf_start, 0)
    # upper_bound =  min(cdf_end, 1)
    # norm_constant = upper_bound - lower_bound
    # u = np.random.random() * norm_constant + lower_bound
    # if gamma > 0:
    #     inv_exp_sample =  -np.log(1 - u) / param_lambda + loc_const
    # else:
    #     inv_exp_sample = -np.log(u)/param_lambda - loc_const
    # return inv_exp_sample


# Input:
## lower_bound (float) -- Truncation begin
## upper_bound (float) -- Truncation end
## service_rate_current_queue (float >= 0)
## service_rate_next_queue (float >= 0)
## current_queue_current_event ([float] size 2) -- [arrival, departure]
## next_queue_current_event ([float] size 2) -- [arrival, departure]
## next_queue_previous_event ([float] size 2) -- [arrival, departure]
## current_queue_next_event ([float] size 2) -- [arrival, departure]
# Output: Partition probabilities (array, sum to 1)
def partition_probabilities(lower_bound, upper_bound, service_rate_current_queue, service_rate_next_queue, current_queue_current_event, next_queue_current_event ,next_queue_previous_event, current_queue_next_event):

    # if next_queue_current_event[0] is None and current_queue_next_event[0] is None:
    #     return [1,0,0]

    [current_queue_current_event, next_queue_current_event, next_queue_previous_event, current_queue_next_event] = set_new_bounds(lower_bound, upper_bound,current_queue_current_event, next_queue_current_event, next_queue_previous_event, current_queue_next_event)
    [current_queue_current_arrival, current_queue_current_departure] = current_queue_current_event
    [next_queue_current_arrival, next_queue_current_departure] = next_queue_current_event
    [next_queue_previous_arrival, next_queue_previous_departure] = next_queue_previous_event
    [current_queue_next_arrival, current_queue_next_departure] = current_queue_next_event

    # Valid partitions
    partitions = []
    if lower_bound <= next_queue_previous_departure <= upper_bound:
        partitions.append(next_queue_previous_departure)
    if lower_bound <= current_queue_next_arrival <= upper_bound:
        partitions.append(current_queue_next_arrival)
    partitions.sort()

    if len(partitions) < 2:
        print('error')

    #print([lower_bound, partitions[0], partitions[1], upper_bound])
    #print([lower_bound, upper_bound, service_rate_current_queue, service_rate_next_queue, current_queue_current_event, next_queue_current_event ,[next_queue_previous_arrival, next_queue_previous_departure], [current_queue_next_arrival, current_queue_next_departure]])

    norm_array = [0]*3
    # F(x) = 1 - exp(-mu*(x-a)) for left side queues
    # F(x) = exp(-mu*(b-x)) for right side queues

    # Full scaled probability of left-most case, truncated

        # Previous event, next queue
        #Z *= np.exp(service_rate_next_queue * (min(next_queue_previous_departure,current_queue_next_arrival) - next_queue_previous_departure)) - \
        #     np.exp(service_rate_next_queue * (max(next_queue_previous_arrival, lower_bound) - next_queue_previous_departure))
        # Current event, next queue
        #Z *= 1-np.exp(service_rate_next_queue * (next_queue_previous_departure - next_queue_current_departure))
    if partitions[0] == lower_bound:
        Z = 0
    else:
    # Current event, current queue
        if service_rate_current_queue != 0:
            Z = np.exp(-service_rate_current_queue * (lower_bound - current_queue_current_arrival)) - \
                np.exp(-service_rate_current_queue * (partitions[0] - current_queue_current_arrival))
        else:
            Z = 1

    # Next event, current queue
    #Z += 1-np.exp(service_rate_current_queue*(current_queue_next_arrival - current_queue_next_departure))

    # # Truncate
    # Z /= np.exp(-service_rate_current_queue * (lower_bound - current_queue_current_arrival))  \
    #      - np.exp(-service_rate_current_queue * (current_queue_current_departure - current_queue_current_arrival))
    norm_array[0] = Z

    # Full scaled probability of right-most case, truncated
    Z = 0
    if current_queue_next_arrival is None or partitions[1] == upper_bound:
        norm_array[2] = 0
    else:
        # Previous event, next queue
        #Z *= 1 - np.exp(-service_rate_next_queue * (next_queue_previous_departure - next_queue_previous_arrival))
        # Current event, next queue

        Z += 1 - np.exp(service_rate_next_queue * (partitions[1] - current_queue_next_departure))
        # Current queue, current and next event
        current_queue_full = service_rate_current_queue**2 * np.exp(-service_rate_current_queue * (min(current_queue_next_departure, upper_bound) - min(current_queue_current_arrival, upper_bound)))\
             *(min(upper_bound, current_queue_next_departure) - min(current_queue_next_arrival, upper_bound))
        Z += current_queue_full*(min(upper_bound, current_queue_next_departure) - current_queue_next_arrival)

        # Truncate
        # Z /= np.exp(service_rate_current_queue * (upper_bound - next_queue_current_departure))  \
        #      - np.exp(service_rate_current_queue * (next_queue_previous_departure - next_queue_current_departure))
        norm_array[2] = Z

    # Full scaled probability of middle case, truncated
    if partitions[0] == partitions[1]:
        Z = 0
    elif next_queue_previous_departure == min(partitions):


        Z = 0
        gamma = 1
        if service_rate_current_queue == service_rate_next_queue:
            Z += service_rate_current_queue * np.exp(service_rate_current_queue*(partitions[1] - partitions[0]))*(partitions[1] - partitions[0])
        else:
            if service_rate_current_queue < service_rate_next_queue:
                gamma = -1
                service_rate = service_rate_next_queue - service_rate_current_queue
            else:
                service_rate = service_rate_current_queue - service_rate_next_queue

            if service_rate_current_queue == 0:
                joint_service = service_rate_next_queue
            elif service_rate_next_queue == 0:
                joint_service = service_rate_current_queue
            else:
                joint_service = service_rate_current_queue * service_rate_next_queue / service_rate
            if service_rate_next_queue == 0:
                loc_const = current_queue_current_arrival * service_rate_current_queue
            else:
                loc_const = gamma * (current_queue_current_arrival * service_rate_current_queue - next_queue_current_departure * service_rate_next_queue) / service_rate
            if gamma > 0:
                Z += joint_service * (np.exp(- service_rate * (
                            max(next_queue_previous_departure, current_queue_current_arrival) - loc_const)) - np.exp(
                    - service_rate * (min(next_queue_current_departure, current_queue_next_arrival) - loc_const)))
            else:
                cdf_end = np.exp(service_rate * (
                            min(upper_bound, next_queue_current_departure) - loc_const))
                cdf_start = np.exp(
                    service_rate * (max(lower_bound, current_queue_current_arrival) - loc_const))
                Z += joint_service * (cdf_end - cdf_start)

            # Previous event, next queue
            #if next_queue_previous_departure > lower_bound:
            #    Z += 1 - np.exp(-service_rate_next_queue * (
            #                next_queue_previous_departure - max(next_queue_previous_arrival, lower_bound)))
            # Next event, current queue
            if current_queue_next_arrival < upper_bound:
                Z += 1 - np.exp(
                    service_rate_current_queue * (current_queue_next_arrival - current_queue_next_departure))

        # Truncate
        # Z /= np.exp(service_rate_current_queue * (upper_bound - next_queue_current_departure)) \
        #      - np.exp(service_rate_current_queue * (next_queue_previous_departure - next_queue_current_departure))
        norm_array[1] = Z


    else: # Full probability scaled, uniform. B > A
        # Previous event, next queue
        #Z *= 1 - np.exp(-service_rate_next_queue * (next_queue_previous_departure - current_queue_next_arrival))
        # Current event, next queue
        #Z *= np.exp(service_rate_next_queue * (current_queue_next_departure - next_queue_previous_departure))
        # Current queue, current and next event
        if service_rate_next_queue == 0 or service_rate_current_queue == 0 or current_queue_next_arrival is None:
            norm_array[1] = 1
        else:
            Z = service_rate_current_queue ** 2 * np.exp(
                -service_rate_current_queue * (current_queue_next_departure - current_queue_current_arrival)) * (
                            next_queue_previous_departure - current_queue_next_arrival)
            norm_array[1] = Z

    Z_sum = np.sum(norm_array)
    #print(norm_array)
    if Z_sum == np.infty:
        print('error')
    #print(norm_array)
    normalized_array = [z / Z_sum for z in norm_array]
    #print(normalized_array)
    return normalized_array

# Sample from a truncated exponential
# Input
## param_lambda (float > 0) - exponential parameter
## start (float) - beginning of interval
## end (float) - end of interval
# def sample_trancated_exponential(param_lambda, start, end):
#     norm_constant = np.exp(-param_lambda * start) - np.exp(-param_lambda * end)
#     cdf_start = 1 - np.exp(-param_lambda*start)
#     u = np.random.random() * norm_constant + cdf_start
#     inv_exp_sample = end +  np.log( 1 - norm_constant * u) / param_lambda
#     return inv_exp_sample
#
# def sample_truncated_exponential_right_fixed(param_lambda, start, end):
#     norm_constant = np.exp(-param_lambda * (end - start)) - 1
#     cdf_start = 1 - np.exp(-param_lambda * (end - start))
#     u = np.random.random() * norm_constant + cdf_start
#     inv_exp_sample =  np.log(1 - norm_constant * u) / param_lambda + end
#     return inv_exp_sample
#
# def sample_truncated_exponential_left_fixed(param_lambda, start, end):
#     norm_constant = 1 - np.exp(-param_lambda * (end-start))
#     cdf_start = 0
#     u = np.random.random() * norm_constant + cdf_start
#     inv_exp_sample = - np.log(1 - norm_constant * u) / param_lambda + start
#     return inv_exp_sample


def set_new_bounds(lower_bound, upper_bound,
                                current_queue_current_event, next_queue_current_event, next_queue_previous_event,
                                current_queue_next_event):

    [current_queue_current_arrival, current_queue_current_departure] = current_queue_current_event
    [next_queue_current_arrival, next_queue_current_departure] = next_queue_current_event
    [next_queue_previous_arrival, next_queue_previous_departure] = next_queue_previous_event
    [current_queue_next_arrival, current_queue_next_departure] = current_queue_next_event



    if current_queue_next_arrival is not None and current_queue_next_arrival > upper_bound:
        if next_queue_previous_departure is None:
            next_queue_previous_departure = upper_bound
        if next_queue_previous_arrival is None or (next_queue_previous_arrival is not None and next_queue_previous_arrival < lower_bound):
            next_queue_previous_arrival = lower_bound
        current_queue_next_arrival = upper_bound
        current_queue_next_departure = upper_bound
    elif current_queue_next_arrival is not None and current_queue_next_arrival <= lower_bound:
        current_queue_next_arrival = lower_bound
        current_queue_next_departure = upper_bound
    elif current_queue_next_arrival is None:
        current_queue_next_arrival = upper_bound
        current_queue_next_departure = upper_bound

    if next_queue_current_arrival is None:
        next_queue_previous_arrival = lower_bound
        next_queue_previous_departure = upper_bound

    elif next_queue_previous_departure is None or next_queue_previous_departure < lower_bound or next_queue_previous_arrival > upper_bound:
        next_queue_previous_departure = lower_bound
        next_queue_previous_arrival = lower_bound
    elif next_queue_previous_departure > upper_bound:
        next_queue_previous_departure = upper_bound
        next_queue_previous_arrival = lower_bound
    # else:
    #     if next_queue_current_arrival is None and current_queue_next_arrival is not None:
    #         if current_queue_next_arrival > lower_bound:
    #             next_queue_previous_departure = current_queue_next_arrival
    #         else:
    #             next_queue_previous_departure = lower_bound
    #         next_queue_previous_arrival = lower_bound
    #     elif next_queue_current_arrival is None and current_queue_next_arrival is None:
    #         next_queue_previous_departure = upper_bound
    #         next_queue_previous_arrival = lower_bound


    # if current_queue_next_arrival is None or current_queue_next_arrival > upper_bound:
    #     current_queue_next_arrival = upper_bound
    #     current_queue_next_departure = upper_bound
    # if current_queue_next_arrival < lower_bound:
    #     current_queue_next_arrival = lower_bound
    #     current_queue_next_departure = upper_bound


    current_queue_current_event = [current_queue_current_arrival, current_queue_current_departure]
    next_queue_current_event = [next_queue_current_arrival, next_queue_current_departure]
    next_queue_previous_event = [next_queue_previous_arrival, next_queue_previous_departure]
    current_queue_next_event = [current_queue_next_arrival, current_queue_next_departure]


    partitions = []
    if lower_bound <= next_queue_previous_departure <= upper_bound:
        partitions.append(next_queue_previous_departure)
    if lower_bound <= current_queue_next_arrival <= upper_bound:
        partitions.append(current_queue_next_arrival)
    partitions.sort()

    if len(partitions) < 2:
        print('error')

    return [current_queue_current_event, next_queue_current_event, next_queue_previous_event, current_queue_next_event]