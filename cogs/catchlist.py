import disnake, asyncio
from disnake.ext import commands
import sqlite3, math
from sqlite3 import connect


class Catchlist(commands.Cog):


    def __init__(self, client):
        self.client = client
        self.db = connect("database.db")
    
    async def catchlist_update(self, message):
        pass
        
    astnc def catchlist_check(self, message):
        pass
    



def setup(client):
    client.add_cog(Catchlist(client))