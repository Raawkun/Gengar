import disnake, asyncio
from disnake.ext import commands
import sqlite3, math
from sqlite3 import connect


class Catchlist(commands.Cog):


    def __init__(self, client):
        self.client = client
        self.db = connect("database.db")
    
    async def update_catchlist(self, message):
        emb = message.embeds[0]
        data = ""
        for entry in emb.fields:
            if "u200b" in entry.name:
                if " from " in entry.value:
                    method = entry.value.split("`")[1]
                    mon_id = int(entry.value.split(":")[1])
                    ball = entry.value.split("**")[1]
                    self.db.execute(f"UPDATE or INSERT INTO Monthly_Catchlist VALUES ({mon_id}, '{ball}', '{method}')")
                    self.db.commit()
                    data = data+" "+mon_id
        print(data)
            
        
    async def check_catchlist(self, message, method):
        emb = message.embeds[0]
        data = self.db.execute(f"SELECT DexID, Name FROM Dex WHERE Img_url = '{emb.image.url}'")
        data = data.fetchone()
        print(data[1])
    



def setup(client):
    client.add_cog(Catchlist(client))