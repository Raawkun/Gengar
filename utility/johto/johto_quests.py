import asyncio
import datetime
import random
from sqlite3 import connect
from disnake.ext import commands
import disnake

from utility.johto.johto_checks import ChecksOfJohto
from utility.johto.travel_checks import TravelChecks

debug = connect('database.db').execute(f"SELECT Johto_Debug FROM Meow_Temps")
debug = debug.fetchone()[0]

class QuestsOfJohto(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.db = connect("database.db")

    

    async def newbark_quest(self, image, user, before):
        ticket_check = await ChecksOfJohto.travel_tickets()
        mons_needed = await ChecksOfJohto.newbark_check(debug)
        check_db = self.db.execute(f"SELECT * FROM Dex WHERE Img_url='{image}'")
        check_db = check_db.fetchone()
        db_stats = self.db.execute(f"SELECT Permit FROM Johto WHERE User_ID = {user.id}")
        db_stats = db_stats.fetchone()
        db_newbark = self.db.execute(f'SELECT Newbark_Quest FROM Johto Where User_ID = {user.id}')
        db_newbark = db_newbark.fetchone()
        current_score = db_newbark[0]
        new_perm = 1
        msg = ""
        if current_score >= mons_needed and db_stats[0] != 0:
            #print("Score is overrrrr")
            return
        elif check_db[16] == "Johto":
            if (current_score + 1) >= mons_needed:
                self.db.execute(f"UPDATE Johto SET Newbark_Quest = Newbark_Quest + 1, Permit = {new_perm},Johto_Coins = Johto_Coins + 15 WHERE User_ID = {user.id}")
                self.db.commit()
                place = list(ticket_check.keys())[list(ticket_check.values()).index(new_perm)]
                msg = f"{user.mention} Congratulations, you caught enough Johto Pokémon to help Prof Elm with his research and you now have permission to travel to {place}! You also found 15 Johto coins! <:JohtoCoin:1474149692454731818>"
                sent_msg = await before.channel.send(msg)
                await asyncio.sleep(5)
                await sent_msg.edit(content=f"{user.mention} Congrats on passing the quest!")
            else:
                self.db.execute(f"UPDATE Johto SET Newbark_Quest = Newbark_Quest + 1 WHERE User_ID = {user.id}")
                self.db.commit()
    
    async def cherrygrove_quest(self, user, before):
        ticket_check = await ChecksOfJohto.travel_tickets()
        day = datetime.datetime.today().weekday()
        if debug == 0:
            if day < 5: # Normal day rates 450
                check = 450
            else: # 5 Sat, 6 Sun.  Weekend bonus rates 350
                check = 350
        else:
            check = 5
        num = random.randint(1, check)
        shoe_emote = "<:running_shoes:1478852498633785444>"
        gear_emote= "<:pokegear:1478852583660589117>"
        db_stats = self.db.execute(f"SELECT Permit FROM Johto WHERE User_ID = {user.id}")
        db_stats = db_stats.fetchone()
        msg = ""
        new_perm = 2
        shoes_needed, pokegear_needed = await ChecksOfJohto.cherrygrove_check()
        db_pallet = self.db.execute(f'SELECT Running_Shoes, Pokegear FROM Johto Where User_ID = {user.id}')
        db_pallet = db_pallet.fetchone()
        if num == 1 and db_stats[0] == 1:
            if db_pallet[0] < shoes_needed:
                if (db_pallet[0] + 1) == shoes_needed:
                    self.db.execute(f'UPDATE Johto SET Running_Shoes = 1 WHERE User_ID = {user.id}')
                    self.db.commit()
                    msg = f"{user.mention} You found a pair of Running Shoes {shoe_emote}**!!!"
                    await before.channel.send(msg)
        if num == 2 and db_stats[0] == 1:
            if db_pallet[1] < pokegear_needed:
                if (db_pallet[1] + 1) == pokegear_needed:
                    self.db.execute(f'UPDATE Johto SET Pokegear =  1 WHERE User_ID = {user.id}')
                    self.db.commit()
                    msg = f"{user.mention} You found a brand new Pokégear {gear_emote}**!!!"
                    await before.channel.send(msg)
        db_cherry = self.db.execute(f'SELECT Running_Shoes, Pokegear FROM Johto Where User_ID = {user.id}')
        db_cherry = db_cherry.fetchone()
        if db_cherry[0] == 1 and db_cherry[1] == 1:
            place = list(ticket_check.keys())[list(ticket_check.values()).index(new_perm)]
            msg = f"{user.mention} Congratulations, you completed the Cherrygrove City quest by finding a Pokégear {gear_emote} and a pair of Running Shoes {shoe_emote}, you now have permission to travel to {place}! You also found 15 Johto coins! <:JohtoCoin:1474149692454731818>"
            sent_msg = await before.channel.send(msg)
            self.db.execute(f"UPDATE Johto SET Permit = {new_perm}, Johto_Coins = Johto_Coins + 15 WHERE User_ID = {user.id}")
            self.db.commit()
            await asyncio.sleep(5)
            await sent_msg.edit(content=f"{user.mention} Congrats on passing the quest!")

    async def violet_quest(self, image, user, before):
        ticket_check = await ChecksOfJohto.travel_tickets()
        mons_needed = await ChecksOfJohto.violet_check(debug)
        type = "grasstype"
        check_db = self.db.execute(f"SELECT * FROM Dex WHERE Img_url='{image}'")
        check_db = check_db.fetchone()
        db_stats = self.db.execute(f"SELECT Permit FROM Johto WHERE User_ID = {user.id}")
        db_stats = db_stats.fetchone()
        db_newbark = self.db.execute(f'SELECT Violet_Quest FROM Johto Where User_ID = {user.id}')
        db_newbark = db_newbark.fetchone()
        current_score = db_newbark[0]
        new_perm = 3
        msg = ""
        if current_score >= mons_needed or db_stats[0] != 2:
            return
        elif check_db[2] == type or check_db[3] == type:
            if (current_score + 1) == mons_needed:
                self.db.execute(f"UPDATE Johto SET Violet_Quest = Violet_Quest + 1, Johto_Coins = Johto_Coins + 15, Permit = {new_perm} WHERE User_ID = {user.id}")
                self.db.commit()
                place = list(ticket_check.keys())[list(ticket_check.values()).index(new_perm)]
                msg = f"{user.mention} Congratulations, you caught enough grass Pokémon to help Prof Elm with his research and you now have permission to travel to {place}! You also found 15 Johto coins! <:JohtoCoin:1474149692454731818>"
                sent_msg = await before.channel.send(msg)
                await asyncio.sleep(5)
                await sent_msg.edit(content=f"{user.mention} Congrats on passing the quest!")
            else:
                self.db.execute(f"UPDATE Johto SET Violet_Quest = Violet_Quest + 1 WHERE User_ID = {user.id}")
                self.db.commit()
                
    async def azalea_quest(self, image, user, before):
        ticket_check = await ChecksOfJohto.travel_tickets()
        mons_needed, mon_id = await ChecksOfJohto.azalea_check(debug)
        check_db = self.db.execute(f"SELECT * FROM Dex WHERE Img_url='{image}'")
        check_db = check_db.fetchone()
        db_stats = self.db.execute(f"SELECT Permit FROM Johto WHERE User_ID = {user.id}")
        db_stats = db_stats.fetchone()
        db_newbark = self.db.execute(f'SELECT Azalea_Quest FROM Johto Where User_ID = {user.id}')
        db_newbark = db_newbark.fetchone()
        current_score = db_newbark[0]
        new_perm = 4
        msg = ""
        if current_score >= mons_needed or db_stats[0] != 3:
            return
        elif check_db[0] == mon_id:
            if (current_score + 1) == mons_needed:
                self.db.execute(f"UPDATE Johto SET Azalea_Quest = Azalea_Quest + 1, Permit = {new_perm}, Johto_Coins = Johto_Coins + 15 WHERE User_ID = {user.id}")
                self.db.commit()
                place = list(ticket_check.keys())[list(ticket_check.values()).index(new_perm)]
                msg = f"{user.mention} Congratulations, you caught enough Slowpokes to help Prof Elm with his research and you now have permission to travel to {place}! You also found 15 Johto coins! <:JohtoCoin:1474149692454731818>"
                sent_msg = await before.channel.send(msg)
                await asyncio.sleep(5)
                await sent_msg.edit(content=f"{user.mention} Congrats on passing the quest!")
            else:
                self.db.execute(f"UPDATE Johto SET Azalea_Quest = Azalea_Quest + 1 WHERE User_ID = {user.id}")
                self.db.commit() 

    async def goldenrod_quest(self, user, after):
        ticket_check = await ChecksOfJohto.travel_tickets()
        coins_needed = await ChecksOfJohto.goldenrod_check()
        print(coins_needed)
        db_stats = self.db.execute(f"SELECT Permit FROM Johto WHERE User_ID = {user.id}")
        db_stats = db_stats.fetchone()
        db_newbark = self.db.execute(f'SELECT Goldenrod_Quest FROM Johto Where User_ID = {user.id}')
        db_newbark = db_newbark.fetchone()
        try:
            coins_obtained = db_newbark[0].split(",")
        except:
            print(db_newbark)
            if db_newbark[0] != None:
                coins_obtained = db_newbark[0]
            else:
                coins_obtained = []
        print(coins_obtained)
        coin_score = 0
        if len(after.embeds) > 0:
            _embed = after.embeds[0]
            if "You earned " in _embed.footer.text:
                coin_score = _embed.footer.text.split("You earned ")[1]
                coin_score = (coin_score.split(" ")[0]).replace(",", "")
                print(coin_score)
        new_perm = 5
        msg = ""
        if debug == 1:
            print("Debug mode: Goldenrod")
            coins_needed = coins_obtained.copy()
            coins_needed.append(coin_score)
            print(f"Needed: {coins_needed}")
            print(f"Obtained: {coins_obtained}")
        if (coin_score in coins_needed and coin_score in coins_obtained) or db_stats[0] != 4:
            return
        elif (coin_score in coins_needed) and (coin_score not in coins_obtained) and db_stats[0] == 4:
            coins_obtained.append(coin_score)
            print(coins_obtained)
            try:
                total = ','.join(coins_obtained)
            except:
                total = coins_obtained[0]
            print(total)
            self.db.execute(f"UPDATE Johto SET Goldenrod_Quest = '{total}' WHERE User_ID = {user.id}")
            self.db.commit()
            print(sorted(coins_obtained))
            print(sorted(coins_needed))
        if sorted(coins_obtained) == sorted(coins_needed):
            self.db.execute(f"UPDATE Johto SET Goldenrod_Quest = '{total}', Permit = {new_perm}, Johto_Coins = Johto_Coins + 15 WHERE User_ID = {user.id}")
            self.db.commit()
            place = list(ticket_check.keys())[list(ticket_check.values()).index(new_perm)]
            msg = f"{user.mention} Congratulations, you hit the final jackpot with that catch and you now have permission to travel to {place}! You also found 15 Johto coins! <:JohtoCoin:1474149692454731818>"
            sent_msg = await after.channel.send(msg)
            await asyncio.sleep(5)
            await sent_msg.edit(content=f"{user.mention} Congrats on passing the quest!")

    async def ecruteak_quest(self, image, user, before):
        ticket_check = await ChecksOfJohto.travel_tickets()
        mons_needed = await ChecksOfJohto.ecruteak_check(debug)
        type = "firetype"
        check_db = self.db.execute(f"SELECT * FROM Dex WHERE Img_url='{image}'")
        check_db = check_db.fetchone()
        db_stats = self.db.execute(f"SELECT Permit FROM Johto WHERE User_ID = {user.id}")
        db_stats = db_stats.fetchone()
        db_newbark = self.db.execute(f'SELECT Ecruteak_Quest FROM Johto Where User_ID = {user.id}')
        db_newbark = db_newbark.fetchone()
        current_score = db_newbark[0]
        new_perm = 6
        msg = ""
        print(f"{check_db[2]}|{check_db[3]}")
        if current_score >= mons_needed or db_stats[0] != 5:
            return
        elif check_db[2] == type or check_db[3] == type:
            if (current_score + 1) >= mons_needed:
                self.db.execute(f"UPDATE Johto SET Ecruteak_Quest = Ecruteak_Quest + 1, Permit = {new_perm}, Johto_Coins = Johto_Coins + 15 WHERE User_ID = {user.id}")
                self.db.commit()
                place = list(ticket_check.keys())[list(ticket_check.values()).index(new_perm)]
                msg = f"{user.mention} Congratulations, you caught enough fire Pokémon to help Prof Elm with his research and you now have permission to travel to {place}! You also found 15 Johto coins! <:JohtoCoin:1474149692454731818>"
                sent_msg = await before.channel.send(msg)
                await asyncio.sleep(5)
                await sent_msg.edit(content=f"{user.mention} Congrats on passing the quest!")
            else:
                self.db.execute(f"UPDATE Johto SET Ecruteak_Quest = Ecruteak_Quest + 1 WHERE User_ID = {user.id}")
                self.db.commit()

    async def olivine_quest(self, image, user, before):
        ticket_check = await ChecksOfJohto.travel_tickets()
        mons_needed = await ChecksOfJohto.olivine_check(debug)
        type = "electrictype"
        check_db = self.db.execute(f"SELECT * FROM Dex WHERE Img_url='{image}'")
        check_db = check_db.fetchone()
        db_stats = self.db.execute(f"SELECT Permit FROM Johto WHERE User_ID = {user.id}")
        db_stats = db_stats.fetchone()
        db_newbark = self.db.execute(f'SELECT Olivine_Quest FROM Johto Where User_ID = {user.id}')
        db_newbark = db_newbark.fetchone()
        current_score = db_newbark[0]
        new_perm = 7
        msg = ""
        if current_score >= mons_needed or db_stats[0] != 6:
            return
        elif check_db[2] == type or check_db[3] == type:
            if (current_score + 1) == mons_needed:
                self.db.execute(f"UPDATE Johto SET Olivine_Quest = Olivine_Quest + 1, Permit = {new_perm}, Johto_Coins = Johto_Coins + 15 WHERE User_ID = {user.id}")
                self.db.commit()
                place = list(ticket_check.keys())[list(ticket_check.values()).index(new_perm)]
                msg = f"{user.mention} Congratulations, you caught enough electric Pokémon to help power the city again and you now have permission to travel to {place}! You also found 15 Johto coins! <:JohtoCoin:1474149692454731818>"
                sent_msg = await before.channel.send(msg)
                await asyncio.sleep(5)
                await sent_msg.edit(content=f"{user.mention} Congrats on passing the quest!")
            else:
                self.db.execute(f"UPDATE Johto SET Olivine_Quest = Olivine_Quest + 1 WHERE User_ID = {user.id}")
                self.db.commit()

    async def cianwood_quest(self, image, user, before):
        safari_mons, mons_needed = await ChecksOfJohto.cianwood_check(debug)
        ticket_check = await ChecksOfJohto.travel_tickets()
        check_db = self.db.execute(f"SELECT * FROM Dex WHERE Img_url='{image}'")
        check_db = check_db.fetchone()
        db_pallet = self.db.execute(f'SELECT Permit FROM Johto Where User_ID = {user.id}')
        db_pallet = db_pallet.fetchone()
        db_quest = self.db.execute(f"SELECT Cianwood_Quest FROM Johto WHERE User_ID = {user.id}")
        db_quest = db_quest.fetchone()
        current_score = db_quest[0]
        new_perm = 8
        msg = ""
        if check_db[0] in safari_mons:
            if debug == 1:
                await before.reply("Thats one we need")
            if (current_score+1) > mons_needed or db_pallet[0] != 7:
                return
            elif check_db[0] in safari_mons:
                if (current_score+1) == mons_needed:
                    self.db.execute(f"UPDATE Johto SET Cianwood_Quest = Cianwood_Quest + 1, Permit = {new_perm}, Johto_Coins = Johto_Coins + 15 WHERE User_ID = {user.id}")
                    self.db.commit()
                    place = list(ticket_check.keys())[list(ticket_check.values()).index(new_perm)]
                    msg = f"{user.mention} Congratulations, you caught enough safari pokémon to help Prof Elm with his research and you now have permission to travel to {place}! You also found 15 Johto coins! <:JohtoCoin:1474149692454731818>"
                    sent_msg = await before.channel.send(msg)
                    await asyncio.sleep(5)
                    await sent_msg.edit(content=f"{user.mention} Congrats on passing the quest!")
                else:
                    self.db.execute(f"UPDATE Johto SET Cianwood_Quest = Cianwood_Quest + 1 WHERE User_ID = {user.id}")
                    self.db.commit()
        else:
            return
        

    async def mahogany_quest(self, image, user, before):
        ticket_check = await ChecksOfJohto.travel_tickets()
        mons_needed = await ChecksOfJohto.mahogany_check(debug)
        type = "icetype"
        check_db = self.db.execute(f"SELECT * FROM Dex WHERE Img_url='{image}'")
        check_db = check_db.fetchone()
        db_stats = self.db.execute(f"SELECT Permit FROM Johto WHERE User_ID = {user.id}")
        db_stats = db_stats.fetchone()
        db_newbark = self.db.execute(f'SELECT Mahogany_Quest FROM Johto Where User_ID = {user.id}')
        db_newbark = db_newbark.fetchone()
        current_score = db_newbark[0]
        new_perm = 9
        msg = ""
        if current_score >= mons_needed or db_stats[0] != 8:
            return
        elif check_db[2] == type or check_db[3] == type:
            if (current_score + 1) == mons_needed:
                self.db.execute(f"UPDATE Johto SET Mahogany_Quest = Mahogany_Quest + 1, Permit = {new_perm}, Johto_Coins = Johto_Coins + 15 WHERE User_ID = {user.id}")
                self.db.commit()
                place = list(ticket_check.keys())[list(ticket_check.values()).index(new_perm)]
                #NEEDS UPDATE
                msg = f"{user.mention} Congratulations, you caught enough ice Pokémon to help Leader Pryce and you now have permission to travel to {place}! You also found 15 Johto coins! <:JohtoCoin:1474149692454731818>"
                sent_msg = await before.channel.send(msg)
                await asyncio.sleep(5)
                await sent_msg.edit(content=f"{user.mention} Congrats on passing the quest!")
            else:
                self.db.execute(f"UPDATE Johto SET Mahogany_Quest = Mahogany_Quest + 1 WHERE User_ID = {user.id}")
                self.db.commit()

    async def blackthorn_quest(self, user, after):
        ticket_check = await ChecksOfJohto.travel_tickets()
        items_needed, boosted = await ChecksOfJohto.blackthorn_check(debug)
        db_stats = self.db.execute(f"SELECT Permit FROM Johto WHERE User_ID = {user.id}")
        db_stats = db_stats.fetchone()
        db_newbark = self.db.execute(f'SELECT Blackthorn_Quest FROM Johto Where User_ID = {user.id}')
        db_newbark = db_newbark.fetchone()
        current_score = db_newbark[0]
        new_perm = 10
        _embed = after.embeds[0]
        if after.embeds != []:
            print(_embed.description)
            item = _embed.description.split("retrieved")[1]
            item = item.split("**")[1]
            print(item)
            if debug == 1:
                boosted = []
                boosted.append(item)
                probt(boosted)
            if item not in boosted or current_score >= items_needed or db_stats != 9:
                return
            elif item in boosted:
                print('item is in boosted')
                if (current_score + 1) == items_needed:
                    self.db.execute(f"UPDATE Johto SET Blackthorn_Quest = Blackthorn_Quest + 1, Permit = {new_perm}, Johto_Coins = Johto_Coins + 15, Ticket = {new_perm} WHERE User_ID = {user.id}")
                    self.db.commit()
                    msg = f"{user.mention} Congratulations, you managed to grab {items_needed} type boosting Items and have finished your Johto Quest!!  Unless there's secret quests you can do..? You also found 15 Johto coins! <:JohtoCoin:1474149692454731818>"
                    sent_msg = await after.channel.send(msg)
                    await asyncio.sleep(5)
                    await sent_msg.edit(content=f"{user.mention} Congrats on passing the quest!")
                else:
                    self.db.execute(f"UPDATE Johto SET Blackthorn_Quest = Blackthorn_Quest + 1 WHERE User_ID = {user.id}")
                    self.db.commit()

    async def secret_quest_1(self, image, user, before): #Celebi Quest
        ticket_check = await ChecksOfJohto.travel_tickets()
        mon_id, mons_needed = await ChecksOfJohto.secret_1_check()
        db_celebi = self.db.execute(f"SELECT Secret_1 FROM Johto WHERE User_ID = {user.id}")
        db_celebi = db_celebi.fetchone()
        if db_celebi[0] == 1:
            return
        else:
            data = self.db.execute(f"SELECT * FROM Dex WHERE Img_Url = '{image}'")
            data = data.fetchone()
            if data[11] == 1:
                name = data[1].split("Shiny ")[1]
                data = self.db.execute(f"SELECT * FROM Dex WHERE Name = '{name}'")
                data = data.fetchone()
            if data[0] in mon_id:
                guild = user.guild
                Cele_Hunter = disnake.utils.get(guild.roles, name="Celebi Hunter")
                self.db.execute(f"UPDATE Johto SET Secret_1 = 1, Johto_Coins = Johto_Coins + 100 WHERE User_ID = {user.id}")
                self.db.commit()
                await user.add_roles(Cele_Hunter)
                msg = "You placed the GS Ball into the shrine within Ilex Forest and found the mythical Celebi! You are awarded 100 Johto Coins <:JohtoCoin:1474149692454731818>!"
                emb = disnake.Embed(description=msg, color=disnake.Colour.brand_green(),title="Ancient Shrine")
                emb.set_image(url="https://github.com/Raawkun/Discord-Bot-Files/blob/main/pics/HGSS_Ilex_Forest-Night.png")
                await before.channel.send(content=f"{user.mention}",embed=emb,delete_after=10)

    async def secret_quest_2(self, image, user, before): #Legendaries
        mon_ids, mons_needed = await ChecksOfJohto.secret_2_check()
        db_mons = self.db.execute(f"SELECT Secret_2, Secret_Quest_2 FROM Johto WHERE User_ID = {user.id}")
        db_mons = db_mons.fetchone()
        data = self.db.execute(f"SELECT * FROM Dex WHERE Img_Url = '{image}'")
        data = data.fetchone()
        if data[11] == 1: #If shiny, convert to non-shiny version
            name = data[1].split("Shiny ")[1]
            data = self.db.execute(f"SELECT * FROM Dex WHERE Name = '{name}'")
            data = data.fetchone()
        #print(data[0])
        if data[0] not in mon_ids: #Check if the mon is one of the legendaries
            return
        else: #Its a Johto Legendary, so lets check further
            user_list = db_mons[1].split(",")
            if len(user_list) == len(mons_needed): #Are we already done???
                return
            else:
                if data[0] in user_list: #Did we already catch it?
                    return
                else:
                    mon_ids.append(data[0]).sort()
                    user_list_new = ",".join(mon_ids)
                    if mon_ids == mons_needed:
                        self.db.execute(f"UPDATE Johto SET Secret_2 = 1, Secret_Quest_2 = '{user_list_new}', Johto_Coins = Johto_Coins + 100 WHERE User_ID = {user.id}")
                        self.db.commit()
                        guild = user.guild
                        Johto_dex = disnake.utils.get(guild.roles, "Johto Dexxer")
                        try:
                            await user.add_roles(Johto_dex)
                        except:
                            print(f"Couldnt add {Johto_dex.name()} to {user.display_name()}.")
                        msg = "Wow! You managed to catch all Johto's legendaries! That's impressive! Here, take 100 Johto Coins <:JohtoCoin:1474149692454731818> for your effort!"
                        emb = disnake.Embed(description=msg, color=disnake.Colour.brand_green(),title="Legendary Catcher")
                        await before.channel.send(content=f"{user.mention}", embed=emb, delete_after=10)
                    else:
                        self.db.execute(f"UPDATE Johto SET Secret_Quest_2 = '{user_list_new}' WHERE User_ID = {user.id}")
                        self.db.commit()







    async def johto_coins(self, user, before, coin_type):
        hunt_coinodds, fish_coinodds, battle_coinodds = await ChecksOfJohto.coin_check(debug)
        item_database = self.db.execute(f"SELECT * FROM Johto WHERE User_ID = '{user.id}' ")
        item_database = item_database.fetchall()
        bonus_city = None
        bonus_increase = 5
        if item_database:
            amulet_count = item_database[0][20]
        else:
            amulet_count = 0
        locations = await TravelChecks.travel_locations()
        day = datetime.datetime.today().weekday()
        hunt_coinodds = 1 / (hunt_coinodds * (1 - (0.01 * amulet_count)))
        fish_coinodds = 1 / (fish_coinodds * (1 - (0.01 * amulet_count)))
        battle_coinodds = 1 / (battle_coinodds * (1 - (0.01 * amulet_count)))
        # hunt_coinodds = ((1/hunt_coinodds) * (1 + (0.01 * amulet_count)))
        # fish_coinodds = ((1/fish_coinodds) * (1 + (0.01 * amulet_count)))
        # battle_coinodds = ((1/battle_coinodds) * (1 + (0.01 * amulet_count)))
        odds = 0
        if coin_type == "hunt":
            odds = hunt_coinodds
        elif coin_type == "fish":
            odds = fish_coinodds
        elif coin_type == "battle":
            odds = battle_coinodds
        roll = random.random()
        if bonus_city:
            if before.channel.id in locations["Viridian City"]:
                odds = int(odds * (1 + (bonus_increase/100)))
        if odds > roll:
            if day < 5: # Normal weekday rates
                multi_coin = 100
            else: # 5 Sat, 6 Sun.  Weekend bonus rates
                multi_coin = 95
            coin_emote = "<:JohtoCoin:1474149692454731818>"

            # multi_coin = ((1/multi_coin) * (1 + (0.01 * amulet_count)))
            multi_coin = 1 / (multi_coin * (1 - (0.01 * amulet_count)))
            # if before.channel.id in locations["Viridian City"]:
                # multi_coin = int(multi_coin * 1.1)

            msg = ""
            roll = random.random()
            if multi_coin > roll:
                chance = 1/100 * (1 + (0.01 * amulet_count))
                roll2 = random.random()
                if chance > roll2:
                    self.db.execute(f"UPDATE Johto SET Johto_Coins = Johto_Coins + 5 WHERE User_ID = {user.id}")
                    self.db.commit()
                    msg = f"{user.mention} Congratulations, you found five Johto Coins! {coin_emote * 5}"
                else:
                    self.db.execute(f"UPDATE Johto SET Johto_Coins = Johto_Coins + 2 WHERE User_ID = {user.id}")
                    self.db.commit()
                    msg = f"{user.mention} Congratulations, you found two Johto Coins! {coin_emote * 2}"
            else:
                self.db.execute(f"UPDATE Johto SET Johto_Coins = Johto_Coins + 1 WHERE User_ID = {user.id}")
                self.db.commit()
                msg = f"{user.mention} Congratulations, you found a Johto Coin! {coin_emote}"
            if msg:
                await before.channel.send(msg)
             

def setup(client):
    client.add_cog(QuestsOfJohto(client))