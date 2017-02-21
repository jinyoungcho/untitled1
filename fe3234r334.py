from geopy.geocoders import Nominatim

geolocator = Nominatim()
location = geolocator.reverse("40.7267,-74.0345")
# print(location.address)
# print((location.latitude, location.longitude))
print(location.raw['address']['postcode'])