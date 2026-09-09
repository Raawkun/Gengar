import disnake, asyncio
from disnake.ext import commands
import sqlite3, math
from sqlite3 import connect


class Catchlist(commands.Cog):


    def __init__(self, client):
        self.client = client
        self.db = connect("database.db")
    
    async def update_catchlist(self, message):
        pass
        
    astnc def check_catchlist(self, message, method):
        emb = message.embeds[0]
        data = self.db.execute(f"SELECT DexID, Name FROM Dex WHERE Image_url = '{emb.image.url}')
        data = data.fetchone()
        print(data[1])
    



def setup(client):
    client.add_cog(Catchlist(client))