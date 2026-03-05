import asyncio
import datetime
import disnake
from disnake.ext import commands
import sqlite3
from sqlite3 import connect
from cogs.module import Modules
from utility.rarity_db import poke_rarity, embed_color
from utility.embed import Custom_embed
from utility.drop_chance import drop_pos, rare_calc, ball_used_low, ball_used_high
from utility.id_lists import safari_id
from cogs.safari_event import SafariEvent
import random
from utility.all_checks import Basic_checker
from cogs.listener import Listener
from cogs.rare_spawns import Rare_spawns
from utility.johto.travel_checks import TravelChecks
from utility.johto.johto_checks import ChecksOfJohto
from utility.johto.johto_quests import QuestsOfJohto

class On_Edit(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.db = connect("database.db")

    current_time = datetime.datetime.utcnow()
    timestamp = current_time.strftime('%Y-%m-%d %H:%M:%S')
    Rare_Spawns = ["Event", "Legendary", "Shiny","Golden"]

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        
        # 825950637958234133
        receiver_channel = self.db.execute(f'SELECT * FROM Admin WHERE Server_ID = {before.guild.id}')
        receiver_channel = receiver_channel.fetchone()
        #print(receiver_channel)
        receiver_channel = int(receiver_channel[4])
        current_time = datetime.datetime.utcnow()
        locations = await TravelChecks.travel_locations()
        ticket_check = await TravelChecks.johto_tickets()
        timestamp = current_time.strftime('%Y-%m-%d %H:%M:%S')
        if receiver_channel > 0:
            announce = self.client.get_channel(int(receiver_channel))
        log = self.client.get_channel(1210143608355823647)
        
        if before.author.id == 664508672713424926:  #Meow
            if before.pinned != after.pinned:
                return
            if before.pinned == after.pinned:
                ##### Rare Spawn #####
                #Rare_Spawns = ["Event", "Legendary", "Shiny", "Rare", "SuperRare","Golden"]
                if (len(before.embeds) > 0):
                    #print("Edit with Embed")
                    befembed = before.embeds[0]
                    if "may continue playing" in after.content.lower():
                        emoji = "<a:GengarClapping:1378680505775558708>"
                        await after.add_reaction(emoji)
                        return
                    
                    if (len(after.embeds) > 0):
                        _embed = after.embeds[0]
                        color = _embed.color
                        #print("After embed")
                    else:
                        return
                    if _embed.description:
                        if "fished out a" in _embed.description:
                            #print("Fishyyyy")
                            try:
                                data = self.db.execute(f'SELECT * FROM Dex WHERE Img_url = "{_embed.image.url}"')
                                data = data.fetchone()
                            except:
                                try:
                                    name = _embed.description.split("**")[3]
                                    data = self.db.execute(f'SELECT * FROM Dex WHERE Name = "{name}"')
                                    data = data.fetchone()
                                except:
                                    await before.channel.send("It seems this Pokémon is not in my database - could you please add it with checking its ``/pokedex entry``?")
                                    return
                            if data[11] == 1:
                                await before.channel.send("Watch out! This one is a <:shin:1165314036909494344> Pokémon!")
                            elif data[12]:
                                await before.channel.send("Watch out! This one is a <:gold:1165319370801692786> Pokémon!")
                    if _embed.footer.text:
                        if "pokemon roll" in _embed.footer.text.lower():
                            #print("There's been a roll")
                            try:
                                data = self.db.execute(f'SELECT * FROM Dex WHERE Img_url = "{_embed.image.url}"')
                                data = data.fetchone()
                                raremon = data[14]
                                #print(f"{data[1]} - {data[14]}")
                            except:
                                try:
                                    name = _embed.description.split("**")[1]
                                    data = self.db.execute(f'SELECT * FROM Dex WHERE Name = "{name}"')
                                    data = data.fetchone()
                                    raremon = data[14]
                                except:
                                    await before.channel.send("It seems this Pokémon is not in my database - could you please add it with checking its ``/pokedex entry``?")
                                    return
                            if before.reference:
                                ref_msg = await before.channel.fetch_message(before.reference.message_id)
                                sender = ref_msg.author
                            elif before.interaction_metadata:
                                ref_msg = before.interaction_metadata.user
                                sender = ref_msg
                            if "caught a" in _embed.description:
                                if "pokecoins" in _embed.footer.text.lower():
                                    asyncio.create_task(Modules.dailycheck(self,after))
                                    asyncio.create_task(Modules.averagecoins(self,after))
                                    if after.channel.id in locations["Goldenrod City"]:
                                        await QuestsOfJohto.goldenrod_quest(self, sender, after)
                                    coin_type = "hunt"
                                else:
                                    coin_type = "fish"
                                if data[0] == 129:
                                    asyncio.create_task(Modules.fisheventcheck(self, after,sender))
                                types =(data[2], data[3])
                                ev = self.db.execute(f"SELECT Additional FROM Events WHERE Name = 'TypeHunt'")
                                ev = ev.fetchone()
                                if ev[0] in types:
                                    #print(f"{data[2]} {data[3]}")
                                    asyncio.create_task(Modules.eventchecker(self, after,sender))
                                if "_fossil" in _embed.description:
                                    fossil = _embed.description.split("retrieved a <:")[1]
                                    fossil = fossil.split(":")[0]
                                    await after.reply(f"``;res ex {fossil}``")
                                if after.channel.id in locations["New Bark Town"]:
                                    #print(data[16])
                                    await QuestsOfJohto.newbark_quest(self, data[15],sender,before)
                                elif after.channel.id in locations["Cherrygrove City"]:
                                    await QuestsOfJohto.cherrygrove_quest(self, sender, before)
                                elif after.channel.id in locations["Violet City"]:
                                    await QuestsOfJohto.violet_quest(self, data[15], sender, before)
                                elif after.channel.id in locations["Azalea Town"]:
                                    await QuestsOfJohto.azalea_quest(self, data[15], sender, before)
                                    await QuestsOfJohto.secret_quest_1(self, data[15], sender, before)
                                elif after.channel.id in locations["Ecruteak City"]:
                                    await QuestsOfJohto.ecruteak_quest(self, data[15], sender, before)
                                elif after.channel.id in locations["Olivine City"]:
                                    await QuestsOfJohto.olivine_quest(self, data[15], sender, before)
                                elif after.channel.id in locations["Cianwood City"]:
                                    await QuestsOfJohto.cianwood_quest(self, data[15],sender,before)
                                elif after.channel.id in locations["Mahogany Town"]:
                                    await QuestsOfJohto.mahogany_quest(self, data[15],sender,before)
                                for location in locations.values():
                                    if after.channel.id in location:
                                        await QuestsOfJohto.johto_coins(self, sender, before, coin_type)
                                        await QuestsOfJohto.secret_quest_2(self, data[15], sender, before)
                                if "retrieved a" in _embed.description:
                                    if after.channel.id in locations["Blackthorn City"]:
                                        await QuestsOfJohto.blackthorn_quest(self, sender,before)
                            if raremon in self.Rare_Spawns or data[0] in Listener.exclusives or _embed.color.contains('ea260b'):
                                print(f"Theres a rare spawn: {data[0]} {data[1]}")
                            
                                asyncio.create_task(Rare_spawns.poke_spawn(self, after, data))

            if ":map: Map:" in before.content:
                if "steps today:" in after.content.lower():
                    #print("Someone is stepping.")
                    if "found a " in before.content:
                        if before.reference:
                            ref_msg = await before.channel.fetch_message(before.reference.message_id)
                            sender = ref_msg.author
                        else:
                            sender = "A User"
                        #print("Theres a pokemon")
                        asyncio.create_task(Modules.dailycheck(self,before))
                        # monrare = before.content.split("found a ")[1]
                        # monname = monrare.split("**")[1]
                        # monnumber = monrare.split(":")[3]
                        # monrare = monrare.split(":")[1]
                        #print(f'{monnumber}'", "f'{monrare}'", "f'{monname}')
                        if "caught a " in after.content:
                            asyncio.create_task(Modules.dailycheck(self, after))
                            mon = after.content.split("just caught")[1]
                            mon = mon.split("!")[0]
                            mon = mon.split("**")[1]
                            data = self.db.execute(f"SELECT * FROM Dex WHERE Name = '{mon}'")
                            data = data.fetchone()
                            #print("Calculate catch")
                            if data[14] in self.Rare_Spawns:
                        #Rare_Spawns = ["Event", "Legendary", "Shiny", "Rare", "SuperRare","Golden","Uncommon"]
                                asyncio.create_task(Rare_spawns.explore_spawn(self, after, data))
                                    



def setup(client):
    client.add_cog(On_Edit(client))