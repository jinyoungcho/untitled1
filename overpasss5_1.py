from overpass import API
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict


api = API()
response = api.Get('way["highway"]["highway"!~"footway|cycleway|path|service|track|pedestrian|steps"](40.751872, -73.994120 ,40.752353, -73.989678);')

node_dic={}
x = 0
for features in response['features']:
    for coordinate in features['geometry']['coordinates']:
        # print(x, j[1], j[0])
        node_dic[x] = (coordinate[1], coordinate[0])
        x += 1

cor_dic=defaultdict(list)
for node_num in node_dic:
    cor_dic[node_dic[node_num]].append(node_num)


print(node_dic)
print(cor_dic)

node_size = len(node_dic)
print(node_size)
arc_list = np.zeros((node_size,node_size),dtype='int')
print(arc_list)

x =0
for i in response['features']:
    for j in range(len(i['geometry']['coordinates'])):
        if j != len(i['geometry']['coordinates'])-1:
            arc_list[cor_dic[node_dic[x]][0]][cor_dic[node_dic[x+1]][0]]+=1

            print(node_dic[x], cor_dic[node_dic[x]], node_dic[x+1], cor_dic[node_dic[x+1]])
        x += 1

Arc_tuple_List = []
for x,y in enumerate(arc_list):
    for i,j in enumerate(y):
        if arc_list[x,i] != False:
            Arc_tuple_List.append((x,i))

G = nx.Graph()
G.add_nodes_from(node_dic)
G.add_edges_from(Arc_tuple_List)
nx.draw(G, with_labels=True, node_size = 300, width=0.3)
plt.show()