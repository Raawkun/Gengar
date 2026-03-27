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
                

def setup(client):
    client.add_cog(Garden(client))