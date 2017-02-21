from collections import defaultdict
from geopy.distance import vincenty
import json, io
import matplotlib.pyplot as plt
import networkx as nx

with open('data3.json', encoding='utf-8') as data_file:
    response = json.loads(data_file.read())

node_dic={}
cor_dic=defaultdict(list)
x = 0
for features in response['features']:
    for coordinate in features['geometry']['coordinates']:
        node_dic[x] = (coordinate[1], coordinate[0])
        x += 1

for node_num in node_dic:
    cor_dic[node_dic[node_num]].append(node_num)

#####################################################################################################################

distance_dic={}
street_dic={}

for feature in response['features']:
    sample_coordinates = []
    coordinates = feature['geometry']['coordinates']
    for cor in coordinates:
        if (cor[1],cor[0]) in cor_dic.keys():
            sample_coordinates.append((cor[1],cor[0]))
    for i in range(len(sample_coordinates)-1):
        cor_i = sample_coordinates[i]
        cor_j = sample_coordinates[i+1]
        distance_dic[cor_dic[cor_i][0], cor_dic[cor_j][0]] = vincenty(cor_i,cor_j).km*100
        if "name" in feature["properties"]:
            street_dic[cor_dic[cor_i][0], cor_dic[cor_j][0]] = feature["properties"]["name"]
        else:
            street_dic[cor_dic[cor_i][0], cor_dic[cor_j][0]] = "unknown"
            print(feature["properties"])
            print(feature['geometry']['coordinates'])
            print("-----")
        if "oneway" not in feature["properties"].keys():
            distance_dic[cor_dic[cor_j][0], cor_dic[cor_i][0]] = vincenty(cor_j, cor_i).km * 100
            if "name" in feature["properties"]:
                street_dic[cor_dic[cor_j][0], cor_dic[cor_i][0]] = feature["properties"]["name"]
            else:
                street_dic[cor_dic[cor_j][0], cor_dic[cor_i][0]] = "unknown"

Arc_tuple_List = []
for key in distance_dic.keys():
    Arc_tuple_List.append((key[0],key[1]))

# for a in Arc_tuple_List: ## selfdirected 찾기
#     if a[0]==a[1]:
#         print(a)

G = nx.Graph()
G.add_nodes_from(node_dic)
G.add_edges_from(Arc_tuple_List)
# print(nx.number_connected_components(G))
nx.draw(G,pos=node_dic,with_labels=True, node_size = 0, width=0.1)
plt.show()

# x = True
# while(x == True):
#     useless_node_list = [node for node in G.in_degree() if G.in_degree()[node] == 1 and G.out_degree()[node] == 0]
#     useless_arc_list = []
#     for Arc in Arc_tuple_List:
#         if Arc[1] in useless_node_list:
#             useless_arc_list.append(Arc)
#
#     print(useless_node_list)
#     print(useless_arc_list)
#     if len(useless_node_list) == 0:
#         x = False
#     else:
#         for useless_node in useless_node_list:
#             if useless_node in node_dic.keys():
#                 print(useless_node)
#                 del node_dic[useless_node]
#         for useless_arc in useless_arc_list:
#             if useless_arc in Arc_tuple_List:
#                 Arc_tuple_List.remove(useless_arc)
#         G.remove_nodes_from(useless_node_list)


# plt.show()
# plt.savefig("graph.png", dpi=1000)
# plt.savefig("graph.pdf")