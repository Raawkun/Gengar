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
        level = 0
        atk = 0
        def = 0
        hp = 0
        spatk = 0
        spdef = 0
        speed = 0
        image = embed.image.url()
        dex = self.db.execute(f"SELECT * FROM Dex Where Img_url = {image}")
        dex = dex.fetchone()
        baseatk = dex[5]
        basedef=dex[6]
        basehp=dex[4]
        basespatk=dex[7]
        basespdef=dex[8]
        basespeed=dex[9]


def setup(client):
    client.add_cog(Modules(client))