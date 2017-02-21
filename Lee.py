from overpass import API
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict
from geopy.distance import vincenty
import pandas as pd


api = API()
api.timeout=900
response = api.Get('way["highway"]["highway"!~"footway|cycleway|path|service|track|pedestrian|steps|crossing"](40.751872, -73.994120 ,40.762353, -73.979678);')
# response = api.Get('way["highway"]["highway"~"motorway|trunk"](40.701274, -74.033596, 40.807903, -73.931286);')

################################################################################
node_dic={}
cor_dic=defaultdict(list)
x = 0
for features in response['features']:
    for coordinate in features['geometry']['coordinates']:
        node_dic[x] = (coordinate[1], coordinate[0])
        x += 1
for node_num in node_dic:
    cor_dic[node_dic[node_num]].append(node_num)
################################################################################


cor_intersection_dic={}
intersection_cor_dic={}

for a in cor_dic:
    if len(cor_dic[a])>=2:
        cor_intersection_dic[a]=cor_dic[a][0]
        intersection_cor_dic[cor_dic[a][0]]=a
print("------------")
print(node_dic)
print(cor_dic)

print(intersection_cor_dic)
print(cor_intersection_dic)
print("-------------")

###############################################################################

node_size = len(node_dic)
intersection_size = len(intersection_cor_dic)

arc_list = np.zeros((node_size,node_size),dtype='int')
distance_list= np.zeros((node_size,node_size),dtype='float')
arc_list2 = np.zeros((node_size,node_size),dtype='int')
distance_list2 = np.zeros((node_size,node_size),dtype='float')
###############################################################################

for feature in response['features']:
    print(feature)
    corlist = feature['geometry']['coordinates']
    # print(corlist)
    i = 0
    j = 1
    for i in range(len(corlist)-1):
        distance=0
        for j in range(i+1,len(corlist)):
            cor_key1 = (corlist[i][1],corlist[i][0])
            cor_key2 = (corlist[j][1],corlist[j][0])
            distance += vincenty((corlist[j-1][1],corlist[j-1][0]), (corlist[j][1],corlist[j][0])).km * 100
            if cor_key1 in cor_intersection_dic.keys():
                if cor_key2 in cor_intersection_dic.keys():
                    distance_list2[cor_intersection_dic[cor_key1]][cor_intersection_dic[cor_key2]] = distance
                    break
            else:
                break



for feature in response['features']:
    # print(feature['geometry']['coordinates'])
    # print(feature['properties'].keys())
    # if 'oneway' in feature['properties'].keys():
    ilen = len(feature['geometry']['coordinates'])
    for i,coordinate in enumerate(feature['geometry']['coordinates']):
        if i != ilen-1:
            cor_key1 = (feature['geometry']['coordinates'][i][1],feature['geometry']['coordinates'][i][0])
            cor_key2 = (feature['geometry']['coordinates'][i+1][1], feature['geometry']['coordinates'][i+1][0])
            # arc_list[cor_dic[cor_key1][0]][cor_dic[cor_key2][0]]+=1
            distance = vincenty(cor_key1, cor_key2).km*100
            distance_list[cor_dic[cor_key1][0]][cor_dic[cor_key2][0]] = distance





###############################################시각화
Arc_tuple_List = []
for x,y in enumerate(distance_list):
    for i,j in enumerate(y):
        if distance_list[x,i] != False:
            Arc_tuple_List.append((x,i))
print(Arc_tuple_List)

Arc_tuple_List2 = []
for x,y in enumerate(distance_list2):
    for i,j in enumerate(y):
        if distance_list2[x,i] != False:
            Arc_tuple_List2.append((x,i))
print(Arc_tuple_List2)

distance1 = pd.DataFrame()
arc_i_list1 = [arc[0]for arc in Arc_tuple_List]
arc_j_list1 = [arc[1]for arc in Arc_tuple_List]
arc_distace_list1 = [distance_list[arc[0]][arc[1]]for arc in Arc_tuple_List]
distance1["i"] = arc_i_list1
distance1["j"] = arc_j_list1
distance1["distance"] = arc_distace_list1


distance2 = pd.DataFrame()
arc_i_list2 = [arc[0]for arc in Arc_tuple_List2]
arc_j_list2 = [arc[1]for arc in Arc_tuple_List2]
arc_distace_list2 = [distance_list2[arc[0]][arc[1]]for arc in Arc_tuple_List2]
distance2["i"] = arc_i_list2
distance2["j"] = arc_j_list2
distance2["distance"] = arc_distace_list2

distance1.to_csv("distance1.csv")
distance2.to_csv("distance2.csv")

# arc_i_list = [arc[0]for arc in Arc_tuple_List]
# arc_j_list = [arc[1]for arc in Arc_tuple_List]
# arc_distance_list = [distance_list2[arc[0]][arc[1]]for arc in Arc_tuple_List]
# print(arc_i_list)
# print(arc_j_list)
# print(arc_distance_list)
#
# ARCS = pd.DataFrame()
# ARCS["i"] = arc_i_list
# ARCS["j"] = arc_j_list
# ARCS["Distance"] = arc_distance_list
#
# ARCS.to_csv("ARCS.csv")


#
# new_node_dic = {}
# for nodes in cor_dic.values():
#     new_node_dic[nodes[0]] = node_dic[nodes[0]]
#


G = nx.Graph()
G.add_nodes_from(node_dic)
G.add_edges_from(Arc_tuple_List)
#
# G2 = nx.Graph()
# G2.add_nodes_from(intersection_cor_dic)
# G2.add_edges_from(Arc_tuple_List2)
#
nx.draw(G, pos=node_dic,with_labels=True, node_size = 1000, width=0.3)
plt.show()
# nx.draw(G2, pos=intersection_cor_dic,with_labels=True, node_size = 300, width=0.3)
# plt.show()

# Arc = pd.DataFrame()
# Arc["i"].from
# Arc["j"]
# Arc["distance"]
# print(distance_list2)