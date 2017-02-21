from overpass import API
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict
from geopy.distance import vincenty

api = API()
api.timeout=900
response = api.Get('way["highway"]["highway"~"motorway|trunk"](40.462335, -74.362618, 40.918417, -73.669106);')

node_dic={}
x = 0
for features in response['features']:
    for coordinate in features['geometry']['coordinates']:
        node_dic[x] = (coordinate[1], coordinate[0])
        x += 1



cor_dic=defaultdict(list)
for node_num in node_dic:
    cor_dic[node_dic[node_num]].append(node_num)

node_size = len(node_dic)
arc_list = np.zeros((node_size,node_size),dtype='int')
distance_list= np.zeros((node_size,node_size),dtype='float')

print(arc_list)

x =0
for feature in response['features']:
    print(feature['geometry']['coordinates'])
    print(feature['properties'].keys())
    ilen = len(feature['geometry']['coordinates'])
    for i,coordinate in enumerate(feature['geometry']['coordinates']):
        if i != ilen-1:
            cor_key1 = (feature['geometry']['coordinates'][i][1],feature['geometry']['coordinates'][i][0])
            cor_key2 = (feature['geometry']['coordinates'][i+1][1], feature['geometry']['coordinates'][i+1][0])
            print(cor_dic[cor_key1][0], cor_dic[cor_key2][0])
            arc_list[cor_dic[cor_key1][0]][cor_dic[cor_key2][0]]+=1

            distance = vincenty(cor_key1, cor_key2).km * 100  # 미터단위
            print(distance)
            distance_list[cor_dic[cor_key1][0]][cor_dic[cor_key2][0]] = distance

            if 'oneway' not in feature['properties'].keys():
                print(cor_dic[cor_key2][0], cor_dic[cor_key1][0])
                arc_list[cor_dic[cor_key2][0]][cor_dic[cor_key1][0]] += 1
                distance = vincenty(cor_key2, cor_key1).km * 100
                distance_list[cor_dic[cor_key2][0]][cor_dic[cor_key1][0]] = distance




###############################################시각화
Arc_tuple_List = []
for x,y in enumerate(arc_list):
    for i,j in enumerate(y):
        if arc_list[x,i] != False:
            Arc_tuple_List.append((x,i))
print(Arc_tuple_List)

new_node_dic = {}
for nodes in cor_dic.values():
    new_node_dic[nodes[0]] = node_dic[nodes[0]]

G = nx.DiGraph()
G.add_nodes_from(new_node_dic)
G.add_edges_from(Arc_tuple_List)
nx.draw(G, pos=new_node_dic,with_labels=True, node_size = 300, width=0.3)
plt.show()

