import asyncio
from datetime import datetime, timedelta
import os
import disnake
from disnake.ext import commands
import sqlite3, math
from sqlite3 import connect
from zoneinfo import ZoneInfo
import pytz
import numpy
from  utility.rarity_db import poke_rarity, embed_color, type_emotes, type_colors
from utility.embed import Custom_embed, Auction_embed
from utility.info_dict import cmds,functions
from utility.drop_chance import th_points
import random
from utility.all_checks import Basic_checker
import pandas
import aiosqlite
import openpyxl

class Modules(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.db = connect("database.db")

    hunted_type = ""

    async def load_type(self):
        data = self.db.execute(f"SELECT * FROM Events WHERE Name = 'TypeHunt'")
        data = data.fetchone()
        if data[1] == 1:
            Modules.hunted_type = f"{data[5]}"
            Modules.showtype(self)

    async def showtype(self):
        print(Modules.typehunt)
        
    async def adamannpc(self, message):
        if message.reference:
            ref = await message.channel.fetch_message(message.reference.message_id)
            sender = ref.author
        elif message.interaction:
            sender = message.interaction.author
        await asyncio.sleep(1800)
        await message.channel.send(f"<@{sender.id}> - Trainer **Xmas Steven** is ready for the next battle.\n**Don't forget to set the right team!!!** <:493:1213076751559819294>")

    # async def darktest(self, message):
    #     if message.reference:
    #         ref_msg = await message.channel.fetch_message(message.reference.message_id)
    #         sender = ref_msg.author
    #     elif message.interaction:
    #         sender = message.interaction.author
    #     if sender.id == 475664587736481792 or sender.id == 352224989367369729:
    #         #print("Sjaap battle - testing for Dark mons.")
    #         if len(message.embeds)>0:
    #             emb = message.embeds[0]
    #             #print("Has an embed.")
    #             if emb.description:
    #                 #print("Has a description.")
    #                 opponent = emb.description.split("challenged ")[1]
    #                 opponent = opponent.split("**")[1]
    #                 #print(opponent)
    #                 mons = emb.description.split(opponent)[2]
    #                 #print(mons)
    #                 mon = [mons.split(":")[1], mons.split(":")[3], mons.split(":")[5]]
    #                 #print(mon)
    #                 #await message.channel.send(mon)
    #                 desc = ""
    #                 i = 1
    #                 for entry in mon:
    #                     dex = self.db.execute(f'SELECT DexID, Name, Type_1, Type_2 FROM Dex WHERE DexID = {entry}')
    #                     dex = dex.fetchone()
    #                     #print(dex)
    #                     if dex[2] == "darktype" or dex[3] == "darktype":
    #                         desc += f"Team-number {i}: {dex[1]} is a Dark type Pokémon.\n"
    #                     i = i + 1
    #                 if desc != "":
    #                     await message.reply(f"<@{sender.id}>\n{desc}")

    async def averagecoins(self, message):
        #print("Someone caught.")
        if message.reference:
            ref_msg = await message.channel.fetch_message(message.reference.message_id)
            sender = ref_msg.author
        elif message.interaction:
            sender = message.interaction.author
        if len(message.embeds)>0:
            emb = message.embeds[0]
            if emb.footer.text:
                coin = emb.footer.text.split(" earned ")[1]
                coin = coin.split(" ")[0]
                try:
                    coin = coin.replace(",", "")
                except:
                    return
                #print(coin)
                try:
                    self.db.execute(f"INSERT INTO average VALUES ({sender.id}, '{sender.name}', {int(coin)}, 1, {int(coin)})")
                    self.db.commit()
                except:
                    try:
                        self.db.execute(F"UPDATE average SET coins = coins + {int(coin)}, catch_count = catch_count + 1 WHERE UserID = {sender.id}")
                        self.db.commit()
                        self.db.execute(f"UPDATE average SET avg_coins = coins/catch_count WHERE UserID = {sender.id}")
                        self.db.commit()
                    except Exception as e:
                        print(e)
    async def resetaverage(self):
        conn = sqlite3.connect('database.db')
        df = pandas.read_sql_query("SELECT * FROM average WHERE catch_count > 299 ORDER BY catch_count DESC", conn)
        file_path = "/tmp/exported_data.xlsx"
        df.to_excel(file_path,index=False,engine='openpyxl')
        conn.close()
        channel = self.client.get_channel(1272981076419149886)
        await channel.send(file=disnake.File(file_path))
        self.db.execute(f"DELETE FROM average")
        self.db.commit()
        os.remove(file_path)
    async def averagetimer(self):
        while True:
            cet = pytz.timezone('CET')
            now = datetime.now(cet)
            days_until_monday = (7-now.weekday())%7
            if days_until_monday == 0 and now.hour >= 14:
                days_until_monday = 7 
            next_monday = now + timedelta(days=days_until_monday)
            next_monday_at_2pm = cet.localize(datetime(next_monday.year, next_monday.month, next_monday.day, 14, 0, 0))
            #next_monday_at_2pm = now + datetime.timedelta(seconds=20)
            time_until = next_monday_at_2pm-now
            print(f"Setting a LB Timer for {time_until.total_seconds()} seconds.")
            await asyncio.sleep(time_until.total_seconds())
            await asyncio.create_task(Modules.resetaverage(self))

    async def dailyreset(self):
        while True:
            est = ZoneInfo("America/New_York")
            now = datetime.now(est)
            now = datetime(now.year, now.month,now.day,now.hour,now.minute,now.second)
            yesterday = now-timedelta(days=1)
            tomorrow = now+timedelta(days=1)
            date = str(f"{now.day}.{now.month}.{now.year}")
            date_yst = str(f"{yesterday.day}.{yesterday.month}.{yesterday.year}")
            date_tmr = str(f"{tomorrow.day}.{tomorrow.month}.{tomorrow.year}")
            reset_time = datetime(now.year,now.month,now.day,0,5,0)
            if now >= reset_time:
                check = self.db.execute(f"SELECT * FROM DailyStats WHERE Date = '{date}'")
                check = check.fetchone()
                if check is None:
                    self.db.execute(f"INSERT INTO DailyStats VALUES ('{date}',0,0,0,0,0,0,0,0,0,0,0,0,0)")
                    self.db.commit()
                check = self.db.execute(f"SELECT * FROM DailyStats WHERE Date = '{date_tmr}'")
                check = check.fetchone()
                if check is None:
                    self.db.execute(f"INSERT INTO DailyStats VALUES ('{date_tmr}',0,0,0,0,0,0,0,0,0,0,0,0,0)")
                    self.db.commit()
                reset_time += timedelta(days=1)
            
            sleep_duration = (reset_time - now).total_seconds()
            print(f"Sleep duration until next Daily Stat Reset: {sleep_duration / 3600} hours.")
            await asyncio.sleep(sleep_duration)

            est = ZoneInfo("America/New_York")
            now = datetime.now(est)
            yesterday = now-timedelta(days=1)
            date = str(f"{now.day}.{now.month}.{now.year}")
            date_yst = str(f"{yesterday.day}.{yesterday.month}.{yesterday.year}")
            
            para = 825813023716540426
            channel = 1063926051861971015 #MeowHelper-Daily-Stats in Paralympic
            channel = self.client.get_channel(channel)
            guild = channel.guild
            coin = "<:pokecoin:835054000063381516>"
            embed = disnake.Embed(title="Daily Server Stats",description=f"The daily server stats for {guild.name}.",color=disnake.Color.blurple())
            row = self.db.execute(f"SELECT * FROM DailyStats WHERE Date = '{date_yst}'")
            row = row.fetchone()
            
            embed.add_field(name="**Coins**",value=f"Total: {(row[1]+row[2]+row[3]+row[4]+row[5]):,} {coin}\nFrom Catches: {row[1]:,} {coin}\nFrom Battles: {row[2]:,} {coin}\nFrom Market: {row[3]:,} {coin}\nFrom Releasing: {row[4]:,} {coin}\nFrom World Boss: {row[5]:,} {coin}",inline=True)
            embed.add_field(name="**Pokémon**",value=f"Pokémon Seen: {row[6]:,} Pokémon\nPokémon Caught: {row[7]:,} Pokémon",inline=True)
            embed.add_field(name="**Battles**",value=f"Total Battles: {row[10]:,} Battles\nBattles Won: {row[11]:,} Battles\nIcon Drops: {row[12]:,} Icons",inline=True)
            embed.add_field(name="**Eggs**",value=f"Eggs Hatched: {row[13]:,} Eggs")
            embed.set_author(name=f"{date_yst}")
            embed.set_footer(text=f"Provided by Mega Gengar. | Daily Stats getting reset at 12pm EST.")
            await channel.send(embed=embed)

            await asyncio.sleep(3600)

    async def dailycheck(self,message):
        if message.guild.id == 825813023716540426: #paralympic
            est = ZoneInfo("America/New_York")
            now = datetime.now(est)
            date = str(f"{now.day}.{now.month}.{now.year}")
            #IconDrop
            if "you've unlocked" and " trainer icon" in message.content.lower():
                self.db.execute(f"UPDATE DailyStats SET Icons = Icons + 1 WHERE Date = '{date}'")
                self.db.commit()
            #PokeCaught from Explore
            if "you just caught a " in message.content.lower():
                coins = message.content.split("You earned")[1]
                coins = coins.split("> ")[1]
                coins = coins.split("!")[0]
                coins = int(coins.replace(",",""))
                #print(f"Explore catch; {coins}")
                self.db.execute(f"UPDATE DailyStats SET PokeCaught = PokeCaught + 1, CoinCatch = CoinCatch+{coins} WHERE Date = '{date}'")
                self.db.commit()
            #PokeSeen (Should also work for explore?)
            if "found a " in message.content.lower():
                self.db.execute(f"UPDATE DailyStats SET PokeSeen = PokeSeen + 1 WHERE Date = '{date}'")
                self.db.commit()
            #BattleWon &
            #CoinBattle
            if "won the battle" in message.content:
                try:
                    coins = message.content.lower().split(" pokecoins")[0]
                    coins = coins.split(" ")
                    gth = len(coins)-1
                    coins = int(coins[gth].replace(",",""))
                    self.db.execute(f"UPDATE DailyStats SET BattleWon = BattleWon+1,CoinBattle = CoinBattle + {coins} WHERE Date = '{date}'")
                    self.db.commit()
                except:
                    print(f"There was a battling-error for the Daily Stats.")
                    print(f"In the channel: {message.channel.name}, MSG ID: {message.id}")
            #CoinRelease
            if "released " in message.content.lower():
                coins = message.content.split("!")[0]
                coins = coins.split("<:PokeCoin:666879070650236928> **")[1]
                coins = coins.split("**")[0]
                coins = int(coins.replace(",",""))
                print(f"Release coins: {coins}")
                self.db.execute(f"UPDATE DailyStats SET CoinRelease = CoinRelease + {coins} WHERE Date = '{date}'")
                self.db.commit()
            #CoinWorldBoss
            if "here are your rewards for the " in message.content.lower():
                coins = message.content.split("PokeCoins earned: <:PokeCoin:666879070650236928> ")[1]
                coins = int(coins.split()[0].replace(",",""))
                print(f"Worldboss coins: {coins}")
                self.db.execute(f"UPDATE DailyStats SET CoinWorldBoss = CoinWorldBoss + {coins} WHERE Date = '{date}'")
                self.db.commit()
            if (len(message.embeds)>0):
                emb = message.embeds[0]
                if emb.footer:
                #TotalBattle
                    if "battle starts in" in emb.footer.text.lower():
                        self.db.execute(f"UPDATE DailyStats SET TotalBattle = TotalBattle + 1 WHERE Date = '{date}'")
                        self.db.commit()
                #CoinCatch &
                #PokeCaught
                if emb.description:
                    if "caught a" in emb.description:
                        self.db.execute(f"UPDATE DailyStats SET PokeCaught = PokeCaught+1 WHERE Date = '{date}'")
                        self.db.commit()
                        if "pokecoins" in emb.footer.text.lower():
                            coins = emb.footer.text.split("You earned ")[1]
                            coins = int((coins.split(" ")[0]).replace(",",""))
                            self.db.execute(f"UPDATE DailyStats SET CoinCatch = CoinCatch + {coins} WHERE Date = '{date}'")
                            self.db.commit()
                #CoinMarket
                if emb.title:
                    if "from all of your offers" in emb.title:
                        #print("Still calculating...")
                        coins = int(emb.title.split("**")[1].replace(",",""))
                        #print(f"Market coins: {coins}")
                        self.db.execute(f"UPDATE DailyStats SET CoinMarket = CoinMarket + {coins} WHERE Date = '{date}'")
                        self.db.commit()
                if emb.author.name:
                #EggHatch
                    if "hatched an Egg" in emb.author.name:
                        self.db.execute(f"UPDATE DailyStats SET Eggs = Eggs + 1 WHERE Date = '{date}'")
                        self.db.commit()
            
    def generate_size():
        while True:
            xy = numpy.random.normal(loc=200, scale=70)
            if 1 <= xy <= 700:
                #print(xy)
                return round(xy)
    async def eventchecker(self,message,sender):
        if message.guild.id == 825813023716540426:
            sender = await message.guild.fetch_member(sender.id)
            check = self.db.execute(f"SELECT * FROM Events WHERE Active = 1")
            check = check.fetchone()
            if check[0] == 'BiggestFish':
                asyncio.create_task(Modules.biggestfish(self, message, sender))
            elif check[0] == 'TypeHunt':
                print("TyPeHuNt")
                for role in sender.roles:
                        if role.id == 837611415070048277:
                            print("Correct role")
                            asyncio.create_task(Modules.typehunt(self, message, sender))
                
    async def typehunt(self, message, sender):
        emb = message.embeds[0]
        data = self.execute(f"SELECT * FROM Dex WHERE Img_Url = '{emb.image.url}'")
        data = data.fetchone()
        ev = self.execute(f"SELECT * FROM Events WHERE Name = 'TypeHunt'")
        ev = ev.fetchone()
        points = th_points[f'{data[14]}']
        check = self.db.execute(f"SELECT * FROM TypeHunt WHERE User_ID = {sender.id}")
        check = check.fetchone()
        if check is None:
            self.db.execute(f"INSERT INTO TypeHunt VALUES ({sender.id},1,{points}")
            self.db.commit()
        else:
            self.db.execute(f"UPDATE TypeHunt SET Amount = Amount + 1, Points = Points + {points} WHERE User_ID = {sender.id}")
            self.db.commit()
            points = points + check[2]
        appending = f"{type_emotes[f'{Modules.hunted_type}']} You earned {th_points[f'{data[14]}']} for your catch!\nYou now have {points} points!"
        embe = disnake.Embed(title="Gengars Type Hunt", description=appending,color=type_colors[f'{data[14]}'])
        embe.set_thumbnail(url=data[15])
        await message.reply(embed=embe)

        
    # BIGGEST FISH / KARP EVENT
    async def fisheventcheck(self,message,sender):
        if message.guild.id == 825813023716540426:
            sender = await message.guild.fetch_member(sender.id)
            check = self.db.execute(f"SELECT * FROM Events WHERE Name = 'BiggestFish'")
            check = check.fetchone()
            try:
                if check[1] == 1:
                    #for role in sender.roles:
                        #if role.id == 837611415070048277:
                    asyncio.create_task(Modules.biggestfish(self, message,sender))
            except Exception as e:
                print(f"Fish event check error: {sender} - {message.jump_url}\n{e}")

    async def biggestfish(self, message,sender):
        rand = random.randint(1,500)
        rand2 = random.random()
        rand3 = random.randint(0,200)
        size = int((rand*rand2)+rand3)
        size = Modules.generate_size()
        if size < 100:
            jk = f"Wow! {size/100}m! That's a tiny <:129:1210417260196270213> Magikarp!"
        elif size >= 100 and size < 300:
            jk = f"Neat! {size/100}m! That's a pretty decent size for a <:129:1210417260196270213> Magikarp!"
        elif size >= 300 and size < 500:
            jk = f"Look at that! {size/100}m! That's a pretty, pretty big <:129:1210417260196270213> Magikarp!"
        elif size >= 500:
            jk = f"... what?! {size/100}m!!! How is a <:129:1210417260196270213> Magikarp that big even possible?!"
        
        check = self.db.execute(f"SELECT * FROM BiggestFish WHERE User_ID = {sender.id}")
        check = check.fetchone()
        if check is None:
            self.db.execute(f"INSERT INTO BiggestFish VALUES ({sender.id},1,{size},{size},{size})")
            self.db.commit()
            appending = f"Your biggest <:129:1210417260196270213> Magikarp so far: {size/100}m"
        else:
            if (float(check[2])/100)>(float(size)/100): #New size smaller biggest fish
                if (float(size)/100)>(float(check[3])/100): #Bigger than smallet
                    self.db.execute(f"UPDATE BiggestFish SET Amount = Amount + 1, Avg = Avg + {size} WHERE User_ID = {sender.id}")
                    self.db.commit()
                    appending = f"Your biggest <:129:1210417260196270213> Magikarp so far: {check[2]/100}m"
                else: #Smaller than smallest
                    self.db.execute(f"UPDATE BiggestFish SET Amount = Amount + 1, Smallest = {size}, Avg = Avg + {size} WHERE User_ID = {sender.id}")
                    self.db.commit()
                    appending = f"That's your smallest  <:129:1210417260196270213> Magikarp so far: {size/100}, former personal smallest was {check[3]/100}m."
            else: #Bigger than biggest
                self.db.execute(f"UPDATE BiggestFish SET Amount = Amount + 1, Size = {size}, Avg = Avg + {size} WHERE User_ID = {sender.id}")
                self.db.commit()
                appending = f"Your biggest <:129:1210417260196270213> Magikarp so far: {size/100}m, former personal highscore was {check[2]/100}m."

        await message.reply(f"{sender.mention} - {jk}\n{appending}")

    async def fishtimer(self):
        data = self.db.execute(f"SELECT * FROM Events WHERE Active = 1")
        data = data.fetchone()
        if data == None:
            print("No Gengar event active.")
        elif data[1] == 1:
            end = data[4]
            now = int(datetime.now().timestamp())
            waiter = end-now
            print(f"Active {data[0]} Event found; gonna end in {waiter/60} minutes.")
            await asyncio.sleep(waiter)
            if data[0] == 'BiggestFish':
                asyncio.create_task(Modules.fishend(self))
            elif data[0] == 'TypeHunt':
                asyncio.create_task(Modules.typeend(self))

    async def typeend(self):
        results = self.db.execute(f"SELECT * FROM TypeHunt ORDER BY Points DESC")
        results = results.fetchall()
        events = self.db.execute(f"SELECT * FROM Events WHERE Name = 'TypeHunt'")
        events = events.fetchone()
        table = ""
        i = 0
        while i < len(results):
            if i<10:
                table += f"<@{results[i][0]}>  |  {results[i][1]}  |  {(results[i][2])}\n"
            i += 1
        emb = disnake.Embed(title="Type Hunt Leaderboard", description=f"Here are the results for the Event which started at <t:{events[3]}:f>.",color=type_colors[f'{events[5]}'])
        emb.add_field(name="Top 10:",value=f"•  Username  |  Catch Amount  |  Points  •\n{table}",inline=True)
        emb.set_footer(text="Provided by Mega Gengar.")
        channel = self.client.get_channel(825958388349272106) #Bot-Testing
        await channel.send(embed=emb)
        async with aiosqlite.connect("database.db") as db:
            async with db.execute(f"SELECT * FROM TypeHunt ORDER BY Points DESC") as cursor:
                cols = [column[0] for column in cursor.description]
                rows = await cursor.fetchall()
                df = pandas.DataFrame(rows, columns = cols)
                df.to_excel("typehunt.xlsx", index=False)
                if channel:
                    await channel.send("Here is the exported table for the last TypeHunt Event:",file=disnake.File("typehunt.xlsx"))
                os.remove("typehunt.xlsx")
                self.db.execute(f"DELETE FROM TypeHunt")
                self.db.commit()
                self.db.execute(f"UPDATE Events SET Active = 0, Runtime = 0, Start_Stamp = 0 WHERE Name = 'TypeHunt'")
                self.db.commit()

    async def fishend(self):
        results = self.db.execute(f"SELECT * FROM BiggestFish ORDER BY Size DESC")
        results = results.fetchall()
        #print(results)
        events = self.db.execute(f"SELECT * FROM Events WHERE Name = 'BiggestFish'")
        events = events.fetchone()
        table = ""
        i = 0
        while i < len(results):
            if i < 10:
                table += f"<@{results[i][0]}>  |  {results[i][1]}  |  {float(results[i][2])/100}m\n"
            i += 1
        
        emb = disnake.Embed(title="Biggest Karp Leaderboard", description=f"Here are the results for the Event which started at <t:{events[3]}:f>.",color=disnake.Color.dark_gold())
        emb.add_field(name="Top 10:",value=f"•  Username  |  Catch Amount  |  Size  •\n{table}",inline=True)
        smallest = self.db.execute(f"SELECT * FROM BiggestFish ORDER BY Smallest ASC")
        smallest = smallest.fetchall()
        small = f"<@{smallest[0][0]}>  |  {smallest[0][3]/100}m"
        emb.add_field(name="Smallest  <:129:1210417260196270213> Karp caught:",value=small,inline=True)
        emb.set_footer(text="Provided by Mega Gengar.")
        channel = self.client.get_channel(825958388349272106) #Bot-Testing
        await channel.send(embed=emb)

        async with aiosqlite.connect("database.db") as db:
            async with db.execute(f"SELECT * FROM BiggestFish ORDER BY Size DESC") as cursor:
                cols = [column[0] for column in cursor.description]
                rows = await cursor.fetchall()
                df = pandas.DataFrame(rows, columns = cols)
                df.to_excel("biggestfish.xlsx", index=False)
                if channel:
                    await channel.send("Here is the exported table for the last Big Fish Event:",file=disnake.File("biggestfish.xlsx"))
                os.remove("biggestfish.xlsx")
                self.db.execute(f"DELETE FROM BiggestFish")
                self.db.commit()
                self.db.execute(f"UPDATE Events SET Active = 0, Runtime = 0, Start_Stamp = 0 WHERE Name = 'BiggestFish'")
                self.db.commit()

    async def rare_spawn(self, message):
        print("Checking the WB message")
        current_time = datetime.utcnow()
        timestamp = current_time.strftime('%Y-%m-%d %H:%M:%S')
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
        embed.set_footer(text=(f'{self.client.user.display_name}'+" | at UTC "f'{timestamp}'), icon_url=f'{self.client.user.avatar}')
        await announce.send(embed=embed)

 
def setup(client):
    client.add_cog(Modules(client))