import disnake
from disnake.ext import commands
import math, sqlite3
from sqlite3 import connect

class Methods(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.db = connect("database.db")

    async def iv_check(self, message):
        embed = message.embeds[0]
        level = int(embed.description.split("**Level**: ")[1].split("\n")[0])
        for entry in embed.fields:
            if "**Pokémon EVs** " in entry.name:
                evs = entry.value
                evatk= int(evs[:-6].split("`ATK` ")[1])
                evdef=int(evs[:-6].split("`DEF` ")[1])
                evhp=int(evs[:-6].split("`HP` ")[1])
                evspatk=int(evs[:-6].split("`SPA` ")[1])
                evspdef=int(evs[:-6].split("`SPD` ")[1])
                evspeed=int(evs[:-6].split("`SPE` ")[1])
            if "**Pokémon Stats**" in entry.name:
                stats = entry.value
                atk = int(stats.split("`Atk` : ")[1].split("\n")[0])
                defe = int(stats.split("`Def` : ")[1].split("\n")[0])
                hp = int(stats.split("`HP`\u200b: ")[1])
            if "\u200b" in entry.name:
                stats = entry.value
                spatk = int(stats.split("`Sp.Atk` : ")[1].split("\n")[0])
                spdef = int(stats.split("`Sp.Def` : ")[1].split("\n")[0])
                speed = int(stats.split("`Speed`\u200b: ")[1])
        image = embed.image.url
        dex = self.db.execute(f"SELECT * FROM Dex Where Img_url = {image}")
        dex = dex.fetchone()
        baseatk = dex[5]
        basedef=dex[6]
        basehp=dex[4]
        basespatk=dex[7]
        basespdef=dex[8]
        basespeed=dex[9]
        if message.reference.author_id == 352224989367369729:
            await message.reply(f"Level:{level}\nBase Stats:{baseatk}/{basedef}/{basehp}/{basespatk}/{basespdef}/{basespeed}\nEVs:{evatk}/{evdef}/{evhp}/{evspatk}/{evspdef}/{evspeed}\nStats:{atk}/{defe}/{hp}/{spatk}/{spdef}/{speed}")




def setup(client):
    client.add_cog(Methods(client))