from overpass import API
import numpy as np
from collections import defaultdict
from geopy.distance import vincenty
import pandas as pd


def make_ARCS(lat1,lon1,lat2,lon2): #좌하 우상 위도경도 입력
    api = API() #overpass API객체 불러오기
    api.timeout=900 # 검색시간 default값이 60초라서 900로 늘려줌

    # response = api.Get('way["highway"]["highway"~"motorway|trunk"](40.701274, -74.033596, 40.807903, -73.931286);') 예시
    response = api.Get('way["highway"]["highway"~"motorway|trunk"]({}, {}, {}, {});'.format(lat1,lon1,lat2,lon2)) #위도경도 값을 넣어서 motorway와 trunk인 고속도로 return

################################################################################


    node_dic={}                     # key(노드번호) value(위도경도)         #{0: (40.752814, -73.981372), 1: (40.7527642, -73.9812537), 2: (40.7521797, -73.9798676), 3: (40.7521385, -73.9797698)
    cor_dic=defaultdict(list)       # key(위도경도) value(노드번호_list)    #(40.7572592, -73.9858201): [406, 416], (40.7507266, -73.9879255): [94], (40.7534284, -73.9807633): [527]
    x = 0
    for features in response['features']:
        for coordinate in features['geometry']['coordinates']:
            node_dic[x] = (coordinate[1], coordinate[0])
            x += 1
    for node_num in node_dic:
        cor_dic[node_dic[node_num]].append(node_num)
################################################################################

#같은 위도경도에 노드번호가 2개이상 이라면 intersection//
    #-> intersection들만 모아서 dictionary를 생성

    intersection_cor_dic = {} #key(노드번호) value(위도경도)  #{0: (40.752814, -73.981372), 259: (40.753481, -73.980888)
    cor_intersection_dic={}   # key(위도경도) value(노드번호)    #(40.7572592, -73.9858201): [406, 416]

    for a in cor_dic:
        if len(cor_dic[a])>=2:
            cor_intersection_dic[a]=cor_dic[a][0]
            intersection_cor_dic[cor_dic[a][0]]=a


###############################################################################
        #-> intersection갯수 만큼의 2차형 어레이 생성
    node_size = len(node_dic)
    distance_list = np.zeros((node_size,node_size),dtype='float')
###############################################################################

    #response안에 들어있는 좌표(coordinates)들을 꺼냄

    # (글로 설명하기 어렵습니다 제가 하나하나 확인해봤는데 잘 작동합니다..!
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

###############################################
                # 데이터로 만들기 csv파일로 만들었습니다
                # 패키지는 pandas를 이용하였습니다

    Arc_tuple_List = []  ##(0, 3), (0, 72), (3, 339), (18, 31), (18, 124), (19, 22), (19, 66), (22, 169), (22, 179)
                         #(i,j) 입니다
    for x,y in enumerate(distance_list):
        for i,j in enumerate(y):
            if distance_list[x,i] != False:
                Arc_tuple_List.append((x,i))

    df = pd.DataFrame()

    arc_i_list = [arc[0]for arc in Arc_tuple_List]
    arc_j_list = [arc[1]for arc in Arc_tuple_List]
    arc_distace_list = [distance_list[arc[0]][arc[1]]for arc in Arc_tuple_List]

    df["i"] = arc_i_list
    df["j"] = arc_j_list
    df["distance"] = arc_distace_list
    df.to_csv("distance.csv") #@#@@##$@#@#$@#$@#%T%%%/<<----------- 빈 csv파일 생성하고 이름을 distance로 먼저 만들어 주셔야 합니다 그다음 실행시키면 저장이 됩니다.

make_ARCS(40.701274, -74.033596, 40.807903, -73.921286)   ##먼저 모든 node들을 list에 담고 그다음 intersection인지 확인을 해서 그런지 너무 크게 좌표를 잡으면 에러가 발생합니다..
