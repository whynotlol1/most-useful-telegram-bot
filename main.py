import telebot
import sqlite3
import random
import time

bot = telebot.TeleBot(token='idi nahuy')

conn = sqlite3.connect('most_useful.db', check_same_thread=False)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER,
    lolis BIGINT,
    last_time_command_used INTEGER
)
""")
conn.commit()

with open("loli_gifs.txt", "r") as f:
    gifs = [el[:-1] for el in f.readlines()]


def epic_random():
    out_of_bounds_chance = 0.2
    if random.random() <= out_of_bounds_chance:
        num = random.randint(-10, 15)
    else:
        num = random.randint(-5, 7)
    if num == 0:
        return 1
    else:
        return num


@bot.message_handler(commands=['help', 'start'])
def send_help(message):
    bot.send_message(message.chat.id, "Welcome to the loli bot! Here's the list of commands:\n\n/loli - get new lolis (every 12 hours)\n\n/my_lolis - see how many lolis you have\n\n/top - see the top 10 users with most lolis\n\nIdea by: Valpik; Bot by: cat dev")


@bot.message_handler(commands=['loli'])
def loli_giver(message):
    now = int(time.time())
    amount_delta = epic_random()
    check = cur.execute("SELECT * FROM users WHERE user=?", (message.from_user.id,)).fetchone()
    if check is None:
        old_amount = 0
        time_delta = 43200
        cur.execute("INSERT INTO users VALUES (?,?,?)", (message.from_user.id, 0, int(time.time())))
    else:
        time_delta = now - check[2]
        old_amount = check[1]
    if time_delta >= 43200:
        cur.execute("UPDATE users SET lolis=? WHERE user=?", (int(old_amount + amount_delta), message.from_user.id))
        conn.commit()
        bot.send_message(message.chat.id, f'{message.from_user.username}, you got {amount_delta} new lolis!')
    else:
        bot.send_message(message.chat.id, f"{message.from_user.username}, you can't get new lolis yet!")
    bot.send_message(message.chat.id, random.choice(gifs))


@bot.message_handler(commands=['my_lolis'])
def loli_viewer(message):
    check = cur.execute("SELECT * FROM users WHERE user=?", (message.from_user.id,)).fetchone()
    if check is None:
        amount = 0
        cur.execute("INSERT INTO users VALUES (?,?,?)", (message.from_user.id, 0, 0))
    else:
        amount = check[1]
    bot.send_message(message.chat.id, f"{message.from_user.username}, you've got {amount} lolis!")


@bot.message_handler(commands=['top'])
def top_loli_people(message):
    top = cur.execute("SELECT * FROM users ORDER BY lolis DESC").fetchall()
    message_string = 'Top 10 users with most lolis:\n'
    if len(top) <= 10:
        lim = len(top)
    else:
        lim = 10
    for i in range(lim):
        message_string += f'\n{top[i][0]}: {top[i][1]} lolis\n'
    bot.send_message(message.chat.id, message_string)


bot.polling(none_stop=True)
