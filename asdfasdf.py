from math import sqrt

location = ['a', .59, .59]
location2 = [(40.752169, -73.991961)]

master_list = [['a', .5, .5],
               ['b', .3, .2],
               ['a', .4, .4],
               ['b', .45, .45],
               ['a', .6, .6],
               ['b', .55, .55]]



def get_neighbours(distance, location, locations):
    neighbours = []
    for loc in locations:
        if sqrt((location[1] - loc[1])**2 + (location[2] - loc[2])**2) < distance:
            neighbours.append(loc)
    return neighbours

print (get_neighbours(0.05, location, master_list))