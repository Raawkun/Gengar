import disnake
from disnake.ext import commands
from sqlite3 import connect
from datetime import datetime
from utility.rarity_db import poke_rarity, embed_color, chambers
from utility.egglist import eggexcl
import re
import asyncio
from zoneinfo import ZoneInfo
from cogs.module import Modules
from utility.embed import Custom_embed

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
        _embed = message.embeds[0]
        receiver_channel = self.db.execute(f'SELECT * FROM Admin WHERE Server_ID = {message.guild.id}')
        receiver_channel = receiver_channel.fetchone()
        if int(receiver_channel[4]) > 0:
            receiver_channel = self.client.get_channel(int(receiver_channel[4]))
        try:
            raremon = poke_rarity[(data[14])]
        except Exception as e:
            print(f"Egg Error: {message.channel.name}\n{message.author.display_name} - {message.jump_url}\n{e}")
        description_text = f"Original message: [Click here]({message.jump_url})\n"
        color = embed_color[data[14]]
        #print(Rare_Spawned)
        #Rare_Spawned = ["Golden","Event", "Legendary", "Shiny", "Rare", "SuperRare"]
        if data[14] in Rare_spawns.Rare_Spawned or str(data[0]) in eggexcl:
            print("Its in the one list!")
            print(str(data[0]))
            embed = disnake.Embed(title=raremon+" **"+data[1]+"** \nDex: #"+str(data[0]), color=color,description=description_text)
            embed.set_author(name=(sender.display_name+" just hatched an exclusive:"),icon_url="https://cdn.discordapp.com/emojis/689325070015135745.gif?size=96&quality=lossless")
            embed.set_image(data[15])
            embed.set_footer(text=(f'{self.client.user.display_name}'+" | at UTC "f'{Rare_spawns.timestamp}'), icon_url=f'{self.client.user.avatar}')
            await receiver_channel.send(embed=embed)
            emoji = '🔔'
            await message.add_reaction(emoji)
            return

    async def one_egg(self, message):
        try:
            #print(message.content)
            mons = message.content.split("** just hatched a ")[1]
            #print(mons)
            mons = mons.split("**")[1]
            #print(mons)
            data = self.db.execute(f"SELECT * FROM Dex WHERE Name = '{mons}'")
            data = data.fetchone()
            if data[14] in Rare_spawns.Rare_Spawned or str(data[0]) in eggexcl:
                asyncio.create_task(Rare_spawns.egg_spawn(self, message, data))
        except Exception as e:
            print(f"{message.jump_url} - \n{e}")

    async def multi_egg(self, message):
        try:
            mons = message.content.split("*You have ")[0]
            #print(mons)
            mons = mons.split("- ")
            #print(mons)
            mons = mons[1:]
            print(mons)
            for entry in mons:
                matches = re.findall(r"\*\*(.+?)\*\*", entry)
                print(matches)
                data = self.db.execute(f"SELECT * FROM Dex WHERE Name = '{matches[0]}'")
                data = data.fetchone()
                if data[14] in Rare_spawns.Rare_Spawned or str(data[0]) in eggexcl:
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
        embed.set_footer(text=(f'{self.client.user.display_name}'+" | at UTC "f'{Rare_spawns.timestamp}'), icon_url=f'{self.client.user.avatar}')
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
                embed.set_footer(text=(f'{self.client.user.display_name}'+" | at UTC "f'{Rare_spawns.timestamp}'), icon_url=f'{self.client.user.avatar}')
                anno = await receiver_channel.send(embed=embed)
                
        elif "broke out" in message.content:
            if receiver_channel > 0:
                raremon = poke_rarity[(data[14])]
                description_text = f"Original message: [Click here]({message.jump_url})\n"
                embed = disnake.Embed(title=raremon+" **"+data[1]+"** \nDex: #"+str(data[0]), color=embed_color[data[14]],description=description_text)
                embed.set_author(name=(f'{sender}'+" almost caught a:"), icon_url="https://cdn.discordapp.com/emojis/1072075141489623040.webp?size=96&quality=lossless")
                embed.set_image(data[15])
                embed.set_footer(text=(f'{self.client.user.display_name}'+" | at UTC "f'{Rare_spawns.timestamp}'), icon_url=f'{self.client.user.avatar}')
                anno = await receiver_channel.send(embed=embed)
                
        elif "ran away" in message.content:
            if receiver_channel > 0:
                raremon = poke_rarity[(data[14])]
                description_text = f"Original message: [Click here]({message.jump_url})\n"
                embed = disnake.Embed(title=raremon+" **"+data[1]+"** \nDex: #"+str(data[0]), color=embed_color[data[14]],description=description_text)
                embed.set_author(name=(sender+" was too slow for:"), icon_url="https://cdn.discordapp.com/emojis/1072075141489623040.webp?size=96&quality=lossless")
                embed.set_image(data[15])
                embed.set_footer(text=(f'{self.client.user.display_name}'+" | at UTC "f'{Rare_spawns.timestamp}'), icon_url=f'{self.client.user.avatar}')
                anno = await receiver_channel.send(embed=embed)

    async def icon_spawn(self, message):
        log_channel = 1164544776985653319
        log_chn = self.client.get_channel(log_channel)
        receiver_channel = self.db.execute(f'SELECT * FROM Admin WHERE Server_ID = {message.guild.id}')
        receiver_channel = receiver_channel.fetchone()
        receiver_channel = int(receiver_channel[4])
        if receiver_channel > 0:
            receiver_channel = self.client.get_channel(int(receiver_channel))
        asyncio.create_task(Modules.dailycheck(self, message))
        iconname = message.content.split("unlocked ")[1]
        icon = iconname.split(":")[2]
        icon = icon.split(">")[0]
        iconname = iconname.split(":")[1]
        iconname = iconname.replace("_"," ")
        iconname = iconname.title()
        authorid = message.content.split("@")[1]
        authorid = int(authorid.split(">")[0])
        user = self.client.get_user(authorid)
        thumburl = "https://cdn.discordapp.com/emojis/"
        icon = str(icon)
        thumburl = thumburl+icon
        thumburl = thumburl+".webp?size=96&quality=lossless"
        print(thumburl)
        desc_text = f"Original message: [Click here]({message.jump_url})\n"
        embed = await Custom_embed(self.client,thumb=thumburl,description="**"+iconname+"** was viciously defeated and dropped their icon.\n"+desc_text).setup_embed()
        embed.set_footer(text=(f'{self.client.user.display_name}'+" | at UTC "f'{Rare_spawns.timestamp}'), icon_url=f'{self.client.user.avatar}')
        embed.set_author(name=f'{self.client.get_user(authorid).display_name}'" just found a new icon!", icon_url="https://cdn.discordapp.com/emojis/766701189260771359.webp?size=96&quality=lossless")
        await receiver_channel.send(embed=embed)
        await log_chn.send(user.name+" found an icon")
        await log_chn.send("Its "+iconname)

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
        embed.set_footer(text=(f'{self.client.user.display_name}'+" | at UTC "f'{Rare_spawns.timestamp}'), icon_url=f'{self.client.user.avatar}')
        await announce.send(embed=embed)
        emoji = '🔔'
        await message.add_reaction(emoji)
        return

    async def gold_spawn(self, message):
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
        data_pr = self.db.execute(f'SELECT * FROM Dex WHERE Img_url = "{_embed.image.url}"')
        data_pr = data_pr.fetchall()
        logging = 1083131761451606096
        logging = self.client.get_channel(logging)
        try:
            await logging.send(embed=message.embed)
        except:
            logging.send("NO message to log")
        try:
            await logging.send(_embed.description)
        except:
            logging.send("How's there no description???")
        #print(data_pr[0][14])
        raremon = poke_rarity[(data_pr[0][14])]
        description_text = f"Original message: [Click here]({message.jump_url})\n"
        embed = disnake.Embed(title=raremon+" **"+data_pr[0][1]+"** \nDex: #"+str(data_pr[0][0]), color=_embed.color,description=description_text)
        embed.set_author(name=(f'{sender.display_name}'+" just claimed a:"),icon_url="https://cdn.discordapp.com/emojis/676623920711073793.webp?size=96&quality=lossless")
        embed.set_image(_embed.image.url)
        embed.set_footer(text=(f'{self.client.user.display_name}'+" | at UTC "f'{Rare_spawns.timestamp}'), icon_url=f'{self.client.user.avatar}')
        await receiver_channel.send(embed=embed)

    async def box_spawn(self, message):
        pass

    async def chamber_claim(self, message):
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
        nite = message.content.split("<:")[1]
        item = nite.split(":")[0]
        try:
            if chambers[item]:
                print(f'{item}, {chambers[item]}')
                number = nite.split(":")[1]
                number = number.split(">")[0]
                dex = self.db.execute(f'SELECT * FROM Dex WHERE DexID = {chambers[item]}')
                dex = dex.fetchone()
                print(dex[1])
                current_time = message.created_at
                timestamp = current_time.strftime('%Y-%m-%d %H:%M:%S')
                description_text = f"Original message: [Click here]({message.jump_url})\n"
                embed = disnake.Embed(title=f"{sender.display_name} was able to claim a **{item.capitalize()}**",description=description_text)
                embed.set_author(name=(f'{sender.display_name}'+" won in a megachamber!"),icon_url=f"https://cdn.discordapp.com/emojis/{number}.webp?size=96&quality=lossless")
                embed.set_footer(text=(f'{self.client.user.display_name}'+" | at UTC "f'{timestamp}'), icon_url=f'{self.client.user.avatar}')
                embed.set_image(dex[15])
                await receiver_channel.send(embed=embed)
        except Exception as e:
            print(f"No valid Chamber, its too easy: {e}")

    async def code_claim(self, message):
        receiver_channel = self.db.execute(f'SELECT * FROM Admin WHERE Server_ID = {message.guild.id}')
        receiver_channel = receiver_channel.fetchone()
        receiver_channel = int(receiver_channel[4])
        if receiver_channel > 0:
            receiver_channel = self.client.get_channel(int(receiver_channel))
        if message.reference:
            ref_msg = await message.channel.fetch_message(message.reference.message_id)
            sender = ref_msg.author
        elif message.interaction:
            sender = message.interaction.author
        monname = message.content.split("**")[1]
        monname = monname+" "
        data = self.db.execute(f'SELECT * FROM Dex WHERE Name LIKE "{monname}"')
        data = data.fetchall()
        #print(data)
        url = data[0][15]
        #print(url)
        monname = data[0][1]
        print(monname)
        current_time = message.created_at
        timestamp = current_time.strftime('%Y-%m-%d %H:%M:%S')
        description_text = f"Original message: [Click here]({message.jump_url})\n"
        embed = await Custom_embed(self.client,thumb=url,description=sender.display_name+" just claimed a **"+monname+"** from a code.\n"+description_text).setup_embed()
        embed.set_footer(text=(f'{self.client.user.display_name}'+" | at UTC "f'{timestamp}'), icon_url=f'{self.client.user.avatar}')
        embed.set_author(name=f'{sender.display_name}'" just redeemed a code!", icon_url="https://cdn.discordapp.com/emojis/671852541729832964.webp?size=240&quality=lossless")
        await receiver_channel.send(embed=embed)


def setup(client):
    client.add_cog(Rare_spawns(client))