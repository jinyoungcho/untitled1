from overpass import API
import numpy as np
from collections import defaultdict
from geopy.distance import vincenty
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx

api = API()
api.timeout=900
# response = api.Get('way["highway"]["highway"!~"footway|cycleway|path|service|track|pedestrian|steps|crossing"](40.751872, -73.994120 ,40.762353, -73.979678);')
response = api.Get('way["tiger:county"= "New York, NY"]["highway"]["highway"!~"footway|cycleway|path|service|track|pedestrian|steps"];')

node_dic={}
cor_dic=defaultdict(list)
x = 0
for features in response['features']:
    for coordinate in features['geometry']['coordinates']:
        node_dic[x] = (coordinate[1], coordinate[0])
        x += 1

for node_num in node_dic:
    cor_dic[node_dic[node_num]].append(node_num)

intersection_cor_dic = {} #key(노드번호) value(위도경도)  #{0: (40.752814, -73.981372), 259: (40.753481, -73.980888)
cor_intersection_dic={}   # key(위도경도) value(노드번호)    #(40.7572592, -73.9858201): [406, 416]

for a in cor_dic:
    if len(cor_dic[a])>=2:
        cor_intersection_dic[a]=cor_dic[a][0]
        intersection_cor_dic[cor_dic[a][0]]=a


node_size = len(node_dic)
distance_list = np.zeros((node_size,node_size),dtype='float')

for feature in response['features']:
    corlist = feature['geometry']['coordinates']
    i = 0                                                                       # i와 j를 먼저 생성
    j = 1
    for i in range(len(corlist)-1):
        distance=0
        for j in range(i+1,len(corlist)):
            cor_key1 = (corlist[i][1],corlist[i][0])
            cor_key2 = (corlist[j][1],corlist[j][0])
            distance += vincenty((corlist[j-1][1],corlist[j-1][0]), (corlist[j][1],corlist[j][0])).km * 100  # i1 j(n) 누적으로 더한 값들 // 단위는 m로 했습니다.
            if cor_key1 in cor_intersection_dic.keys():                         # i가 intersection노드 안에 포함이 되있고
                if cor_key2 in cor_intersection_dic.keys():                     # j도 intersection노드 안에 포함이 되 있으면
                    distance_list[cor_intersection_dic[cor_key1]][cor_intersection_dic[cor_key2]] = distance # i 와 j 의 거리를 합한 값을 distance_list에 넣어준다
                    break
            else:
                break


Arc_tuple_List = []  ##(0, 3), (0, 72), (3, 339), (18, 31), (18, 124), (19, 22), (19, 66), (22, 169), (22, 179)
                         #(i,j) 입니다
for x,y in enumerate(distance_list):
    for i,j in enumerate(y):
        if distance_list[x,i] != False:
            Arc_tuple_List.append((x,i))


##
df = pd.DataFrame()
arc_i_list = [arc[0] for arc in Arc_tuple_List]
arc_j_list = [arc[1] for arc in Arc_tuple_List]
arc_distace_list = [distance_list[arc[0]][arc[1]] for arc in Arc_tuple_List]

df["i"] = arc_i_list
df["j"] = arc_j_list
df["distance"] = arc_distace_list
df.to_csv("distance.csv")


# G = nx.DiGraph()
# G.add_nodes_from(intersection_cor_dic)
# G.add_edges_from(Arc_tuple_List)
# nx.draw(G,with_labels=True, node_size = 300, width=0.3)
# plt.show()