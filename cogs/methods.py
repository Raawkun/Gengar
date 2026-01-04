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
        for entry in embed.Fields:
            if "**Pokémon EVs** " in entry.name:
                evs = entry.value()
                evatk= int(evs.split("`ATK` ")[1].split("`")[0])
                evdef=int(evs.split("`DEF` ")[1].split("`")[0])
                evhp=int(evs.split("`HP` ")[1].split("`")[0])
                evspatk=int(evs.split("`SPA` ")[1].split("`")[0])
                evspdef=int(evs.split("`SPD` ")[1].split("`")[0])
                evspeed=int(evs.split("`SPE` ")[1].split("`")[0])
            if "**Pokémon Stats**" in entry.name:
                stats = entry.value()
                atk = int(stats.split("`Atk` : ")[1].split("`")[0])
                defe = int(stats.split("`Def` : ")[1].split("`")[0])
                hp = int(stats.split("`HP`\u200b: ")[1].split("`")[0])
            if "\u200b" in entry.name:
                stats = entry.value()
                spatk = int(stats.split("`Sp.Atk` : ")[1].split("`")[0])
                spdef = int(stats.split("`Sp.Def` : ")[1].split("`")[0])
                speed = int(stats.split("`Speed`\u200b: ")[1])
        image = embed.image.url()
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