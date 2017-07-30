def print_builds(dire_tower_status, dire_barracks_status, radiant_tower_status, radiant_barracks_status):
    mask = 1
    dr_tow = [18, 14, 10, 19, 15, 11, 20, 16, 12, 0, 1]
    dr_bar = [4, 3, 6, 5, 8, 7]
    rd_tow = [0, 4, 8, 1, 5, 9, 2, 6, 10, 19, 20]
    rd_bar = [13, 12, 15, 14, 17, 16]
    dire = [
        ".......", "...", "\n",
        "", "", "", "", "", "", "\n",
        "..", ".....", ".....", "\n",
        "..", ".....", ".....", "\n",
        "..", ".....", ".....", "\n\n"
    ]
    radiant = [
        "..", ".....", ".....", "\n",
        "..", ".....", ".....", "\n",
        "..", ".....", ".....", "\n",
        "", "", "", "", "", "", "\n",
        ".......", "...", "\n"
    ]

    for i in range(11):
        if dire_tower_status & mask:
            dire[dr_tow[i]] += "✅"
        else:
            dire[dr_tow[i]] += "❌"
        mask <<= 1
    mask = 1
    for i in range(6):
        if dire_barracks_status & mask:
            dire[dr_bar[i]] += "✅"
        else:
            dire[dr_bar[i]] += "❌"
        mask <<= 1
    mask = 1
    for i in range(11):
        if radiant_tower_status & mask:
            radiant[rd_tow[i]] += "✅"
        else:
            radiant[rd_tow[i]] += "❌"
        mask <<= 1
    mask = 1
    for i in range(6):
        if radiant_barracks_status & mask:
            radiant[rd_bar[i]] += "✅"
        else:
            radiant[rd_bar[i]] += "❌"
        mask <<= 1
    return ''.join(dire) + ''.join(radiant)


def get_stats(path, i):
    import ast
    import heroes
    import items

    f = open(path + "/teams")
    teams = f.readlines()
    f.close()
    f = open(path + "/compare", "r")
    compare = ast.literal_eval(f.read())
    pl_stats = "\n"
    f.close()
    duration = "Длительность: " + str(int(i["scoreboard"]["duration"] // 60)).rjust(2, "0") + ":" + str(int(i["scoreboard"]["duration"] % 60)).rjust(2, "0")
    radiant_nw = 0
    dire_nw = 0
    score_ra = 0
    score_di = 0
    pl_stats = pl_stats + teams[0][:-1] + ":\n\n"
    for j in i["scoreboard"]["radiant"]["players"]:
        score_ra = score_ra + j["kills"]
        radiant_nw = radiant_nw + j["net_worth"]
        pl_stats = pl_stats + compare[j["account_id"]] + "\n" + heroes.heroes[j["hero_id"]] + "\nKDA: " + str(j["kills"]) + " " + str(j["death"]) + " " + str(j["assists"]) + "\nCreepStat: " + str(j["last_hits"]) + "/" + str(j["denies"]) + "\nItems: "
        its = []
        for k in range(6):
            if j["item" + str(k)] != 0:
                its.append(items.items[j["item" + str(k)]])
        pl_stats = pl_stats + ", ".join(its) + "\n\n"
    pl_stats = pl_stats + "\n" + teams[1] + ":\n\n"
    for j in i["scoreboard"]["dire"]["players"]:
        score_di = score_di + j["kills"]
        dire_nw = dire_nw + j["net_worth"]
        pl_stats = pl_stats + compare[j["account_id"]] + "\n" + heroes.heroes[j["hero_id"]] + "\nKDA: " + str(j["kills"]) + " " + str(j["death"]) + " " + str(j["assists"]) + "\nCreepStat: " + str(j["last_hits"]) + "/" + str(j["denies"]) + "\nItems: "
        its = []
        for k in range(6):
            if j["item" + str(k)] != 0:
                its.append(items.items[j["item" + str(k)]])
        pl_stats = pl_stats + ", ".join(its) + "\n\n"
    nw_difference = radiant_nw - dire_nw
    score = "Текущий счёт: " + teams[0][:-1] + " " + str(score_ra) + ":" + str(score_di) + " " + teams[1]
    if nw_difference > 0:
        advantage = "Преимущество команды " + teams[0][:-1] + " " + str(nw_difference) + " золота"
    elif nw_difference < 0:
        advantage = "Преимущество команды " + teams[1] + " " + str(nw_difference * -1) + " золота"
    else:
        advantage = "Команды имеют равные нетворсы"
    buildings = teams[1] + "\n" + print_builds(i["scoreboard"]["dire"]["tower_state"], i["scoreboard"]["dire"]["barracks_state"], i["scoreboard"]["radiant"]["tower_state"], i["scoreboard"]["radiant"]["barracks_state"]) + teams[0][:-1] + "\n"
    return duration +"\n" + score + "\n" + advantage + "\n\n" + buildings + "\n" + pl_stats


def make_result(result, path):
    import painter
    import ast
    teams = []
    try:
        teams.append(result["radiant_name"])
    except:
        teams.append("Radiant")
    try:
        teams.append(result["dire_name"])
    except:
        teams.append("Dire")
    f = open(path + "/compare", "r")
    compare = ast.literal_eval(f.read())
    f.close()
    winner = painter.result_painter(result["players"], result["duration"], result["match_id"], compare, teams, result["radiant_win"], path)
    return winner


def make_picks(match, path):
    import painter
    compare = {}
    id = []
    player_id = []
    teams = []
    for j in match["players"]:
        if j["team"] == 0 or j["team"] == 1:
            compare[j["account_id"]] = j["name"]
    for j in match["scoreboard"]["radiant"]["players"]:
        id.append(j["hero_id"])
        player_id.append(j["account_id"])
    for j in match["scoreboard"]["dire"]["players"]:
        id.append(j["hero_id"])
        player_id.append(j["account_id"])
    try:
        teams.append(match["radiant_team"]["team_name"])
    except:
        teams.append("Radiant")
    try:
        teams.append(match["dire_team"]["team_name"])
    except:
        teams.append("Dire")
    if len(id) == 10 and not (0 in id):
        try:
            painter.painter(id, player_id, teams, compare, match["match_id"], path)
            f = open(path + "/compare", "w+")
            f.write(str(compare))
            f.close()
            f = open(path + "/teams", "w+")
            f.write("\n".join(teams))
            f.close()
        except KeyError:
            pass
