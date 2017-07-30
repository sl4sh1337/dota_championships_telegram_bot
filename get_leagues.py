import dota2api
import pprint
import constants

api = dota2api.Initialise(constants.tok)

#pprint.PrettyPrinter(width=1).pprint(api.get_league_listing().url)

f = open("league.py", "w+", encoding='utf-8')

a = {}
for i in api.get_league_listing()["leagues"]:
    a[i["leagueid"]] = i["name"]
f.write("leagues = " + str(a))
f.close()
