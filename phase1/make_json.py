from overpass import API
import json, io

api = API()
api.timeout=900
# response = str(api.Get('way["tiger:county"= "New York, NY"]["highway"]["highway"!~"footway|cycleway|path|service|track|pedestrian|steps'
#                    'crossing|construction"];'))

response = str(api.Get('way["tiger:county"= "New York, NY"]["highway"]["highway"!~"footway|cycleway|path|service|track|pedestrian|steps'
                   'crossing|construction"];'))


j_response = json.loads(response)

with io.open('data.json', 'w', encoding='utf8') as outfile:
    str_ = json.dumps(j_response,
                      indent=4, sort_keys=True,
                      separators=(',', ':'), ensure_ascii=False)
    outfile.write(str(str_))