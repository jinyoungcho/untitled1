from uszipcode import ZipcodeSearchEngine
search = ZipcodeSearchEngine()
a = search.by_coordinate(40.8579417,-73.9591453)[0]['Zipcode']
print(a)