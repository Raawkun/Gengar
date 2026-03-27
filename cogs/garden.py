import disnake
from disnake.ext import commands
from sqlite3 import connect
from datetime import datetime, timedelta
import asyncio
from utility.info_dict import rem_emotes, emote_list, embed_color

class Garden(commands.Cog):

    def __init__(self,client):
        self.client = client
        self.db = connect("database.db")

    async def garden_check(userid, slot, timestamp):
        check = self.db.execute(f"SELECT * FROM Garden WHERE User_ID = {userid}")
        check = check.fetchall()
        if check is not None:
            for entry in check:
                if slot == entry[1]:
                    if timestamp == entry[2]:
                        return
                    else:
                        pass
                        
                        
    async def user_check(userid, message):
        check = self.db.execute(f"SELECT Garden, Emotes, Ping FROM Toggles WHERE User_ID = {userid}")
        check = check.fetchone()
        if (check == None) or (check[0] == 0):
            return
        else:
            emb = message.embeds[0]
            pots = emb.description.split("Slot ")
            for entry in pots:
                if "Next stage" in entry:
                    number = entry.split("**")[0]
                    stamp = entry.split("<t:")[1].split(":R>")[0]
                else:
                    continue
            #msg = await asyncio.create_task(Garden.garden_check(

def setup(client):
    client.add_cog(Garden(client))