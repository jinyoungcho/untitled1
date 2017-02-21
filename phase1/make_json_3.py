from overpass import API
import json, io
from uszipcode import ZipcodeSearchEngine

api = API()
api.timeout=900

# response = str(api.Get('way["highway"]["highway"!~"footway|cycleway|path|track|pedestrian|steps|crossing'
#                        '|construction"](40.697655, -74.031030, 40.875447, -73.863863);'))
response = api.Get('way["highway"]["highway"!~"footway|cycleway|path|track|pedestrian|steps|crossing'
                       '|construction"](40.697655, -74.031030, 40.875447, -73.863863);')
# response = api.Get('way["highway"]["highway"!~"footway|cycleway|path|track|pedestrian|steps|crossing'
#                        '|construction"](40.760233, -74.026183, 40.767530, -73.985527);')


postcode_list = ["10025", "10024", "10040", "10009", "10027", "10003", "10014", "10012", "10005", "10004", "10019",
                 "10023", "10006", "10035", "10010", "10016", "10032", "10002", "10038", "10013", "10278", "10018",
                 "10036", "10128", "10280", "10037", "10028", "10115", "10029", "10031", "10039", "10026", "10044",
                 "10021", "10007", "10011", "10034", "10030", "10111", "10022", "10119", "10199", "10001", "10033",
                 "10282", "10065", "10075", "10173", "10165", "10168", "10174", "10112", "10020", "10103", "10017",
                 "10069", "10167", "10154", "10170"]

search = ZipcodeSearchEngine()
response2={"features":[]}
for features in response['features']:
    # print(features['geometry'], features['properties'])
    coordinates = features['geometry']['coordinates']
    for latlon in coordinates:
        sample_postcode = search.by_coordinate(latlon[1],latlon[0])[0]['Zipcode']
        # print(sample_postcode, type(sample_postcode))
        if sample_postcode in postcode_list:
            response2['features'].append(features)
            # print("get ya!")
            break

j_response2 = json.dumps(response2)
j_response = json.loads(j_response2)

with io.open('data3.json', 'w', encoding='utf8') as outfile:
    str_ = json.dumps(j_response,
                      indent=4, sort_keys=True,
                      separators=(',', ':'), ensure_ascii=False)
    outfile.write(str(str_))




# postcode_tuple=()
# for features in response['features']:
#     print(features['geometry'], features['properties'])
#     coordinates = features['geometry']['coordinates']
#     for latlon in coordinates:
#         sample_postcode = int(search.by_coordinate(latlon[1],latlon[0])[0]['Zipcode'])
#         postcode_tuple = postcode_tuple + (sample_postcode,)
#
# print(postcode_tuple)

