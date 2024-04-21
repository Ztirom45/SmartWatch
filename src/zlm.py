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

ARRAY_SIZE = 50
STEP_MIN_FREQ = 0.3

def get_step(acc_array:list) -> bool:
    """
        a function which detects a step in the data and removes the step from it
    """
    #get peaks
    peak_filter = lambda position: is_peak(acc_array,position)
    peaks_pos = list(map(lambda i:i,filter(peak_filter,range(len(acc_array)))))

    if len(acc_array) > ARRAY_SIZE:
        if len(peaks_pos) > 1:
            #get frequency
            step_freq = (max((acc_array[peaks_pos[0]],acc_array[peaks_pos[1]]))-
                        min((acc_array[peaks_pos[0]],acc_array[peaks_pos[1]])))
            #delete analysed part of array
            del(acc_array[0:peaks_pos[1]])
            return step_freq > STEP_MIN_FREQ
                 
        else:
            del(acc_array[0])
    return False
