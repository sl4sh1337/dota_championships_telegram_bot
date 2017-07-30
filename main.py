import dota2api
import constants
import sys
import os
import dota
import time
import telebot

import sqlite3
connection = sqlite3.connect("db.db")


def get_users_list():
    global connection
    cur = connection.cursor()
    return cur.execute("SELECT * FROM Users").fetchall()

timer = time.time()
bot = telebot.TeleBot(constants.teletok)
api = dota2api.Initialise(constants.tok)

if __name__ == '__main__':
    while True:
        try:
            curtime = time.time()
            gotten = False
            while not gotten:
                try:
                    live = api.get_live_league_games()["games"]
                    for i in live:
                        teams = []
                        try:
                            teams.append(i["radiant_team"]["team_name"])
                        except:
                            teams.append("Radiant")
                        try:
                            teams.append(i["dire_team"]["team_name"])
                        except:
                            teams.append("Dire")
                        teams.sort()
                        path = "live/" + ' vs. '.join(teams) + "/" + str(i["match_id"]) + "l"
                        path1 = "live/" + ' vs. '.join(teams) + "/" + str(i["match_id"]) + "f"
                        if ("scoreboard" in i) and (i["scoreboard"]["duration"] > 0) and not os.path.exists(path) and not os.path.exists(path1) and i["league_tier"] > 1:
                            dota.make_picks(i, path)
                            f = open(path + "/stat", "w+")
                            f.close()

                            usrs = get_users_list()
                            tm = time.time()

                            numba = str(len(os.listdir("live/" + ' vs. '.join(teams) + "/")))
                            caption = ' vs. '.join(teams) + "| Игра № " + numba

                            for k in range(len(usrs)):
                                if usrs[k][1] == "a":
                                    img = open(path + "/pick.png", "rb")
                                    try:
                                        bot.send_photo(int(usrs[k][0]), img, caption=caption)
                                        img.close()
                                    except:
                                        img.close()
                                        pass
                                elif usrs[k][1] == "w":
                                    try:
                                        bot.send_message(int(usrs[k][0]), "Начался матч\n" + caption + "\nЧтобы узнать пики команд, перешлите это сообщение боту", disable_web_page_preview=True)
                                    except:
                                        pass
                                if (k + 1) % 30 == 0:
                                    if time.time() - tm <= 1:
                                        time.sleep(1)
                                    tm = time.time()

                        elif os.path.exists(path) and (curtime - timer) > 20:
                            stata = dota.get_stats(path, i)
                            f = open(path + "/stat", "w")
                            f.write(stata)
                            f.close()

                        gotten = True
                except dota2api.src.exceptions.APITimeoutError:
                    time.sleep(2)
                    pass

                if os.path.exists("live/"):
                    for j in os.listdir("live/"):
                        for live in os.listdir("live/" + j):
                            flag = False
                            while not flag:
                                try:
                                    if live[-1] == "l":
                                        winna = ""
                                        result = api.get_match_details(int(live[:-1]))
                                        winna = dota.make_result(result, "live/" + j + "/"  + live)

                                        os.rename("live/" + j + "/"  + live, "live/" + j + "/" + live[:-1] + "f")
                                        f = open("live/" + j + "/" + live[:-1] + "f/winner", "w+")
                                        f.write(winna)
                                        f.close()

                                        usrs1 = get_users_list()
                                        tm = time.time()
                                        numba = str(len(os.listdir("live/" + j + "/")))
                                        caption = j + "| Игра № " + numba

                                        for k in range(len(usrs1)):
                                            if usrs1[k][1] == "a":
                                                img = open("live/" + j + "/" + live[:-1] + "f" + "/result.png", "rb")
                                                try:
                                                    bot.send_photo(int(usrs1[k][0]), img, caption=caption)
                                                    img.close()
                                                except:
                                                    img.close()
                                                    pass
                                            elif usrs1[k][1] == "w":
                                                try:
                                                    bot.send_message(int(usrs1[k][0]), "Закончился матч\n" + caption + "\nПобедила команда " + winna + ". Чтобы узнать подробности, перешлите это сообщение боту", disable_web_page_preview=True)
                                                except:
                                                    pass
                                            if (k + 1) % 30 == 0:
                                                if time.time() - tm <= 1:
                                                    time.sleep(1)
                                                tm = time.time()


                                    flag = True
                                except dota2api.src.exceptions.APIError:
                                    flag = True
                                    pass
                                except dota2api.src.exceptions.APITimeoutError:
                                    time.sleep(2)
                                    pass
            if (curtime - timer) > 20:
                timer = curtime
        except KeyboardInterrupt:
            sys.exit()

        except:
            pass
