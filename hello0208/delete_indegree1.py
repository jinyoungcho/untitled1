from overpass import API
import numpy as np
from collections import defaultdict
from geopy.distance import vincenty
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx

api = API()
api.timeout=900
response = api.Get('way["tiger:county"= "New York, NY"]["highway"]["highway"!~"footway|cycleway|path|service|track|pedestrian|steps'
                   'crossing|construction"];')




node_dic={}
cor_dic=defaultdict(list)
x = 0
for features in response['features']:
    # print(features)
    for coordinate in features['geometry']['coordinates']:
        node_dic[x] = (coordinate[1], coordinate[0])
        x += 1

print("node_dic: ", node_dic)

for node_num in node_dic:
    cor_dic[node_dic[node_num]].append(node_num)

# for i in cor_dic:
    # cor_dic[i].sort()

print("cor_dic: ", cor_dic)

intersection_cor_dic = {} #key(노드번호) value(위도경도)  #{0: (40.752814, -73.981372), 259: (40.753481, -73.980888)
cor_intersection_dic={}   # key(위도경도) value(노드번호)    #(40.7572592, -73.9858201): [406, 416]

for key in cor_dic:
    if len(cor_dic[key]) > 1:
        cor_intersection_dic[key] = cor_dic[key][0]
        intersection_cor_dic[cor_dic[key][0]] = key

print(intersection_cor_dic)
print(cor_intersection_dic)


intersection_size = len(intersection_cor_dic)
distance_dic={}

for feature in response['features']:
    sample_coordinates = []
    coordinates = feature['geometry']['coordinates']
    for cor in coordinates:
        if (cor[1],cor[0]) in cor_intersection_dic.keys():
            sample_coordinates.append((cor[1],cor[0]))

    print("1-", coordinates)
    print("2-", sample_coordinates)
    print("3-", [cor_dic[cor] for cor in sample_coordinates])
    print(feature["properties"])
    # if "turn:lanes" in feature["properties"].keys():
    for i in range(len(sample_coordinates)-1):
        cor_i = sample_coordinates[i]
        cor_j = sample_coordinates[i+1]
        distance_dic[cor_intersection_dic[cor_i], cor_intersection_dic[cor_j]] = vincenty(cor_i,cor_j).km*100


print(distance_dic)


Arc_tuple_List = []  ##(0, 3), (0, 72), (3, 339), (18, 31), (18, 124), (19, 22), (19, 66), (22, 169), (22, 179)
                         #(i,j) 입니다
for key in distance_dic.keys():
    Arc_tuple_List.append((key[0],key[1]))

df = pd.DataFrame()

arc_i_list = [arc[0]for arc in Arc_tuple_List]
arc_j_list = [arc[1]for arc in Arc_tuple_List]
arc_distace_list = [distance_dic[arc[0],arc[1]]for arc in Arc_tuple_List]



print(arc_i_list)
print(arc_j_list)
print(arc_distace_list)
print(distance_dic)



# df["i"] = arc_i_list
# df["j"] = arc_j_list
# df["distance"] = arc_distace_list
# df.to_csv("distance.csv") #@#@@##$@#@#$@#$@#%T%%%/<<----------- 빈 csv파일 생성하고 이름을 distance로 먼저 만들어 주셔야 합니다 그다음 실행시키면 저장이 됩니다.



# Arc_tuple_List = []
# for x,y in enumerate(arc_list):
#     for i,j in enumerate(y):
#         if arc_list[x,i] != False:
#             Arc_tuple_List.append((x,i))

#
G = nx.DiGraph()
G.add_nodes_from(intersection_cor_dic)
G.add_edges_from(Arc_tuple_List)
# nx.draw(G, pos=intersection_cor_dic,with_labels=True, node_size = 500, width=0.3)
# plt.show()

node_indegree_dic =  G.in_degree()
node_outdegree_dic = G.out_degree()



print(node_indegree_dic)

print([a for a in zip(node_indegree_dic.keys() , node_outdegree_dic.keys())])

useless_intersection = []
for nodes in zip(node_indegree_dic.keys() , node_outdegree_dic.keys()):
    # print(nodes[0], nodes[1])
    if (node_indegree_dic[nodes[0]] == 1 and node_outdegree_dic[nodes[1]] == 0):
        print(nodes[0])
        useless_intersection.append(nodes[0])
        del intersection_cor_dic[nodes[0]]

print(Arc_tuple_List)
print(useless_intersection)
for i in Arc_tuple_List:
    if i[0] in useless_intersection or i[1] in useless_intersection:
        Arc_tuple_List.remove(i)


G1 = nx.DiGraph()
G1.add_nodes_from(intersection_cor_dic)
G1.add_edges_from(Arc_tuple_List)

#######
node_indegree_dic =  G1.in_degree()
node_outdegree_dic = G1.out_degree()

useless_intersection = []
for nodes in zip(node_indegree_dic.keys() , node_outdegree_dic.keys()):
    # print(nodes[0], nodes[1])
    if (node_indegree_dic[nodes[0]] == 1 and node_outdegree_dic[nodes[1]] == 0):
        print(nodes[0])
        useless_intersection.append(nodes[0])
        del intersection_cor_dic[nodes[0]]

print(Arc_tuple_List)
print(useless_intersection)
for i in Arc_tuple_List:
    if i[0] in useless_intersection or i[1] in useless_intersection:
        Arc_tuple_List.remove(i)
##########
# nx.draw(G1, pos=intersection_cor_dic,with_labels=True, node_size = 500, width=0.3)
# plt.show()