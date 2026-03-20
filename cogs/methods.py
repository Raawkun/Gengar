import disnake
from disnake.ext import commands
import math, sqlite3
from sqlite3 import connect
from utility.embed import Custom_embed

class Methods(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.db = connect("database.db")

    async def iv_check(self, sender, message):
        sender = sender.id
        toggle = self.db.execute(f"SELECT IV FROM Toggle WHERE User_ID = {sender}")
        toggle = toggle.fetchone()
        if toggle[0] == 1:
            embed = message.embeds[0]
            name = embed.title.split("> ")
            #print(name)
            name = name[2]
            #Get Stats from Embed
            nature = embed.description.split("**Nature: ")[1].split(" ")[0]
            level = int(embed.description.split("**Level**: ")[1].split("\n")[0])
            for entry in embed.fields:
                if "**Pokémon EVs** " in entry.name:
                    evs = entry.value
                    print(evs)
                    evatk= evs.split("`ATK` **")[1].split("**")[0].replace(" ","")
                    print(evatk)
                    evatk=int(evatk)
                    evhp=evs.split("`HP` **")[1].split("**")[0].replace(" ","")
                    evhp=int(evhp)
                    evspatk=evs.split("`SPA` **")[1].split("**")[0].replace(" ","")
                    evspatk=int(evspatk)
                    
                if "**Pokémon Stats**" in entry.name:
                    stats = entry.value
                    atk = int(stats.split("`Atk` **")[1].split("**")[0])
                    if nature in ["Lonely", "Brave", "Adamant", "Naughty"]:
                        atk = int(atk*0.9)
                    elif nature in ["Bold", "Timid", "Modest", "Calm"]:
                        atk = int(atk*1.1)
                    spatk = int(stats.split("`SpA` **")[1].split("**")[0])
                    if nature in ["Modest", "Mild", "Quiet", "Rash"]:
                        spatk = int(spatk*0.9)
                    elif nature in ["Adamant", "Impish", "Jolly", "Careful"]:
                        spatk = int(spatk*1.1)
                    hp = int(stats.split("`HP` **")[1].split("**")[0])
                if "\u200b" in entry.name:
                    print(entry.value)
                    if "`DEF` **  " in entry.value:
                        evs=entry.value
                        evdef=evs.split("`DEF` **")[1].split("**")[0].replace(" ","")
                        evdef=int(evdef)
                        evspdef=evs.split("`SPD` **")[1].split("**")[0].replace(" ","")
                        evspdef=int(evspdef)
                        evspeed=evs.split("`SPE` **")[1].split("**")[0].replace(" ","")
                        evspeed=int(evspeed)
                    elif ":shield:" in entry.value:
                        stats = entry.value
                        print(stats)
                        defe = int(stats.split("`Def` **")[1].split("**")[0])
                        if nature in ["Bold", "Relaxed", "Impish", "Lax"]:
                            defe = int(defe*0.9)
                        elif nature in ["Lonely", "Hasty", "Mild", "Gentle"]:
                            defe = int(defe*1.1)
                        spdef = int(stats.split("`SpD` **")[1].split("**")[0])
                        if nature in ["Calm", "Gentle", "Sassy", "Careful"]:
                            spdef = int(spdef*0.9)
                        elif nature in ["Naughty", "Lax", "Naive", "Rash"]:
                            spdef = int(spdef*1.1)
                        speed = int(stats.split("`Spe` **")[1].split("**")[0])
                        if nature in ["Timid", "Hasty", "Jolly", "Naive"]:
                            speed = int(speed*0.9)
                        elif nature in ["Brave", "Relaxed", "Quiet", "Sassy"]:
                            speed = int(speed*1.1)
            image = embed.image.url
            try:
                dex = self.db.execute(f"SELECT * FROM Dex WHERE Img_url='{image}'")
                dex = dex.fetchall()
            except Exception as e:
                print(e)
                return
            if not dex:
                embed = await Custom_embed(
                    self.client, title = f"__Calculated IV's__", description = f"""This pokemon is not currently in the database.  Please use `/pokedex entry (mon name)` to add it."""
                ).setup_embed()
                await message.channel.send(embed=embed)
                return
            else:
                for row in dex:
                    b_atk = row[5]
                    b_def = row[6]
                    b_hp = row[4]
                    b_spe = row[9]
                    golden = row[12]
                    shiny = row[11]
                    dex_name = row[1]
                    pic = row[15]

                # print(f"hp_EV: {hp_ev} Level: {level} EV influence: {atk_ev * level / 400}")
                # print(hp)
                atk -= math.floor(evatk * level / 400)
                defe -= math.floor(evdef * level / 400)
                speed -= math.floor(evspeed * level / 400)
                # hp -= math.floor(hp_ev * level / 400)
                # print(hp)

                atk_iv = math.ceil(((atk - 5 - (2.7 * b_atk * (level/100))) * 100) / (level + 100))
                def_iv = math.ceil(((defe - 5 - (2.7 * b_def * (level/100))) * 100) / (level + 100))
                spe_iv = math.ceil(((speed - 5 - (2.7 * b_spe * (level/100))) * 100) / (level + 100))
                
                # hp_iv = math.ceil(((hp - (level / 3) - (2.7 * b_hp * (level / 100))) * 100) / (level + 200))

                # hp_iv = math.ceil(((hp - level - 10 - (2.7 * b_hp * (level / 100))) * 100) / (level + 100))

                # hp_iv = math.ceil((100 * (hp - level - 10) / level) - (2.7 * b_hp))
                hp_iv = None
                i = 0

                for iv in range(21):  # Loop through EV values from 0 to 20
                    hp_check = math.floor((((2.7 * b_hp) + iv + math.floor(evhp / 4)) * level / 100) + level + 10)
                    # print(f"Check{i} {hp_check} {iv}")
                    i += 1
                    if hp_check == hp:
                        hp_iv = iv
                        break
                else:
                    hp_iv = 0
                    # print("Couldn't find match")

                #print(f"{atk_iv}, {def_iv}, {spe_iv}, {hp_iv}")
                # print(atk_iv, def_iv, spd_iv)
                if golden:
                    progress = round(((atk_iv + def_iv + spe_iv + hp_iv) / 80 ) * 100 , 2)
                else:
                    progress = round(((atk_iv + def_iv + spe_iv + hp_iv) / 60 ) * 100 , 2)
                

                embed = await Custom_embed(
                    self.client, title = f"__Calculated IV's__", description = f"""Your IV progress is: **{progress}%**\n*Please note, this is not accurate for low levels*"""
                ).setup_embed()
                embed.set_author(name=f"{name}", icon_url=f"{pic}")
                embed.add_field(name="⠀", value=f'⚔ Atk: `{atk_iv}`\n🛡 Def: `{def_iv}`', inline=True)
                embed.add_field(name="⠀", value=f'💖 HP: `{hp_iv}`\n⚡ Spe: `{spe_iv}`', inline=True)
            await message.channel.send(embed=embed)
        else:
            return


def setup(client):
    client.add_cog(Methods(client))