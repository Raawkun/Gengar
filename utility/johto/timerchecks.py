import asyncio
import datetime
from sqlite3 import connect
import time
import disnake
from disnake.ext import commands
from utility.info_dict import rem_emotes, poke_rarity, embed_color, chambers
from utility.egglist import eggexcl
from utility.embed import Custom_embed

class TimerChecks(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.db = connect("database.db")


    async def itemcheck(self, msg, sender):
        data = self.db.execute(f'SELECT Emotes, React, Grazz, Repel, Ping FROM Toggles WHERE User_ID = {sender.id}')
        data = data.fetchone()
        if data:
            if data[3] == 1:
                if "super_repel" in msg.content and "boost" in msg.content:
                    if data[0]==0:
                        desc=f'{rem_emotes["remind"]} - <@{sender.id}> Hey, your {rem_emotes["superrepel"]} boost expired!'
                    else:
                        desc=f'{rem_emotes["remind"]} - <@{sender.id}> {rem_emotes["superrepel"]}'
                    if data[1] == 1:
                        emote = int((rem_emotes["supperrepel"].split(":")[2]).split(">")[0])
                        emote = self.client.get_emoji(emote)
                        await msg.add_reaction(emote)
                    else:
                        if data[4] == 0:
                            await msg.channel.send(desc, allowed_mentions=disnake.AllowedMentions(users=False))
                        else:
                            await msg.channel.send(desc)
                if "max_repel" in msg.content and "boost" in msg.content:
                    if data[0]==0:
                        desc=f'{rem_emotes["remind"]} - <@{sender.id}> Hey, your {rem_emotes["maxrepel"]} boost expired!'
                    else:
                        desc=f'{rem_emotes["remind"]} - <@{sender.id}> {rem_emotes["maxrepel"]}'
                    if data[1] == 1:
                        emote = int((rem_emotes["maxrepel"].split(":")[2]).split(">")[0])
                        emote = self.client.get_emoji(emote)
                        await msg.add_reaction(emote)
                    else:
                        if data[4] == 0:
                            await msg.channel.send(desc, allowed_mentions=disnake.AllowedMentions(users=False))
                        else:
                            await msg.channel.send(desc)
                if ":repel" in msg.content and "boost" in msg.content:
                    if data[0]==0:
                        desc=f'{rem_emotes["remind"]} - <@{sender.id}> Hey, your {rem_emotes["repel"]} boost expired!'
                    else:
                        desc=f'{rem_emotes["remind"]} - <@{sender.id}> {rem_emotes["repel"]}'
                    if data[1] == 1:
                        emote = int((rem_emotes["repel"].split(":")[2]).split(">")[0])
                        emote = self.client.get_emoji(emote)
                        await msg.add_reaction(emote)
                    else:
                        if data[4] == 0:
                            await msg.channel.send(desc, allowed_mentions=disnake.AllowedMentions(users=False))
                        else:
                            await msg.channel.send(desc)
                if ":fluffy" in msg.content:
                    if data[0]==0:
                        desc=f'{rem_emotes["remind"]} - <@{sender.id}> Hey, your {rem_emotes["fluffy"]} boost expired!'
                    else:
                        desc=f'{rem_emotes["remind"]} - <@{sender.id}> {rem_emotes["fluffy"]}'
                    if data[1] == 1:
                        emote = int((rem_emotes["fluffy"].split(":")[2]).split(">")[0])
                        emote = self.client.get_emoji(emote)
                        await msg.add_reaction(emote)
                    else:
                        if data[4] == 0:
                            await msg.channel.send(desc, allowed_mentions=disnake.AllowedMentions(users=False))
                        else:
                            await msg.channel.send(desc)
                if ":pokedoll" in msg.content:
                    if data[0]==0:
                        desc=f'{rem_emotes["remind"]} - <@{sender.id}> Hey, your {rem_emotes["pokedoll"]} boost expired!'
                    else:
                        desc=f'{rem_emotes["remind"]} - <@{sender.id}> {rem_emotes["pokedoll"]}'
                    if data[1] == 1:
                        emote = int((rem_emotes["pokedoll"].split(":")[2]).split(">")[0])
                        emote = self.client.get_emoji(emote)
                        await msg.add_reaction(emote)
                    else:
                        if data[4] == 0:
                            await msg.channel.send(desc, allowed_mentions=disnake.AllowedMentions(users=False))
                        else:
                            await msg.channel.send(desc)
                if ":poketoy" in msg.content:
                    if data[0]==0:
                        desc=f'{rem_emotes["remind"]} - <@{sender.id}> Hey, your {rem_emotes["poketoy"]} boost expired!'
                    else:
                        desc=f'{rem_emotes["remind"]} - <@{sender.id}> {rem_emotes["poketoy"]}'
                    if data[1] == 1:
                        emote = int((rem_emotes["poketoy"].split(":")[2]).split(">")[0])
                        emote = self.client.get_emoji(emote)
                        await msg.add_reaction(emote)
                    else:
                        if data[4] == 0:
                            await msg.channel.send(desc, allowed_mentions=disnake.AllowedMentions(users=False))
                        else:
                            await msg.channel.send(desc)
            else: return
            if data[2] == 1:
                if "goldenrazz" in msg.content and "boost" in msg.content:
                    if data[0]==0:
                        desc=f'{rem_emotes["remind"]} - <@{sender.id}> Hey, your {rem_emotes["grazz"]} boost expired!'
                    else:
                        desc=f'{rem_emotes["remind"]} - <@{sender.id}> {rem_emotes["grazz"]}'
                    if data[1] == 1:
                        emote = int((rem_emotes["grazz"].split(":")[2]).split(">")[0])
                        emote = self.client.get_emoji(emote)
                        await msg.add_reaction(emote)
                    else:
                        if data[4] == 0:
                            await msg.channel.send(desc, allowed_mentions=disnake.AllowedMentions(users=False))
                        else:
                            await msg.channel.send(desc)
                if "honey" in msg.content and "boost" in msg.content:
                    if data[0]==0:
                        desc=f'{rem_emotes["remind"]} - <@{sender.id}> Hey, your {rem_emotes["honey"]} boost expired!'
                    else:
                        desc=f'{rem_emotes["remind"]} - <@{sender.id}> {rem_emotes["honey"]}'
                    if data[1] == 1:
                        emote = int((rem_emotes["honey"].split(":")[2]).split(">")[0])
                        emote = self.client.get_emoji(emote)
                        await msg.add_reaction(emote)
                    else:
                        if data[4] == 0:
                            await msg.channel.send(desc, allowed_mentions=disnake.AllowedMentions(users=False))
                        else:
                            await msg.channel.send(desc)
            else: return

    async def raritycheck(self, log, before, after, sender):
        _embed = after.embeds[0]
        color = _embed.color
        #print(timestamp)
        Rare_Spawns = ["Event", "Legendary", "Shiny","Golden"]
        #Rare_Spawns = ["Event", "Legendary", "Shiny", "Common", "Uncommon", "Rare", "SuperRare","Golden"]
        if _embed.description:
            if _embed.footer.text:
                #print("Oh, a footer!")
                try:
                    data = self.db.execute(f'SELECT * FROM Dex WHERE Img_url = "{_embed.image.url}"')
                    data = data.fetchone()
                    #print(data)
                except Exception as e:
                    #print(f"No data - {e}")
                    return
                if "caught a" in _embed.description:
                    if "token" in _embed.footer.text.lower():
                        #print(f"caught a {data[1]}")
                        raremon = data[14]
                        ball = _embed.description.split(" with a")[1]
                        ball = ball.split("!")[0]
                        ball = ball.split(" ")[1]
                        #print("Fish caught")
                        if raremon in Rare_Spawns or _embed.color == 0xe9270b:
                            #print(f"in raremon - {raremon}")
                            raremon = poke_rarity[(data[14])]
                            description_text = f"Original message: [Click here]({before.jump_url})\n"
                            embed = disnake.Embed(title=raremon+" **"+data[1]+"** \nDex: #"+str(data[0]), color=color,description=description_text)
                            embed.set_author(name=(sender.display_name+" just caught a:"), icon_url=_embed.author.icon_url)
                            embed.set_image(_embed.image.url)
                            embed.timestamp = after.edited_at
                            embed.set_footer(text=(f'{self.client.user.display_name}'+" | Message from "), icon_url=f'{self.client.user.avatar}')
                            await log.send(embed=embed)
                            emoji = '🔔'
                            await after.add_reaction(emoji)
                    else:
                        description_text = ""
                        if "retrieved a" in _embed.description:
                            item = _embed.description.split("retrieved")[1]
                            item = item.split("**")[1]
                            print(item)
                            description_text = f"<:held_item:1213754494266122280> **It held onto a {item}**.\n"
                        raremon = data[14]
                        ball = _embed.description.split(" with a")[1]
                        ball = ball.split("!")[0]
                        ball = ball.split(" ")[1]
                        #print("Fish caught")
                        if raremon in Rare_Spawns or _embed.color == 0xe9270b:
                            #print(f"in raremon - {raremon}")
                            raremon = poke_rarity[(data[14])]
                            description_text = f"Original message: [Click here]({before.jump_url})\n"
                            embed = disnake.Embed(title=raremon+" **"+data[1]+"** \nDex: #"+str(data[0]), color=color,description=description_text)
                            embed.set_author(name=(sender.display_name+" just caught a:"), icon_url=_embed.author.icon_url)
                            embed.set_image(_embed.image.url)
                            embed.timestamp = after.edited_at
                            embed.set_footer(text=(f'{self.client.user.display_name}'+" | Message from "), icon_url=f'{self.client.user.avatar}')
                            await log.send(embed=embed)
                            emoji = '🔔'
                            await after.add_reaction(emoji)
                if "broke out" in _embed.description:
                    raremon = data[14]
                    ball = _embed.description.split(" out of the")[1]
                    ball = ball.split("!")[0]
                    ball = ball.split(" ")[1]
                    if raremon in Rare_Spawns or _embed.color == 0xe9270b:
                        raremon = poke_rarity[(data[14])]
                        description_text = f"Original message: [Click here]({before.jump_url})\n"
                        embed = disnake.Embed(title=raremon+" **"+data[1]+"** \nDex: #"+str(data[0]), color=color,description=description_text)
                        embed.set_author(name=(sender.display_name+" almost caught a:"), icon_url=_embed.author.icon_url)
                        embed.set_image(_embed.image.url)
                        embed.timestamp = after.edited_at
                        embed.set_footer(text=(f'{self.client.user.display_name}'+" | Message from "), icon_url=f'{self.client.user.avatar}')
                        await log.send(embed=embed)
                        emoji = '🔔'
                        await after.add_reaction(emoji)
                if "ran away" in _embed.description:
                    raremon = data[14]
                    if raremon in Rare_Spawns or _embed.color == 0xe9270b:
                        raremon = poke_rarity[(data[14])]
                        description_text = f"Original message: [Click here]({before.jump_url})\n"
                        embed = disnake.Embed(title=raremon+" **"+data[1]+"** \nDex: #"+str(data[0]), color=color,description=description_text)
                        embed.set_author(name=(sender.display_name+" was too slow for:"), icon_url=_embed.author.icon_url)
                        embed.set_image(_embed.image.url)
                        embed.timestamp = after.edited_at
                        embed.set_footer(text=(f'{self.client.user.display_name}'+" | Message from "), icon_url=f'{self.client.user.avatar}')
                        anno = await log.send(embed=embed)
                        emoji = '🔔'
                        await after.add_reaction(emoji)

    async def explorecheck(self, log, mon, after, sender):
        
        if "just caught a " in after.content:
        
            raremon = poke_rarity[(mon[14])]
            description_text = f"Original message: [Click here]({after.jump_url})\n"
            embed = disnake.Embed(title=raremon+" **"+mon[1]+"** \nDex: #"+str(mon[0]), color=embed_color[mon[14]],description=description_text)
            embed.set_author(name=(f'{sender}'+" just discovered a:"), icon_url="https://cdn.discordapp.com/emojis/1072075141489623040.webp?size=96&quality=lossless")
            embed.set_image(mon[15])
            embed.set_footer(text=(f'{self.client.user.display_name}'+" | at UTC "f'{time.time()}'), icon_url=f'{self.client.user.avatar}')
            await log.send(embed=embed)
                
            print("Explore: Caught it!")
        elif "broke out" in after.content:
        
            raremon = poke_rarity[(mon[14])]
            description_text = f"Original message: [Click here]({after.jump_url})\n"
            embed = disnake.Embed(title=raremon+" **"+mon[1]+"** \nDex: #"+str(mon[0]), color=embed_color[mon[14]],description=description_text)
            embed.set_author(name=(f'{sender}'+" almost caught a:"), icon_url="https://cdn.discordapp.com/emojis/1072075141489623040.webp?size=96&quality=lossless")
            embed.set_image(mon[15])
            embed.set_footer(text=(f'{self.client.user.display_name}'+" | at UTC "f'{time.time()}'), icon_url=f'{self.client.user.avatar}')
            await log.send(embed=embed)
                
            print("Explore: Broke out")
        elif "ran away" in after.content:
            raremon = poke_rarity[(mon[14])]
            description_text = f"Original message: [Click here]({after.jump_url})\n"
            embed = disnake.Embed(title=raremon+" **"+mon[1]+"** \nDex: #"+str(mon[0]), color=embed_color[mon[14]],description=description_text)
            embed.set_author(name=(sender+" was too slow for:"), icon_url="https://cdn.discordapp.com/emojis/1072075141489623040.webp?size=96&quality=lossless")
            embed.set_image(mon[15])
            embed.set_footer(text=(f'{self.client.user.display_name}'+" | at UTC "f'{time.time()}'), icon_url=f'{self.client.user.avatar}')
            await log.send(embed=embed)
                
            print("Explore: Ran away")

    async def spawncheck(self, msg, sender):
        rem = self.db.execute(f'SELECT Linked, Emotes, React, ToggleSpawn, Ping FROM Toggles WHERE User_ID = {sender.id}')
        rem = rem.fetchone()
        #print(rem)
        await asyncio.sleep(8.8)
        if rem[3] == 1:
            if rem[0] == 0:
                link = ";p"
            else:
                link = "</pokemon:1015311085441654824>"
            if rem[1]==0:
                desc=f'{rem_emotes["remind"]} - <@{sender.id}>, you can now use {link} again.'
            else:
                if rem[0] == 0:
                    link = ""
                desc = f'{rem_emotes["remind"]} - <@{sender.id}> {rem_emotes["spawn"]} {link}'
            if rem[2] == 1:
                emote = int((rem_emotes["spawn"].split(":")[2]).split(">")[0])
                emote = self.client.get_emoji(emote)
                await msg.add_reaction(emote)
            else:
                if rem[4] == 1:
                    await msg.channel.send(desc)
                else:
                    await msg.channel.send(desc, allowed_mentions = disnake.AllowedMentions(users = False))

    async def fishcheck(self, msg, sender):
        rem = self.db.execute(f'SELECT Linked, Emotes, React, ToggleFish, Ping FROM Toggles WHERE User_ID = {sender.id}')
        rem = rem.fetchone()
        print(f"Fishcheck{rem}")
        await asyncio.sleep(24.2)
        if rem[3] == 1:
            if rem[0] == 0:
                link = ";fish"
            else:
                link = "</fish spawn:1015311084812501026>"
            if rem[1]==0:
                desc=f'{rem_emotes["remind"]} - <@{sender.id}>, you can now use {link} again.'
            else:
                if rem[0] == 0:
                    link = ""
                desc = f'{rem_emotes["remind"]} - <@{sender.id}> {rem_emotes["fish"]} {link}'
            if rem[2] == 1:
                emote = int((rem_emotes["fish"].split(":")[2]).split(">")[0])
                emote = self.client.get_emoji(emote)
                await msg.add_reaction(emote)
            else:
                if rem[4] == 1:
                    await msg.channel.send(desc)
                else:
                    await msg.channel.send(desc, allowed_mentions = disnake.AllowedMentions(users = False))

    async def battlecheck(self, msg, sender):
        rem = self.db.execute(f'SELECT Linked, Emotes, React, ToggleBattle, Ping FROM Toggles WHERE User_ID = {sender.id}')
        rem = rem.fetchone()
        print(f"Battlecheck{rem}")
        await asyncio.sleep(59)
        if rem[3] == 1:
            if rem[0] == 0:
                link = ";battle"
            else:
                link = "</battle:1015311084422434819>"
            if rem[1]==0:
                desc=f'{rem_emotes["remind"]} - <@{sender.id}>, you can now use {link} again.'
            else:
                if rem[0] == 0:
                    link = ""
                desc = f'{rem_emotes["remind"]} - <@{sender.id}> {rem_emotes["battle"]} {link}'
            if rem[2] == 1:
                emote = int((rem_emotes["battle"].split(":")[2]).split(">")[0])
                emote = self.client.get_emoji(emote)
                await msg.add_reaction(emote)
            else:
                if rem[4] == 1:
                    await msg.channel.send(desc)
                else:
                    await msg.channel.send(desc, allowed_mentions = disnake.AllowedMentions(users = False))
            
    async def otherchecks(self, msg, sender, other):
        rem = self.db.execute(f'SELECT Linked, Emotes, React, ToggleOthers, Ping FROM Toggles WHERE User_ID = {sender.id}')
        rem = rem.fetchone()
        if other == "swap":
            await asyncio.sleep(6)
            if rem[0] == 0:
                link = ";swap"
            else:
                link = "</swap info:1015013443000074363>"
        elif other == "buddy":
            await asyncio.sleep(5)
            if rem[0] == 0:
                link = ";buddy"
            else:
                link = "</buddy current-buddy:1015311084422434823>"
        elif other == "moves":
            await asyncio.sleep(5)
            other = "buddy"
            if rem[0] == 0:
                link = ";moves"
            else:
                link = "</moves view:1015311085441654817>"
        elif other == "catchbot":
            await asyncio.sleep(5)
            if rem[0] == 0:
                link = ";catchbot"
            else:
                link = "</catchbot view:1015311084422434824>"
        elif other == "egg":
            await asyncio.sleep(5)
            if rem[0] == 0:
                link = ";egg"
            else:
                link = "</egg status:1015311084594405485>"
        elif other == "give":
            await asyncio.sleep()
            if rem[0] == 0:
                link = ";give"
            else:
                link = "</give:1015311084812501028>"
        elif other == "market":
            await asyncio.sleep(3)
            if rem[0] == 0:
                link = ";market"
            else:
                link = "</market view:1015311085307445255>"
        if rem[3] == 1:
            if rem[1]==0:
                desc=f'{rem_emotes["remind"]} - <@{sender.id}>, you can now use {link} again.'
            else:
                if rem[0] == 0:
                    link = ""
                desc = f'{rem_emotes["remind"]} - <@{sender.id}> {rem_emotes[other]} {link}'
            if rem[2] == 1:
                try:
                    emote = int((rem_emotes[other].split(":")[2]).split(">")[0])
                    emote = self.client.get_emoji(emote)
                except:
                    emote = rem_emotes[other].split[0]
                await msg.add_reaction(emote)
            else:
                if rem[4] == 1:
                    await msg.channel.send(desc)
                else:
                    await msg.channel.send(desc, allowed_mentions = disnake.AllowedMentions(users = False))

    async def questcheck(self, msg, sender):
        rem = self.db.execute(f'SELECT Linked, Emotes, React, ToggleQuest, Ping FROM Toggles WHERE User_ID = {sender.id}')
        rem = rem.fetchone()
        #print(rem)
        await asyncio.sleep(6)
        if rem[3] == 1:
            if rem[0] == 0:
                link = ";quest"
            else:
                link = "</quest info:1015311085517156475>"
            if rem[1]==0:
                desc=f'{rem_emotes["remind"]} - <@{sender.id}>, you can now use {link} again.'
            else:
                if rem[0] == 0:
                    link = ""
                desc = f'{rem_emotes["remind"]} - <@{sender.id}> {rem_emotes["quest"]} {link}'
            if rem[2] == 1:
                emote = int((rem_emotes["quest"].split(":")[2]).split(">")[0])
                emote = self.client.get_emoji(emote)
                await msg.add_reaction(emote)
            else:
                if rem[4] == 1:
                    await msg.channel.send(desc)
                else:
                    await msg.channel.send(desc, allowed_mentions = disnake.AllowedMentions(users = False))

    async def iconcheck(self,log,  msg, sender):
        iconname = msg.content.split("unlocked ")[1]
        icon = iconname.split(":")[2]
        icon = icon.split(">")[0]
        iconname = iconname.split(":")[1]
        iconname = iconname.replace("_"," ")
        iconname = iconname.title()
        authorid = msg.content.split("@")[1]
        authorid = int(authorid.split(">")[0])
        thumburl = "https://cdn.discordapp.com/emojis/"
        icon = str(icon)
        thumburl = thumburl+icon
        thumburl = thumburl+".webp?size=96&quality=lossless"
        print(thumburl)
        desc_text = f"Original message: [Click here]({msg.jump_url})\n"
        embed = await Custom_embed(self.client,thumb=thumburl,description="**"+iconname+"** was viciously defeated and dropped their icon.\n"+desc_text).setup_embed()
        embed.set_footer(text=(f'{self.client.user.display_name}'+" | Message from "), icon_url=f'{self.client.user.avatar}')
        embed.timestamp = msg.created_at
        embed.set_author(name=f'{self.client.get_user(authorid).display_name}'" just found a new icon!", icon_url="https://cdn.discordapp.com/emojis/766701189260771359.webp?size=96&quality=lossless")
        await log.send(embed=embed)

    async def rarecheck(self, log, mode, message, mon, sender): #For eggs, boxes, swap etc.
        emb =  message.embeds[0]
        Rare_Spawn = ["Event", "Legendary", "Shiny", "Golden"]
        description_text = ""
        if mon[14] in Rare_Spawn or str(mon[0]) in eggexcl:
            if mode == "egg":
                mode = " just hatched an exclusive:"
                icon = "https://cdn.discordapp.com/emojis/689325070015135745.gif?size=96&quality=lossless"
            elif mode == "box":
                mode = " just unboxed a:"
                icon = "https://cdn.discordapp.com/emojis/784865588207157259.gif?size=96&quality=lossless"
                if "Pokemon received" in emb.description:
                                    mons = emb.description.split("total):\n")[1]
                                    mons = mons.split(">")
                                    unused = mons.pop()
                                    description_text = "Pokemon received:\n"
                                    for entry in mons:
                                        monid = entry.split(":")[1]
                                        monid = int(monid)
                                        dex = self.db.execute(f'SELECT * FROM SpawnEmotes WHERE DexID = {monid}')
                                        dex = dex.fetchone()
                                        description_text += f'<:{monid}:{dex[3]}> '
            elif mode == "swap":
                mode = " just swapped for a:"
                icon = "https://cdn.discordapp.com/emojis/869901886080315392.webp?size=96&quality=lossless"
            description_text += f"Original message: [Click here]({message.jump_url})\n"
            raremon = poke_rarity[mon[14]]
            embed = disnake.Embed(title=raremon+" **"+mon[1]+"** \nDex: #"+str(mon[0]), color=embed_color[mon[14]],description=description_text)
            embed.set_author(name=(sender.display_name+mode),icon_url=icon)
            embed.set_image(mon[15])
            embed.set_footer(text=(f'{self.client.user.display_name}'+" | Message from "), icon_url=f'{self.client.user.avatar}')
            embed.timestamp = message.created_at
            await log.send(embed=embed)

    async def cbcheck(self, log, message, sender):
        description_text = f"Original message: [Click here]({message.jump_url})\n"
        emb = message.embeds[0]
        stamp = message.created_at
        if "Legendary" in emb.description:
            legy_mon = emb.description.split(":Legendary:")[1]
            legy_numb = legy_mon.split(":")[1]
            data = self.db.execute(f'SELECT * FROM Dex WHERE DexID = "{legy_numb}"')
            data = data.fetchone()
            raremon = poke_rarity[(data[14])]
            embed = disnake.Embed(title=raremon+" **"+data[1]+"** \nDex: #"+str(data[0]), color=embed_color[data[14]],description=description_text)
            embed.set_author(name=(sender.display_name+"'s catchbot brought a:"),icon_url="https://cdn.discordapp.com/emojis/1167818560752603196.webp?size=96&quality=lossless")
            embed.set_image(data[15])
            embed.set_footer(text=(f'{self.client.user.display_name}'+" | at UTC "f'{stamp}'), icon_url=f'{self.client.user.avatar}')
            await log.send(embed=embed)
        if "Shiny" in emb.description:
            shiny_mon = emb.description.split(":Shiny:")[1]
            shiny_numb = shiny_mon.split(":")[1]
            data = self.db.execute(f'SELECT * FROM Dex WHERE DexID = "{shiny_numb}"')
            data = data.fetchone()
            real_mon = "Shiny "+data[1]
            data = self.db.execute(f'SELECT * FROM Dex WHERE Name = "{real_mon}"')
            data = data.fetchall()
            raremon = poke_rarity[(data[14])]
            embed = disnake.Embed(title=raremon+" **"+data[1]+"** \nDex: #"+str(data[0]), color=embed_color[data[14]],description=description_text)
            embed.set_author(name=(sender.display_name+"'s catchbot brought a:"),icon_url="https://cdn.discordapp.com/emojis/717198164280606802.gif?size=96&quality=lossless")
            embed.set_image(data[15])
            embed.set_footer(text=(f'{self.client.user.display_name}'+" | at UTC "f'{stamp}'), icon_url=f'{self.client.user.avatar}')
            await log.send(embed=embed)
        if "Golden" in emb.description:
            gold_mon = emb.description.split(":Golden:")[1]
            gold_numb = gold_mon.split(":")[1]
            data = self.db.execute(f'SELECT * FROM Dex WHERE DexID = "{gold_numb}"')
            data = data.fetchone()
            real_mon = "Golden "+data[1]
            data = self.db.execute(f'SELECT * FROM Dex WHERE Name = "{real_mon}"')
            data = data.fetchall()
            raremon = poke_rarity[(data[14])]
            embed = disnake.Embed(title=raremon+" **"+data[1]+"** \nDex: #"+str(data[0]), color=embed_color[data[14]],description=description_text)
            embed.set_author(name=(sender.display_name+"'s catchbot brought a:"),icon_url="https://cdn.discordapp.com/emojis/717198164280606802.gif?size=96&quality=lossless")
            embed.set_image(data[15])
            embed.set_footer(text=(f'{self.client.user.display_name}'+" | at UTC "f'{stamp}'), icon_url=f'{self.client.user.avatar}')
            await log.send(embed=embed)

    async def claimcheck(self, log, message, sender):
        stamp = round(datetime.datetime.timestamp())
        emb = message.embeds[0]
        data = self.db.execute(f'SELECT * FROM Dex WHERE Img_url = "{emb.image.url}"')
        data = data.fetchone()
        raremon = poke_rarity[(data[14])]
        description_text = f"Original message: [Click here]({message.jump_url})\n"
        embed = disnake.Embed(title=raremon+" **"+data[1]+"** \nDex: #"+str(data[0]), color=emb.color,description=description_text)
        embed.set_author(name=(f'{sender.display_name}'+" just claimed a:"),icon_url="https://cdn.discordapp.com/emojis/676623920711073793.webp?size=96&quality=lossless")
        embed.set_image(emb.image.url)
        embed.set_footer(text=(f'{self.client.user.display_name}'+" | at UTC "f'{stamp}'), icon_url=f'{self.client.user.avatar}')
        await log.send(embed=embed)

    async def marketcheck(self, message, sender):
        emb = message.embeds[0]
        try:
            dex=emb.author.name.split("#")[1]
            data = self.db.execute(f'SELECT * FROM Dex WHERE DexID = {dex}')
            data = data.fetchone()
            if data[17] >=2:
                lowest = f'{data[17]:,}'
                amount = f'{data[19]:,}'
                time = str(data[18])
                msg = "Lowest Price: "+lowest+"\nAmount: "+amount+"\nLast Update: <t:"+time+":f>"
                thumb = emb.thumbnail.url
                embed = await Custom_embed(self.client,title=data[1]+" #"+str(data[0]),description=msg,thumb=thumb).setup_embed()
                await message.channel.send(embed=embed)
        except Exception as e:
            error = self.client.get_channel(1227339831982690354)
            await error.send(f"{e} - {message.jump_url}")

    async def dexcheck(self, message, sender):
        emb = message.embeds[0]
        try:
            dex=emb.author.name.split(" #")[1]
            name=emb.author.name.split(" #")[0]
            print(f"{dex} - {name}")
            try:
                data = self.db.execute(f'SELECT * FROM Dex WHERE DexID = {dex}')
                data = data.fetchone()
                val = data[17]
                time = data[18]
                amount = data[19]
            except:
                val = 0
                time = 0
                amount = 0
            for field in emb.fields:
                if field.name == "Dex Number":
                    region = field.value.split("> ")[1]
                    region = region.split(" ")[0]
                if field.name == "Type":
                    type1= field.value.split()[0]
                    type1_semi = type1.split(":")[1]
                    type1_semi = type1_semi.split("type")[0]
                    try:
                        type2 = field.value.split()[1]
                        type2_semi = type2.split(":")[1]
                        type2_semi = type2_semi.split("type")[0]
                    except: type2_semi = None
                if field.name == "Base Attack":
                    b_atk = field.value.split()[1]
                if field.name == "Base Defense":
                    b_def = field.value.split()[1]
                if field.name == "Base HP":
                    b_hp = field.value.split()[1]
                if field.name == "Base Sp. Atk":
                    b_spatk = field.value.split()[1]
                if field.name == "Base Sp. Def":
                    b_spdef = field.value.split()[1]
                if field.name == "Base Speed":
                    b_spd = field.value.split()[1]
                if field.name == "Rarity":
                    rarity = field.value.split(":")[1]
                    if rarity.lower() == "legendary":
                        legendary = True
                    else: legendary = False
                    if rarity.lower() == "shiny":
                        shiny = True
                    else: shiny = False
                    if rarity.lower() == "golden":
                        golden = True
                    else: golden = False
                    if rarity.lower() == "mega":
                        mega = True
                    else: mega = False
                    if rarity.lower() == "shinymega":
                        shiny = True
                        mega = True
                imageurl = emb.image.url
            self.db.execute(f'INSERT or REPLACE INTO Dex VALUES ({dex},"{name}","{type1_semi}","{type2_semi}",{b_hp},{b_atk},{b_def},{b_spatk},{b_spdef},{b_spd},{legendary},{shiny},{golden},{mega},"{rarity}","{imageurl}","{region}",{val},{time},{amount})')
            self.db.commit()
        except Exception as e: 
            error = self.client.get_channel(1227339831982690354)
            await error.send(f"{e} - {message.jump_url}")

    async def pricecheck(self, message, sender):
        emb = message.embeds[0]
        try:
            if "#" in emb.footer.text:
                number = emb.footer.text.split("#")[1]
                number = int(number.split(" ")[0])
                print(number)
                datdex = self.db.execute(f'SELECT * FROM Dex WHERE DexID = {number}')
                datdex = datdex.fetchone()
                print(f"{datdex[0]} - {datdex[1]}")
                current_time = int(datetime.datetime.timestamp(datetime.datetime.now()))
                if "amount for sale" in emb.description.lower():
                    price = emb.description.split("PokeCoin")[2]
                    lowprice = price.split(" ")[1]
                    lowprice = int(lowprice.replace(",", ""))
                    amount = int(price.split(" ")[5])
                else:
                    for entry in emb.fields:
                        if entry.name == "Price each":
                            print(entry.value)
                            price = entry.value.split("`")[1]
                            print(price)
                            lowprice = int(price.replace(",", ""))
                        if entry.name == "Amount Remaining":
                            amount = entry.value.split("`")[1]
                            amount = int((amount.split(" ")[0]).replace(",", ""))
                self.db.execute(f'UPDATE Dex Set LowestVal = {lowprice}, UpdateTime = {current_time}, Amount = {amount} WHERE DexID = {datdex[0]}')
                self.db.commit()
        except Exception as e:
            error = self.client.get_channel(1227339831982690354)
            await error.send(f"{e}")
            await error.send(f"{message.jump_url}")

    async def chambercheck(self, log, message, sender):
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
                description_text = f"Original message: [Click here]({message.jump_url})\n"
                embed = disnake.Embed(title=f"{sender.display_name} was able to claim a **{item.capitalize()}**",description=description_text)
                embed.set_author(name=(f'{sender.display_name}'+" won in a megachamber!"),icon_url=f"https://cdn.discordapp.com/emojis/{number}.webp?size=96&quality=lossless")
                embed.set_footer(text=(f'{self.client.user.display_name}'+" | Message from "), icon_url=f'{self.client.user.avatar}')
                embed.timestamp = message.created_at
                embed.set_image(dex[15])
                await log.send(embed=embed)
        except Exception as e:
            print(f"No valid Chamber, its too easy: {e}")

    async def newquest(self, message, sender):
        emb = message.embeds[0]
        msg = emb.footer.text
        msg = msg.split(": ")[1]
        hours = int(msg.split(" H")[0])*60*60
        minutes = msg.split("H ")[1]
        minutes = int(minutes.split(" M")[0])*60
        seconds = msg.split("M ")[1]
        seconds = int(seconds.split(" S")[0])
        waiter = hours+minutes+seconds
        datarem = self.db.execute(f'SELECT Linked, Emotes, ToggleQuestTimer,QuestActive FROM Toggles WHERE User_ID = {sender.id}')
        datarem = datarem.fetchone()
        print(f"Acquired a wait time for {sender.name} of {waiter} seconds.")
        if datarem[2] != 0:
            #print("QuestTimer is not off.")
            if datarem[3] == 0:
                #print("No quest active!")
                q_time = int(time.time())-8
                q_time = q_time+waiter
                data = self.db.execute(f"SELECT * FROM Quests WHERE User_ID = {sender.id}")
                data = data.fetchone()
                if not data:
                    #print("No previous data in 'Quests' db.")
                    self.db.execute(f'INSERT INTO Quests (Wait, Channel_ID, User_ID) VALUES ({q_time}, {message.channel.id}, {sender.id})')
                    self.db.commit()
                    q_time = str(q_time)
                    if datarem[2] == 1:
                        remind = 1
                    elif datarem[2] == 2:
                        remind = 2
                    if datarem[1] == 0:
                        emote = 0
                    else: 
                        emote = 1
                    if datarem[0] == 0:
                        link = 0
                    else:
                        link = 1
                    minutes = int(waiter/60)
                    if datarem[1] == 1:
                        desc = f'{rem_emotes["remind"]} - <@{sender.id}> {rem_emotes["quest"]}:alarm_clock::white_check_mark: <t:{q_time}:R>'
                    elif datarem[1] == 0:
                        desc = f"{rem_emotes['remind']} - <@{sender.id}>, I've set a timer, next quest is ready at <t:{q_time}:R>"
                    if datarem[2] == 1:
                        await message.channel.send(desc, allowed_mentions= disnake.AllowedMentions(users=False))
                    elif datarem[2] == 2:
                        await message.channel.send(desc)
                    await asyncio.create_task(TimerChecks.quest_reminder(self, message.channel.id, sender.id, waiter,remind, link, emote))
    
    async def quest_reminder(self, channelid, senderid, waiter, remind, link, emote):
        channel = self.client.get_channel(channelid)
        self.db.execute(f'UPDATE Toggles SET QuestActive = 1 WHERE User_ID = {senderid}')
        self.db.commit()
        print(f"Now starting the sleeping - {waiter} seconds for {senderid}")
        await asyncio.sleep(waiter)
        if link == 0:
            link = ";quest"
        else:
            link = f'</quest info:1015311085517156475>'
        if emote == 1:
            if link == 0:
                link = ""
            desc = f'{rem_emotes["remind"]} - <@{senderid}> {rem_emotes["next"]}{rem_emotes["quest"]} {link}'
        else:
            desc = f'{rem_emotes["remind"]} - <@{senderid}>, your next {link} is ready!'
        if remind == 1:
            await channel.send(desc, allowed_mentions = disnake.AllowedMentions(users=False))
        elif remind == 2:
            await channel.send(desc)
        self.db.execute(f'UPDATE Toggles SET QuestActive = 0 WHERE User_ID = {senderid}')
        self.db.commit()
        self.db.execute(f'DELETE FROM Quests WHERE User_ID = {senderid}')
        self.db.commit()

    # async def readyquests(self):
    #     reminders = self.db.execute(f'SELECT * FROM Quests ORDER BY Wait ASC')
    #     reminders = reminders.fetchall()
    #     print(f"Readyquest: {reminders}")
    #     for row in reminders:
    #         userid = row[0]
    #         channelid = row[1]
    #         self.db.execute(f'UPDATE Toggles SET QuestActive = 0 WHERE User_ID = {userid}')
    #         self.db.commit()
    #         current_time = int(time.time())
    #         waiter = row[2]
    #         if waiter > current_time:
    #             waiter = waiter-current_time
    #             data = self.db.execute(f"SELECT Linked, Emotes, Ping, ToggleQuestTimer FROM Toggles WHERE User_ID = {userid}")
    #             data = data.fetchone()
    #             if data[3] == 1:
    #                 reminder = 1
    #             elif data[3] == 2:
    #                 reminder = 2
    #             if row[1] == 1:
    #                 emote = 0
    #             else:
    #                 emote = 1
    #             if row[0] == 0:
    #                 link = 0
    #             else:
    #                 link = 1
    #             #print(f"Channel:{channelid}, User:{userid}, Waiter:{waiter}, Reminder:{reminder}, Link:{link}, Emote:{emote}")
    #             await asyncio.create_task(TimerChecks.quest_reminder(self, channelid, userid, waiter, reminder, link, emote))
    #         elif waiter < current_time:
    #             self.db.execute(f'DELETE FROM Quests WHERE User_ID = {userid}')
    #             self.db.commit()

def setup(client):
    client.add_cog(TimerChecks(client))