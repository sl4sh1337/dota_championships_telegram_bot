import dota2api
import pprint
import constants

api = dota2api.Initialise(constants.tok)

#pprint.PrettyPrinter(width=1).pprint(api.get_heroes())

f = open("heroes.py", "w+")

a = {}
for i in api.get_heroes()["heroes"]:
    a[i["id"]] = i["localized_name"]
f.write("heroes = " + str(a))
f.close()
