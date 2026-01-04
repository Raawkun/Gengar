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
        #Get Stats from Embed
        level = int(embed.description.split("**Level**: ")[1].split("\n")[0])
        for entry in embed.fields:
            if "**Pokémon EVs** " in entry.name:
                evs = entry.value
                evatk= evs.split("`ATK` ")[1].split("`")[0]
                evatk=int(evatk[:-1])
                evdef=evs.split("`DEF` ")[1].split("`")[0]
                evdef=int(evdef[:-1])
                evhp=evs.split("`HP` ")[1].split("`")[0]
                evhp=int(evhp[:-1])
                evspatk=evs.split("`SPA` ")[1].split("`")[0]
                evspatk=int(evspatk[:-1])
                evspdef=evs.split("`SPD` ")[1].split("`")[0]
                evspdef=int(evspdef[:-1])
                evspeed=evs.split("`SPE` ")[1]
                evspeed=int(evspeed[:-1])
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
        dex = self.db.execute(f"SELECT * FROM Dex WHERE Img_url = '{image}'")
        dex = dex.fetchone()
        baseatk = dex[5]
        basedef=dex[6]
        basehp=dex[4]
        basespatk=dex[7]
        basespdef=dex[8]
        basespeed=dex[9]
        ref_msg = await message.channel.fetch_message(message.reference.message_id)
        if ref_msg.author.id == 352224989367369729:
            await message.channel.send(f"Level:{level}\nBase Stats:{baseatk}/{basedef}/{basehp}/{basespatk}/{basespdef}/{basespeed}\nEVs:{evatk}/{evdef}/{evhp}/{evspatk}/{evspdef}/{evspeed}\nStats:{atk}/{defe}/{hp}/{spatk}/{spdef}/{speed}")

        #Start calculation
        IV_ATK = Methods.possible_ivs(baseatk, level,atk,evatk)
        IV_DEF = Methods.possible_ivs(basedef, level,defe,evdef)
        IV_HP = Methods.possible_ivs(basehp, level,hp,evhp)
        IV_SPATK = Methods.possible_ivs(basespatk, level,spatk,evspatk)
        IV_SPDEF = Methods.possible_ivs(basespdef, level,spdef,evspdef)
        IV_SPEED = Methods.possible_ivs(basespeed, level,speed,evspeed)

        desc = f"Possible IVs for **{dex[1]}**:\nATK: {IV_ATK}\nDEF: {IV_DEF}\nHP: {IV_HP}\nSpeed: {IV_SPEED}"
        await message.channel.send(desc)
    def possible_ivs(base_stat: int, level: int, stat: int, ev: int):
        
        # Level-abhängiger EV-Term
        ev_term = (ev // 4) * level // 100

        x = stat - 5

        iv_min = math.ceil(
            (x * 100) / level - (2 * base_stat + ev_term)
        )

        iv_max = math.floor(
            ((x + 1) * 100 - 1) / level - (2 * base_stat + ev_term)
        )

        # IV-Bereich erzwingen
        iv_min = max(0, iv_min)
        print(iv_min)
        iv_max = min(15, iv_max)
        print(iv_max)

        if iv_min > iv_max:
            return []

        return list(range(iv_min, iv_max + 1))


def setup(client):
    client.add_cog(Methods(client))