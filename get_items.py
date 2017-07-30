import dota2api
import pprint
import constants

api = dota2api.Initialise(constants.tok)

#pprint.PrettyPrinter(width=1).pprint(api.get_game_items())

f = open("items.py", "w+")

a = {}
for i in api.get_game_items()["items"]:
    a[i["id"]] = i["localized_name"]
f.write("items = " + str(a))
f.close()