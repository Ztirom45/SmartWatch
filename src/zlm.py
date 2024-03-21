import math

degree_2_radians_distance = lambda degree_and_distance:	[math.radians(degree_and_distance[0]),degree_and_distance[1]]
radians_2_degree_distance = lambda radians_and_distance:[math.degree(radians_and_distance[0]),radians_and_distance[1]]
get_distance			=	lambda vec:			math.sqrt(pow(vec[0],2)+pow(vec[1],2))
get_distance2			=	lambda vec1,vec2:	math.sqrt(pow(vec2[0]-vec1[0],2)+pow(vec2[1]-vec1[1],2))

angle_2_vec_radians = lambda angle,distance:[math.sin(angle)*distance,math.cos(angle)*distance]
vec_2_angle_radians = lambda vec:			[math.atan2(vec),get_distance]

angle_2_vec = lambda angle,distance:angle_2_vec_radians(math.radians(angle),distance)
vec_2_angle = lambda vec:			radians_2_degree_distance(vec_2_angle_radians(vec))