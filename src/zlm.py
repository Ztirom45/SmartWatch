"""
Ztiroms Math Library
written by Ztirom45
LICENSE GPL4
"""

import math

degree_2_radians_distance = lambda degree_and_distance:	[math.radians(degree_and_distance[0]),degree_and_distance[1]]
radians_2_degree_distance = lambda radians_and_distance:[math.degree(radians_and_distance[0]),radians_and_distance[1]]
get_distance			=	lambda vec:			math.sqrt(pow(vec[0],2)+pow(vec[1],2))
get_distance2			=	lambda vec1,vec2:	math.sqrt(pow(vec2[0]-vec1[0],2)+pow(vec2[1]-vec1[1],2))

angle_2_vec_radians = lambda angle,distance:[math.sin(angle)*distance,math.cos(angle)*distance]
vec_2_angle_radians = lambda vec:			[math.atan2(vec),get_distance]

angle_2_vec = lambda angle,distance:angle_2_vec_radians(math.radians(angle),distance)
vec_2_angle = lambda vec:			radians_2_degree_distance(vec_2_angle_radians(vec))


NEIGHBORS_LEFT_RIGHT = 5
def is_peak(data:list,position) ->bool:
    """
        function to track a peak in the neighboorhood of a position
    """
    if position < NEIGHBORS_LEFT_RIGHT or position > len(data)-NEIGHBORS_LEFT_RIGHT-1:
        return False
    return (data[position] == 
            max(data[position-NEIGHBORS_LEFT_RIGHT:position+NEIGHBORS_LEFT_RIGHT])
           or data[position]  == 
            min(data[position-NEIGHBORS_LEFT_RIGHT:position+NEIGHBORS_LEFT_RIGHT]))

ARRAY_SIZE = 100
STEP_MIN_FREQ = 5.0
STEP_MAX_FREQ = 15.0

def get_step(a:list) -> bool:
    """
        a function which detects a step in the data and removes the step from it
    """
    peaks:list = []
    for i in range(len(a)):
        if is_peak(a,i):
            peaks.append(i)

    if len(a)>ARRAY_SIZE:
        if len(peaks) >1:
            del(a[0:peaks[1]])
            acc_freq:float = max(peaks[0:2])-min(peaks[0:2])
            if acc_freq > STEP_MIN_FREQ and acc_freq < STEP_MAX_FREQ:
                return True
        else:
            del(a[0])

    return False

    
