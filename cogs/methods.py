import disnake
from disnake.ext import commands
import math, sqlite3
from sqlite3 import connect

class Methods(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.db = connect("database.db")

    async def iv_calc(self, message):
        embed = message.embeds[0]
        level = 
        atk = 
        def = 
        hp = 
        spatk = 
        spdef = 
        speed = 
        image = embed.image.url()
        dex = 
        


def setup(client):
    client.add_cog(Modules(client))