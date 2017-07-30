import telebot
import constants
import os
import re

import sqlite3



def user_exists(user_id):
    connection = sqlite3.connect("db.db")
    cur = connection.cursor()
    result = cur.execute("SELECT user_id FROM Users WHERE user_id=?", (user_id, )).fetchall()
    connection.close()
    if len(result) == 1:
        return True
    else:
        return False


def create_user(user_id):
    connection = sqlite3.connect("db.db")
    cur = connection.cursor()
    cur.execute("INSERT INTO Users VALUES(?, ?)", (user_id, 'a'))
    connection.commit()
    connection.close()


def get_user_status(user_id):
    connection = sqlite3.connect("db.db")
    cur = connection.cursor()
    result = cur.execute("SELECT status FROM Users WHERE user_id=?", (user_id,)).fetchall()[0][0]
    connection.close()
    return result


def change_user_status(user_id, status):
    connection = sqlite3.connect("db.db")
    cur = connection.cursor()
    cur.execute("UPDATE Users SET status=? WHERE user_id=?", (status, user_id))
    connection.commit()
    connection.close()

bot = telebot.TeleBot(constants.teletok)


@bot.message_handler(commands=["start"])
def start(message):
    print(user_exists(message.from_user.id))
    #userfile = "users/" + str(message.from_user.id)
    if not user_exists(message.from_user.id):
        create_user(message.from_user.id)
    keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
    keyboard.row("Список текущих матчей")
    keyboard.row("Недавние матчи")
    bot.send_message(message.from_user.id, "Добро пожаловать!", reply_markup=keyboard)


@bot.message_handler(commands=["images"])
def start(message):
    #userfile = "users/" + str(message.from_user.id)
    status = get_user_status(message.from_user.id)
    if status == 'a':
        #os.rename(userfile + "a", userfile + "w")
        change_user_status(message.from_user.id, 'w')
        bot.send_message(message.from_user.id, "Отправка изображений отключена")
    elif status == 'w':
        #os.rename(userfile + "w", userfile + "a")
        change_user_status(message.from_user.id, 'a')
        bot.send_message(message.from_user.id, "Отправка изображений включена")
    elif status == 'o':
        bot.send_message(message.from_user.id, "У вас отключена возможность отправки уведомлений о матчах. Чтобы включить её, отправьте команду /notifications")


@bot.message_handler(commands=["notifications"])
def start(message):
    #userfile = "users/" + str(message.from_user.id)
    status = get_user_status(message.from_user.id)
    if status == 'a':
        change_user_status(message.from_user.id, 'o')
        bot.send_message(message.from_user.id, "Уведомления о матчах отключены")
    elif status == 'w':
        change_user_status(message.from_user.id, 'o')
        bot.send_message(message.from_user.id, "Уведомления о матчах отключены")
    elif status == 'o':
        change_user_status(message.from_user.id, 'a')
        bot.send_message(message.from_user.id, "Уведомления о матчах включены")


@bot.message_handler(content_types=["text"])
def text(message):
    if "|" in message.text and "\n" not in message.text:
        first = message.text.find("|")
        sec = message.text.rfind("|")
        if message.text[:first] == "m":
            keyboard = telebot.types.ReplyKeyboardMarkup(True, False)
            keyboard.row("Недавние матчи")
            match = message.text[first + 1:]
            if os.path.exists("live/" + match):
                counter = 1
                for i in sorted(os.listdir("live/" + match)):
                    row = "g|" + match + "| Игра № " + str(counter)
                    if i[-1] == "l":
                        row += " (Идёт сейчас)"
                    elif i[-1] == "f":
                        f = open("live/" + match + "/" + i + "/winner", "r")
                        row += " (Победила команда " + f.read() + ")"
                        f.close()
                    keyboard.row(row)
                    counter += 1
                bot.send_message(message.from_user.id, "Список карт", reply_markup=keyboard)

        elif message.text[:first] == "g":
            match = message.text[first + 1:sec]
            game = message.text[sec + 1:]
            if game.find("(") == -1:
                game_num  = int(re.search('[1-9]', game).group(0))
            else:
                game = game[:game.find("(")]
                game_num = int(re.search('[1-9]', game).group(0))
            lst = sorted(os.listdir("live/" + match + "/"))
            if lst[game_num - 1][-1] == "f":
                img = open("live/" + match + "/" + lst[game_num - 1] + "/result.png", "rb")
                bot.send_photo(message.from_user.id, img)
                img.close()
            elif lst[game_num - 1][-1] == "l":
                try:
                    f = open("live/" + match + "/" + lst[game_num - 1] + "/stat", "r")
                    stats = f.read()
                    bot.send_message(message.from_user.id, stats, disable_web_page_preview=True)
                    f.close()
                except FileNotFoundError:
                    bot.send_message(message.from_user.id, "Ошибка")
                except:
                    f.close()
                    bot.send_message(message.from_user.id, "Ошибка")

    elif "\n" in message.text and message.text.find("\n") != message.text.rfind("\n"):
        mes = message.text[message.text.find("\n") + 1:message.text.rfind("\n")]
        palka = mes.rfind("|")
        match = mes[:palka]
        game = mes[palka + 1:]
        game_num = int(re.search('[1-9]', game).group(0))
        lst = sorted(os.listdir("live/" + match + "/"))
        if lst[game_num - 1][-1] == "f":
            img = open("live/" + match + "/" + lst[game_num - 1] + "/result.png", "rb")
            bot.send_photo(message.from_user.id, img)
            img.close()
        elif lst[game_num - 1][-1] == "l":
            img = open("live/" + match + "/" + lst[game_num - 1] + "/pick.png", "rb")
            bot.send_photo(message.from_user.id, img)
            img.close()

    elif message.text == "Список текущих матчей" or message.text == "Обновить список":
        keyboard = telebot.types.ReplyKeyboardMarkup(True, False)
        keyboard.row("Главная")
        keyboard.row("Обновить список")
        for j in os.listdir("live/"):
            for i in os.listdir("live/" + j + "/"):
                if i[-1] == "l":
                    keyboard.row("g|" + j + "| Игра № " + str(len(os.listdir("live/" + j + "/"))))
                    break
        bot.send_message(message.from_user.id, "Список матчей", reply_markup=keyboard)
    elif message.text == "Недавние матчи":
        keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
        keyboard.row("Главная")
        for j in os.listdir("live/"):
            keyboard.row("m|" + j)
        bot.send_message(message.from_user.id, "Список матчей", reply_markup=keyboard)
    elif message.text == "Главная":
        keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
        keyboard.row("Список текущих матчей")
        keyboard.row("Недавние матчи")
        bot.send_message(message.from_user.id, "Добро пожаловать!", reply_markup=keyboard)
    else: pass


if __name__ == '__main__':
    while True:
        try:
            bot.polling(none_stop=True, interval=0)
        except Exception as e:
            print(e)
            pass
