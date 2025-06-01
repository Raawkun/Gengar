import disnake
from disnake.ext import commands
from sqlite3 import connect
from datetime import datetime
from utility.rarity_db import poke_rarity, embed_color
from utility.egglist import eggexcl
import re
import asyncio
from zoneinfo import ZoneInfo

class Rare_spawns(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.db = connect("database.db")

    current_time = datetime.utcnow()
    timestamp = current_time.strftime('%Y-%m-%d %H:%M:%S')
    Rare_Spawned = ["Event", "Legendary", "Shiny", "Golden"]

    async def egg_spawn(self, message, data):
        est = ZoneInfo("America/New_York")
        now = datetime.now(est)
        date = str(f"{now.day}.{now.month}.{now.year}")
        self.db.execute(f"UPDATE DailyStats SET Eggs = Eggs + 1 WHERE Date = '{date}'")
        self.db.commit()
        if message.reference:
            ref_msg = await message.channel.fetch_message(message.reference.message_id)
            sender = ref_msg.author
        elif message.interaction:
            ref_msg = message.interaction.author
            sender = ref_msg
        _embed = message.embed[0]
        receiver_channel = self.db.execute(f'SELECT * FROM Admin WHERE Server_ID = {message.guild.id}')
        receiver_channel = receiver_channel.fetchone()
        if receiver_channel > 0:
            receiver_channel = self.client.get_channel(int(receiver_channel))
        try:
            raremon = poke_rarity[(data[14])]
        except Exception as e:
            print(f"Egg Error: {message.channel.name}\n{message.author.display_name} - {message.jump_url}\n{e}")
        description_text = f"Original message: [Click here]({message.jump_url})\n"
        color = embed_color[data[14]]
        #print(Rare_Spawned)
        #Rare_Spawned = ["Golden","Event", "Legendary", "Shiny", "Rare", "SuperRare"]
        if data[14] in self.Rare_Spawned or str(data[0]) in eggexcl:
            print("Its in the one list!")
            print(str(data[0]))
            embed = disnake.Embed(title=raremon+" **"+data[1]+"** \nDex: #"+str(data[0]), color=color,description=description_text)
            embed.set_author(name=(sender.display_name+" just hatched an exclusive:"),icon_url="https://cdn.discordapp.com/emojis/689325070015135745.gif?size=96&quality=lossless")
            embed.set_image(_embed.image.url)
            embed.set_footer(text=(f'{self.client.user.display_name}'+" | at UTC "f'{self.timestamp}'), icon_url=f'{self.client.user.avatar}')
            await receiver_channel.send(embed=embed)
            emoji = '🔔'
            await message.add_reaction(emoji)
            return

    async def one_egg(self, message):
        try:
            mons = message.content.split("*just hatched a *")[1]
            print(mons)
            mons = mons.split("**")[1]
            print(mons)
            data = self.db.execute(f"SELECT * FROM Dex WHERE Name = '{mons}'")
            data = data.fetchone()
            if data[14] in self.Rare_Spawned or str(data[0]) in eggexcl:
                asyncio.create_task(Rare_spawns.egg_spawn(self, message, data))
        except Exception as e:
            print(f"{message.jump_url} - \n{e}")

    async def multi_egg(self, message):
        try:
            mons = message.content.split("*You have *")[0]
            print(mons)
            mons = mons.split("- ")
            print(mons)
            mons = mons[1:]
            print(mons)
            for entry in mons:
                matches = re.findall(r"\*\*(.+?)\*\*", entry)
                print(matches)
                data = self.db.execute(f"SELECT * FROM Dex WHERE Name = '{matches}'")
                data = data.fetchone()
                if data[14] in self.Rare_Spawned or str(data[0]) in eggexcl:
                    asyncio.create_task(Rare_spawns.egg_spawn(self, message, data))
        except Exception as e:
            print(f"{message.jump_url} - \n{e}")


    async def poke_spawn(self, message,data):
        receiver_channel = self.db.execute(f'SELECT * FROM Admin WHERE Server_ID = {message.guild.id}')
        receiver_channel = receiver_channel.fetchone()
        receiver_channel = int(receiver_channel[4])
        if receiver_channel > 0:
            receiver_channel = self.client.get_channel(int(receiver_channel))
        if message.reference:
            ref_msg = await message.channel.fetch_message(message.reference.message_id)
            sender = ref_msg.author
        elif message.interaction:
            ref_msg = message.interaction.author
            sender = ref_msg
        _embed = message.embeds[0]
        color = _embed.color
        description_text = " "
        if "caught a" in _embed.description:
            #print(f"Something got caught; {data[1]}")
            if "retrieved a" in _embed.description:
                #Rare_Spawns = ["Event", "Legendary", "Shiny", "Rare","Common", "Uncommon", "SuperRare","Golden"]
                item = _embed.description.split("retrieved")[1]
                item = item.split("**")[1]
                #print(item)
                description_text = f"<:held_item:1213754494266122280> **It held onto a {item}**.\n"
            if "token" in _embed.footer.text:
                author = sender.display_name+" just reeled in a:"
            else:
                author = sender.display_name+" just caught a:"
        

        if "broke out" in _embed.description:
            #print(f"Something broke out; {data[1]}")
            author = sender.display_name+" almost caught a:"
             
        if "ran away" in _embed.description:
            #print(f"Something ran away; {data[1]}")
            author = sender.display_name+" was too slow for:"
        raremon = poke_rarity[(data[14])]
        description_text += f"Original message: [Click here]({message.jump_url})\n"
        embed = disnake.Embed(title=raremon+" **"+data[1]+"** \nDex: #"+str(data[0]), color=color,description=description_text)
        embed.set_author(name=author, icon_url=_embed.author.icon_url)
        embed.set_image(_embed.image.url)
        embed.set_footer(text=(f'{self.client.user.display_name}'+" | at UTC "f'{self.timestamp}'), icon_url=f'{self.client.user.avatar}')
        await receiver_channel.send(embed=embed)
        emoji = '🔔'
        await message.add_reaction(emoji)
        return

    async def explore_spawn(self, message,data):
        receiver_channel = self.db.execute(f'SELECT * FROM Admin WHERE Server_ID = {message.guild.id}')
        receiver_channel = receiver_channel.fetchone()
        receiver_channel = int(receiver_channel[4])
        if receiver_channel > 0:
            receiver_channel = self.client.get_channel(int(receiver_channel))
        if message.reference:
            ref_msg = await message.channel.fetch_message(message.reference.message_id)
            sender = ref_msg.author
        elif message.interaction:
            ref_msg = message.interaction.author
            sender = ref_msg

        if "just caught a " in message.content:
            if receiver_channel > 0:
                raremon = poke_rarity[(data[14])]
                description_text = f"Original message: [Click here]({message.jump_url})\n"
                embed = disnake.Embed(title=raremon+" **"+data[1]+"** \nDex: #"+str(data[0]), color=embed_color[data[14]],description=description_text)
                embed.set_author(name=(f'{sender}'+" just discovered a:"), icon_url="https://cdn.discordapp.com/emojis/1072075141489623040.webp?size=96&quality=lossless")
                embed.set_image(data[15])
                embed.set_footer(text=(f'{self.client.user.display_name}'+" | at UTC "f'{self.timestamp}'), icon_url=f'{self.client.user.avatar}')
                anno = await receiver_channel.send(embed=embed)
                
        elif "broke out" in message.content:
            if receiver_channel > 0:
                raremon = poke_rarity[(data[14])]
                description_text = f"Original message: [Click here]({message.jump_url})\n"
                embed = disnake.Embed(title=raremon+" **"+data[1]+"** \nDex: #"+str(data[0]), color=embed_color[data[14]],description=description_text)
                embed.set_author(name=(f'{sender}'+" almost caught a:"), icon_url="https://cdn.discordapp.com/emojis/1072075141489623040.webp?size=96&quality=lossless")
                embed.set_image(data[15])
                embed.set_footer(text=(f'{self.client.user.display_name}'+" | at UTC "f'{self.timestamp}'), icon_url=f'{self.client.user.avatar}')
                anno = await receiver_channel.send(embed=embed)
                
        elif "ran away" in message.content:
            if receiver_channel > 0:
                raremon = poke_rarity[(data[14])]
                description_text = f"Original message: [Click here]({message.jump_url})\n"
                embed = disnake.Embed(title=raremon+" **"+data[1]+"** \nDex: #"+str(data[0]), color=embed_color[data[14]],description=description_text)
                embed.set_author(name=(sender+" was too slow for:"), icon_url="https://cdn.discordapp.com/emojis/1072075141489623040.webp?size=96&quality=lossless")
                embed.set_image(data[15])
                embed.set_footer(text=(f'{self.client.user.display_name}'+" | at UTC "f'{self.timestamp}'), icon_url=f'{self.client.user.avatar}')
                anno = await receiver_channel.send(embed=embed)

    async def icon_spawn(self, message):
        pass

    async def wb_spawn(self, message):
        #print("Checking the WB message")
        receiver_channel = self.db.execute(f'SELECT * FROM Admin WHERE Server_ID = {message.guild.id}')
        receiver_channel = receiver_channel.fetchone()
        receiver_channel = int(receiver_channel[4])
        if receiver_channel > 0:
            announce = self.client.get_channel(int(receiver_channel))
        if message.reference:
            ref_msg = await message.channel.fetch_message(message.reference.message_id)
            sender = ref_msg.author
        elif message.interaction:
            ref_msg = message.interaction.author
            sender = ref_msg
        id = message.content.split("You obtained a <:")[1]
        id = int(id.split(":")[0])
        data = self.db.execute(f"SELECT * FROM Dex WHERE DexID = {id}")
        data = data.fetchone()
        if (data[14] == "shinygigantamax") or (data[14] == "shiny"):
            color = disnake.Color.fuchsia()
        else:
            color = disnake.Color.red()
        author_icon = "https://cdn.discordapp.com/emojis/1372953699852357665.webp?"
        raremon = poke_rarity[(data[14])]
        description_text = f"Original message: [Click here]({message.jump_url})\n"
        embed = disnake.Embed(title=raremon+" **"+data[1]+"** \nDex: #"+str(data[0]), color=color,description=description_text)
        embed.set_author(name=f"{sender.display_name} got this from a World Boss:", icon_url=author_icon)
        embed.set_image(data[15])
        embed.set_footer(text=(f'{self.client.user.display_name}'+" | at UTC "f'{self.timestamp}'), icon_url=f'{self.client.user.avatar}')
        await announce.send(embed=embed)
        emoji = '🔔'
        await message.add_reaction(emoji)
        return

    async def gold_spawn(self, message):
        pass

    async def box_spawn(self, message):
        pass


def setup(client):
    client.add_cog(Rare_spawns(client))