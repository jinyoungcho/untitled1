from overpass import API
import numpy as np
from collections import defaultdict
from geopy.distance import vincenty
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx

api = API()
api.timeout=900
response = api.Get('way["highway"]["highway"!~"footway|cycleway|path|service|track|pedestrian|steps|'
                   'crossing|construction"](40.761872, -73.994120 ,40.782353, -73.969678);')
# response = api.Get('way["highway"]["highway"!~"footway|cycleway|path|service|track|pedestrian|steps|'
#                    'crossing|construction|residential|bridleway|motorway_link"](40.761872, -73.994120 ,40.782353, -73.969678);')


node_dic={}
cor_dic=defaultdict(list)
x = 0
for features in response['features']:
    print(features['geometry']['coordinates'])
    for coordinate in features['geometry']['coordinates']:
        node_dic[x] = (coordinate[1], coordinate[0])
        x += 1

print("node_dic: ", node_dic)

for node_num in node_dic:
    cor_dic[node_dic[node_num]].append(node_num)

distance_dic={}

for feature in response['features']:
    sample_coordinates = []
    coordinates = feature['geometry']['coordinates']
    for cor in coordinates:
        sample_coordinates.append((cor[1],cor[0]))
    try: feature["properties"]['name']
    except:
        print(feature["properties"])
    # if "turn:lanes" in feature["properties"].keys():
    for i in range(len(sample_coordinates)-1):
        cor_i = sample_coordinates[i]
        cor_j = sample_coordinates[i+1]
        distance_dic[cor_dic[cor_i][0], cor_dic[cor_j][0]] = vincenty(cor_i,cor_j).km*100


print(distance_dic)


Arc_tuple_List = []  ##(0, 3), (0, 72), (3, 339), (18, 31), (18, 124), (19, 22), (19, 66), (22, 169), (22, 179)
                         #(i,j) 입니다
for key in distance_dic.keys():
    Arc_tuple_List.append((key[0],key[1]))

df = pd.DataFrame()
G = nx.DiGraph()
G.add_nodes_from(node_dic)
G.add_edges_from(Arc_tuple_List)
nx.draw(G, pos=node_dic,with_labels=True, node_size = 500, width=0.3)
print(G.degree())
print(G.in_degree())
print(G.out_degree())
plt.show()