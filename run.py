from components import ConsoleBot, AutoBot
import json 

with open("config.json") as f: 
    cfg = json.load(f)

    bot = AutoBot(key = cfg["key"], ip = cfg["ip"])
    bot.run() 


    f.close()
