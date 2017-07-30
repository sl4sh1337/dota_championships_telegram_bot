def get_name(player_id):
    import urllib.request

    hdr = {'User-Agent': 'qeq'}
    req = urllib.request.Request("http://www.dotabuff.com/players/" + str(player_id), headers=hdr)
    html = str(urllib.request.urlopen(req).read())
    x = html.find('<div class="header-content-title">') + len('<div class="header-content-title">')
    y = html.find('<small>Overview', x)
    return html[x + 4:y]


def painter(id, player_id, teams, compare, match_id, path):
    from PIL import Image
    from PIL import ImageDraw
    from PIL import ImageFont
    import heroes
    import source
    import os

    template = Image.open("template.png")
    background = Image.new('RGBA', (1366, 703), (255, 255, 255, 255))

    draw = ImageDraw.Draw(template)
    font_hero = ImageFont.truetype("/home/sl4sh/.fonts/truetype/msttcorefonts/Arial.ttf", 13)
    font_player = ImageFont.truetype("/home/sl4sh/.fonts/truetype/msttcorefonts/Arial.ttf", 14)
    font_team = ImageFont.truetype("/home/sl4sh/.fonts/truetype/msttcorefonts/Arial.ttf", 40)

    for i in range(10):
        hero = Image.open("heroes/" + str(id[i]) + ".jpg")
        background.paste(hero, source.hero_coords[i])

        text_wigth, text_height = draw.textsize(heroes.heroes[id[i]], font=font_hero)
        temp_heroname_x, heroname_y = source.heroname_coords[i]
        final_heroname_coords = (((150 - text_wigth) // 2) + temp_heroname_x, heroname_y)
        draw.text(final_heroname_coords, heroes.heroes[id[i]], font=font_hero)

        player_name = compare[player_id[i]]
        player_name_wigth, player_name_height = draw.textsize(player_name, font=font_player)
        temp_player_name_x, player_name_y = source.heroname_coords[i]
        final_player_name_coords = (((150 - player_name_wigth) // 2) + temp_player_name_x, player_name_y + 176)
        draw.text(final_player_name_coords, player_name, font=font_player)

    draw.text(source.team_coords[0], teams[0], font=font_team, fill=(178, 210, 103, 255))
    draw.text(source.team_coords[1], teams[1], font=font_team, fill=(162, 102, 78, 255))

    os.makedirs(path)
    Image.alpha_composite(background, template).save(path + "/pick.png")


def result_painter(players, time, match_id, compare, teams, winner, path):
    from PIL import Image, ImageFont, ImageDraw
    import heroes
    import source
    import os

    font = ImageFont.truetype("/home/sl4sh/.fonts/truetype/msttcorefonts/Arial.ttf", 9)
    time_font = ImageFont.truetype("/home/sl4sh/.fonts/truetype/msttcorefonts/Arial.ttf", size=12)
    id_font = ImageFont.truetype("/home/sl4sh/.fonts/truetype/msttcorefonts/Arial.ttf", size=11)
    team_font = ImageFont.truetype("/home/sl4sh/.fonts/truetype/msttcorefonts/Arial.ttf", size=16)
    winner_font = ImageFont.truetype("/home/sl4sh/.fonts/truetype/msttcorefonts/Arial.ttf", size=22)
    bg = Image.open("result_template.png")
    background = Image.new('RGBA', (820, 405), (255, 255, 255, 255))
    background.paste(bg, (0, 0))
    draw = ImageDraw.Draw(background)

    for i in range(10):
        name = compare[players[i]["account_id"]]
        draw.text((source.result_coords["x"][0] + 3, source.result_coords["y"][i] + 3), name, font=font)

        level = players[i]["level"]
        draw.text((source.result_coords["x"][1] + 3, source.result_coords["y"][i] + 3), str(level), font=font)

        hero = Image.open("./small_heroes/" + str(players[i]["hero_id"]) + ".png")
        background.paste(hero, (source.result_coords["x"][2], source.result_coords["y"][i]))

        heroname = heroes.heroes[players[i]["hero_id"]]
        draw.text((source.result_coords["x"][3] + 3, source.result_coords["y"][i] + 3), heroname, font=font)

        kill = players[i]["kills"]
        draw.text((source.result_coords["x"][4] + 3, source.result_coords["y"][i] + 3), str(kill), font=font)

        death = players[i]["deaths"]
        draw.text((source.result_coords["x"][5] + 3, source.result_coords["y"][i] + 3), str(death), font=font)

        assist = players[i]["assists"]
        draw.text((source.result_coords["x"][6] + 3, source.result_coords["y"][i] + 3), str(assist), font=font)

        for j in range (6):
            if players[i]["item_" + str(j)] > 0:
                if os.path.isfile("items/" + str(players[i]["item_" + str(j)]) + ".png"):
                    item = Image.open("items/" + str(players[i]["item_" + str(j)]) + ".png")
                else:
                    item = Image.open("items/1001.png")
                background.paste(item, (source.result_coords["x"][7] + 19 * j, source.result_coords["y"][i]))


        gold = str(players[i]["gold"])
        w, h = draw.textsize(gold, font=font)
        draw.text((source.result_coords["x"][8] + 54 - 3 - w, source.result_coords["y"][i] + 3), gold, font=font, fill="yellow")

        lh = str(players[i]["last_hits"])
        w, h = draw.textsize(lh, font=font)
        draw.text((source.result_coords["x"][9] + 44 - 3 - w, source.result_coords["y"][i] + 3), lh, font=font)

        dn = str(players[i]["denies"])
        w, h = draw.textsize(dn, font=font)
        draw.text((source.result_coords["x"][10] + 44 - 3 - w, source.result_coords["y"][i] + 3), dn, font=font)

        gpm = str(players[i]["gold_per_min"])
        w, h = draw.textsize(gpm, font=font)
        draw.text((source.result_coords["x"][11] + 44 - 3 - w, source.result_coords["y"][i] + 3), gpm, font=font)

        xpm = str(players[i]["xp_per_min"])
        w, h = draw.textsize(xpm, font=font)
        draw.text((source.result_coords["x"][12] + 44 - 3 - w, source.result_coords["y"][i] + 3), xpm, font=font)

    draw.text((720, 27), "{}:{}{}".format(str(time // 60), str((time % 60) // 10), str((time % 60) % 10)), font=time_font)

    draw.text((70, 34), str(match_id), font=id_font)
    wid, hei = draw.textsize(str(match_id), font=id_font)
    draw.text((70, 34 + hei + 7), teams[0], font=team_font, fill=(178, 210, 103, 255))
    draw.text((70, 206), teams[1], font=team_font, fill=(162, 102, 78, 255))

    if winner:
        returned_team =  teams[0]
        win_str = teams[0].upper() + " VICTORY"
        win_w, win_h = draw.textsize(win_str, font=winner_font)
        draw.text(((820 - win_w) // 2, 10), win_str, font=winner_font)
    else:
        returned_team = teams[1]
        win_str = teams[1].upper() + " VICTORY"
        win_w, win_h = draw.textsize(win_str, font=winner_font)
        draw.text(((820 - win_w) // 2, 10), win_str, font=winner_font)

    background.save(path + "/result.png")

    return returned_team