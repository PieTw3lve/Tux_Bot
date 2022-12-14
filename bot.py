import os
import json
import io

import hikari
import lightbulb
import miru

import sqlite3

import startup

TOKEN = startup.TOKEN
DEFAULT_GUILD_ID = startup.DEFAULT_GUILD_ID

bot = lightbulb.BotApp(
    token=TOKEN,
    default_enabled_guilds=DEFAULT_GUILD_ID,
    prefix='!',
    intents=hikari.Intents.ALL
)   

@bot.listen()
async def on_ready(event: hikari.StartedEvent) -> None:
    db = sqlite3.connect('database.sqlite')
    cursor = db.cursor() # checks if db exists
    cursor.execute('''CREATE TABLE IF NOT EXISTS database (
        user_id INTEGER, 
        balance INTEGER,
        total INTEGER,
        loss INTEGER,
        tpass INTEGER,
        chicken TEXT,
        chicken_date TEXT,
        chicken_health INTEGER,
        chicken_strength INTEGER,
        chicken_defense INTEGER,
        chicken_hit_rate INTEGER,
        chicken_level INTEGER,
        chicken_experience INTEGER,
        chicken_items TEXT
    )''')
    
    if not os.path.isfile('settings.json') or not os.access('settings.json', os.R_OK): # checks if file exists
        print ("Either file is missing or is not readable, creating file...")
        
        dictionary = {
            'rushsite_signup_accessible': False,
            'rushsite_signup_channel': '1054971242924478504',
            'auto_translate': False,
            'command_cooldown': 5,
            'embed_color': '#249EDB',
            'embed_important_color': 'b03f58',
            'embed_success_color': '#32CD32',
            'embed_error_color': '#FF0000',
        }
        
        with io.open(os.path.join('', 'settings.json'), 'w') as openfile:
            openfile.write(json.dumps(dictionary, indent=4))
 
@bot.listen(hikari.MessageCreateEvent) # Register user to database
async def on_message(event: hikari.MessageCreateEvent):
    if event.is_bot or not event.content: # if bot sent the message
        return
    
    user = event.author
    
    db = sqlite3.connect('database.sqlite')
    cursor = db.cursor()
    
    if verify_user(user) == None: # if user has never been register
        sql = ('INSERT INTO database(user_id, balance, total, loss, tpass, chicken, chicken_date, chicken_health, chicken_strength, chicken_defense, chicken_hit_rate, chicken_level, chicken_experience, chicken_items) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)')
        val = (user.id, 100, 100, 0, 0, 'N/A', 'N/A', 0, 0, 0, 0, 0, 0, 'None')
        cursor.execute(sql, val) 
    
    db.commit() # saves changes
    cursor.close()
    db.close()

## Functions ##

def get_setting(option: str):
    with open('settings.json', 'r') as openfile:
        settings = dict(json.load(openfile))
        
        return settings[option]

def write_setting(option: str, value):
    with open("settings.json", "r") as openfile:
        data = json.load(openfile)

    data[option] = value

    with open("settings.json", "w") as openfile:
        json.dump(data, openfile, indent=4)

def verify_user(user: hikari.User):
    db = sqlite3.connect('database.sqlite')
    cursor = db.cursor()
    
    cursor.execute(f'SELECT user_id FROM database WHERE user_id = {user.id}') # moves cursor to user's id from database
    result = cursor.fetchone() # grabs the value of user's id
    
    return result

## Script ##

if __name__ == '__main__':
    if os.name != 'nt':
        import uvloop
        uvloop.install()
    miru.install(bot)
    bot.load_extensions_from('./extentions')
    bot.run(
        status=hikari.Status.DO_NOT_DISTURB, 
        activity=hikari.Activity(name='Type /info for help!', type=hikari.ActivityType.STREAMING, url='https://www.twitch.tv/ryqb')
    )