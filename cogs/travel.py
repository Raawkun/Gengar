import disnake
from disnake.ext import commands
from disnake import Option, OptionChoice, OptionType, ApplicationCommandInteraction
import asyncio
import math
import datetime
import json
from sqlite3 import connect
from utility.johto.johto_checks import ChecksOfJohto
from utility.johto.mon_cmd import Mon_Cmd
from utility.info_dict import regions
from utility.embed import Custom_embed
# from utility.cogs.promo_check import Promo_check_odds
from utility.johto.johto_quests import QuestsOfJohto
from utility.johto.travel_checks import TravelChecks
import requests
from io import BytesIO
import os
from utility.all_checks import Basic_checker
import json

import sys

if sys.version_info < (3, 7):
    import typing_extensions as typing
else:
    import typing


class Starter_buttons(disnake.ui.View):
    def __init__(self, ctx, mon, client, **kwargs):
        super().__init__(**kwargs, timeout=None)
        self.ctx = ctx
        self.db = connect("database.db")
        self.client = client
        self.mon = mon

    @disnake.ui.button(emoji='<:chikorita:1466201537326878772>', row=0)
    async def _bulb_button(self, button, ctx):
        await ctx.response.defer()
        self.mon = 152
        await Role_menu._starterselect(self, ctx = self.ctx, mon = self.mon, client = self.client)

    @disnake.ui.button(emoji='<:cyndaquil:1466201550367096924>', row=0)
    async def _char_button(self, button, ctx):
        await ctx.response.defer()
        self.mon = 155
        await Role_menu._starterselect(self, ctx = self.ctx, mon = self.mon, client = self.client)

    @disnake.ui.button(emoji='<:totodile:1466201564531261482>', row=0)
    async def _squir_button(self, button, ctx):
        await ctx.response.defer()
        self.mon = 158
        await Role_menu._starterselect(self, ctx = self.ctx, mon = self.mon, client = self.client)

    @disnake.ui.button(emoji='<:pikachu:1230997848812683266>', row=0)
    async def _pika_button(self, button, ctx):
        await ctx.response.defer()
        self.mon = 25
        await Role_menu._starterselect(self, ctx = self.ctx, mon = self.mon, client = self.client)

    @disnake.ui.button(emoji='<:eevee:1230997790159536159>', row=0)
    async def _eevee_button(self, button, ctx):
        await ctx.response.defer()
        self.mon = 133
        await Role_menu._starterselect(self, ctx = self.ctx, mon = self.mon, client = self.client)

    async def interaction_check(self, interaction: disnake.Interaction):
        if self.ctx.author.id != interaction.user.id:
            return await interaction.response.send_message(content = f"Use your own command", ephemeral = True)

        return True

class Travel_buttons(disnake.ui.View):
    def __init__(self, ctx, role, ticket, client, **kwargs):
        super().__init__(**kwargs, timeout=None)
        self.ctx = ctx
        self.role = role
        self.ticket = ticket
        self.client = client
        self.db = connect("database.db")

        if self.role == "New Bark Town":
            self._new_bark_town.disabled = True
        if self.role == "Cherrygrove City":
            self._cherrygrove_city.disabled = True
        if self.role == "Violet City":
            self._violet_city.disabled = True
        if self.role == "Azalea Town":
            self._azalea_town.disabled = True
        if self.role == "Goldenrod City":
            self._goldenrod_city.disabled = True
        if self.role == "Ecruteak City":
            self._ecruteak_city.disabled = True
        if self.role == "Olivine City":
            self._olivine_city.disabled = True
        if self.role == "Cianwood City":
            self._cianwood_city.disabled = True
        if self.role == "Mahogany Town":
            self._mahogany_town.disabled = True
        if self.role == "Blackthorn City":
            self._blackthorn_city.disabled = True
        

        if self.ticket < 1:
            self._cherrygrove_city.disabled = True
            self._violet_city.disabled = True
            self._azalea_town.disabled = True
            self._goldenrod_city.disabled = True
            self._ecruteak_city.disabled = True
            self._olivine_city.disabled = True
            self._cianwood_city.disabled = True
            self._mahogany_town.disabled = True
            self._blackthorn_city.disabled = True
        if self.ticket < 2:
            self._violet_city.disabled = True
            self._azalea_town.disabled = True
            self._goldenrod_city.disabled = True
            self._ecruteak_city.disabled = True
            self._olivine_city.disabled = True
            self._cianwood_city.disabled = True
            self._mahogany_town.disabled = True
            self._blackthorn_city.disabled = True
        if self.ticket < 3:
            self._azalea_town.disabled = True
            self._goldenrod_city.disabled = True
            self._ecruteak_city.disabled = True
            self._olivine_city.disabled = True
            self._cianwood_city.disabled = True
            self._mahogany_town.disabled = True
            self._blackthorn_city.disabled = True
        if self.ticket < 4:
            self._goldenrod_city.disabled = True
            self._ecruteak_city.disabled = True
            self._olivine_city.disabled = True
            self._cianwood_city.disabled = True
            self._mahogany_town.disabled = True
            self._blackthorn_city.disabled = True
        if self.ticket < 5:
            self._ecruteak_city.disabled = True
            self._olivine_city.disabled = True
            self._cianwood_city.disabled = True
            self._mahogany_town.disabled = True
            self._blackthorn_city.disabled = True
        if self.ticket < 6:
            self._olivine_city.disabled = True
            self._cianwood_city.disabled = True
            self._mahogany_town.disabled = True
            self._blackthorn_city.disabled = True
        if self.ticket < 7:
            self._cianwood_city.disabled = True
            self._mahogany_town.disabled = True
            self._blackthorn_city.disabled = True
        if self.ticket < 8:
            self._mahogany_town.disabled = True
            self._blackthorn_city.disabled = True
        if self.ticket < 9:
            self._blackthorn_city.disabled = True

    @disnake.ui.button(label='New Bark Town', row=0)
    async def _new_bark_town(self, button, ctx):
        await ctx.response.defer()
        self.role = 'New Bark Town'
        await Role_menu._roleselect(self, ctx = self.ctx, role = self.role, ticket = self.ticket, client = self.client)

    @disnake.ui.button(label='Cherrygrove City', row=0)
    async def _cherrygrove_city(self, button, ctx):
        await ctx.response.defer()
        self.role = 'Cherrygrove City'
        await Role_menu._roleselect(self, ctx = self.ctx, role = self.role, ticket = self.ticket, client = self.client)

    @disnake.ui.button(label='Violet City', row=0)
    async def _violet_city(self, button, ctx):
        await ctx.response.defer()
        self.role = 'Violet City'
        await Role_menu._roleselect(self, ctx = self.ctx, role = self.role, ticket = self.ticket, client = self.client)

    @disnake.ui.button(label='Azalea Town', row=0)
    async def _azalea_town(self, button, ctx):
        await ctx.response.defer()
        self.role = 'Azalea Town'
        await Role_menu._roleselect(self, ctx = self.ctx, role = self.role, ticket = self.ticket, client = self.client)

    @disnake.ui.button(label='Goldenrod City', row=1)
    async def _goldenrod_city(self, button, ctx):
        await ctx.response.defer()
        self.role = 'Goldenrod City'
        await Role_menu._roleselect(self, ctx = self.ctx, role = self.role, ticket = self.ticket, client = self.client)

    @disnake.ui.button(label='Ecruteak City', row=1)
    async def _ecruteak_city(self, button, ctx):
        await ctx.response.defer()
        self.role = 'Ecruteak City'
        await Role_menu._roleselect(self, ctx = self.ctx, role = self.role, ticket = self.ticket, client = self.client)

    @disnake.ui.button(label='Olivine City', row=1)
    async def _olivine_city(self, button, ctx):
        await ctx.response.defer()
        self.role = 'Olivine City'
        await Role_menu._roleselect(self, ctx = self.ctx, role = self.role, ticket = self.ticket, client = self.client)

    @disnake.ui.button(label='Cianwood City', row=1)
    async def _cianwood_city(self, button, ctx):
        await ctx.response.defer()
        self.role = 'Cianwood City'
        await Role_menu._roleselect(self, ctx = self.ctx, role = self.role, ticket = self.ticket, client = self.client)

    @disnake.ui.button(label='Mahogany Town', row=2)
    async def _mahogany_town(self, button, ctx):
        await ctx.response.defer()
        self.role = 'Mahogany Town'
        await Role_menu._roleselect(self, ctx = self.ctx, role = self.role, ticket = self.ticket, client = self.client)

    @disnake.ui.button(label='Blackthorn City', row=2)
    async def _blackthorn_city(self, button, ctx):
        await ctx.response.defer()
        self.role = 'Blackthorn City'
        await Role_menu._roleselect(self, ctx = self.ctx, role = self.role, ticket = self.ticket, client = self.client)

    async def interaction_check(self, interaction: disnake.Interaction):
        if self.ctx.author.id != interaction.user.id:
            return await interaction.response.send_message(content = f"Use your own command to travel", ephemeral = True)

        return True

class Role_menu(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.db = connect("database.db")
    
    async def _roleselect(self, ctx, role, ticket, client):
        category_name = ctx.channel.category.name
        # channel_location = channel_name.split("-")[0].split("丨")[1]
        category_location = category_name.split(" ")[0].lower()
        # roles = await ChecksOfJohto.travel_roles()
        roles, tickets, region_id = await TravelChecks.check_gather(category_location)
        embed = await Custom_embed(
                    client, title = f"{category_location.title()} Station", description = f"""Welcome to {category_location.title()} Station! Please select your destination using the buttons below.
                    
For more information use:
</info:1080872068012326932> -> `kanto`"""
                ).setup_embed()
        embed.set_image(url = "https://raw.githubusercontent.com/Pr1nc3St4r/ff_images/main/misc/poke_train.gif")
        msg = ""
        member = ctx.guild.get_member(ctx.user.id)
        #print(role)
        #print(ticket)
        button_role = disnake.utils.get(ctx.guild.roles, name=role)
        #print(button_role)
        # roles = await ChecksOfJohto.travel_roles()
        # ticket_check = await ChecksOfJohto.travel_tickets()
        if role:
            #button_role = disnake.utils.get(ctx.guild.roles, name=role)
            if button_role in member.roles:
                msg = f"You are currently in **{role}**!"
                #print(msg)
            else:
                # database = self.db.execute(f"SELECT * FROM Travel WHERE User_ID = '{member.id}' ")
                # database = database.fetchall()
                database = self.db.execute(f"SELECT * FROM Johto WHERE User_ID = '{member.id}' ")
                database = database.fetchone()
                ticket = database[3]
                #print(tickets[role])
                #print(strings)
                #progress = json.loads(strings)
                #print("Button role wasnt in Member Roles")
                if database:
                    # ticket = database[0][2]
                    # ticket = progress[category_location]["ticket"]
                    if ticket >= tickets[role]: #if current ticket is higher or equal the ticket of the pressed Button
                        #print(roles)
                        for r in roles:
                            #print(r)
                            remove = disnake.utils.get(ctx.guild.roles, name=r)
                            #print(remove)
                            if remove in member.roles:
                                #print(remove)
                                # remove = interaction.guild.get_role(r)
                                await member.remove_roles(remove)
                                msg = f"{member.display_name} travelled to **{role}**!"
                        await member.add_roles(button_role)
                        await ctx.edit_original_message(content = msg, embed = None, view = None)
                        return
                    else:
                        msg = f"You don't yet have permission to travel to **{role}**!"
                # else:
                #     self.db.execute(f'INSERT INTO Travel (user_id, name) VALUES ({member.id}, "{member.name}")')
                #     self.db.commit()
                #     permit = 0
                #     if permit_check[role] >= permit:
                #         for r in roles:
                #             if r != role:
                #                 remove = disnake.utils.get(ctx.guild.roles, name=r)
                #                 # remove = interaction.guild.get_role(r)
                #                 await member.remove_roles(remove)
                #                 msg = f"{member.name} travelled to **{role}**!"
                #         await member.add_roles(button_role)
                #         await ctx.edit_original_message(content = msg, embed = None, view = None)
                #         return
                #     else:
                #         msg = f"You don't yet have permission to travel to **{role}**!"
        else:
            for r in roles:
                if disnake.utils.get(ctx.guild.roles, name=r) in member.roles:
                    role = disnake.utils.get(ctx.guild.roles, name=r)
                    # roles_to_remove = [button['role'] for button in buttons if button['role'] != custom_id]
        await ctx.edit_original_message(content = msg, embed = embed, view=Travel_buttons(ctx, role, ticket, client))

    async def _starterselect(self, ctx, mon, client):
        log = self.client.get_channel(1228642827530010624)
        embed = await Custom_embed(
                self.client, title = f"Johto", description = f"""Welcome to Johto! Please select your starter mon so your adventure can begin!"""
            ).setup_embed()
        embed.set_image(url = "https://raw.githubusercontent.com/Pr1nc3St4r/ff_images/main/misc/prof_oak.gif")
        member = ctx.guild.get_member(ctx.user.id)
        if mon is None:
            await ctx.edit_original_message(embed = embed, view=Starter_buttons(ctx, mon, client))
        else:
            # self.db.execute(f'INSERT INTO Travel (User_id, name, Pallet_Mon) VALUES ({member.id}, "{member.name}", {mon})')
            # self.db.commit()
            self.db.execute(f'INSERT INTO Johto (User_ID, Name, Ticket, Permit, Johto_Mon) VALUES ({member.id}, "{member.name}", 0, 0, {mon})')
            self.db.commit()
            check_db = self.db.execute(f"SELECT * FROM Dex WHERE DexID={mon}")
            check_db = check_db.fetchall()
            role = disnake.utils.get(ctx.guild.roles, name="New Bark Town")
            await member.add_roles(role)
            filename = os.path.basename(check_db[0][15])
            msg = f"""Welcome to the Johto Region! Your journey begins in <#1211070035729322024> with {check_db[0][1]}!
Have fun hunting, you will soon be able to travel further afield!"""
            emb = disnake.Embed(description=msg,color=disnake.Colour.brand_green())
            emb.set_image(check_db[0][15])
            await ctx.edit_original_message(content=None, embed = emb, view=None)
            return

    #async def check_travel_channel(ctx):
        #locations = await ChecksOfJohto.travel_locations()
        #for location, numbers in locations.items():
            #if ctx.channel.id in numbers:
                #return(True)
            #else:
                #await ctx.send("This command only works in the Johto region, you have no phone reception here", ephemeral=True)
                #return(False)

    async def oak_comment(self, score):
        bar_full = "<:bar_full:1123545047825141772>"
        bar_empty = "<:bar_empty:1123545044926865508>"
        msg = ""
        # if score < 0.25:
        #     msg = "*You've only just begun your current task, keep at it!*"
        # elif score < 0.5:
        #     msg = "*You're making good progress on your current task, great work!*"
        # elif score < 0.75:
        #     msg = "*Wow, you're over half way through your current task, amazing!*"
        # else:
        #     msg = "*The last push now, keep at it!*"
        full_score = int(score * 10)
        empty_score = 10 - full_score
        msg += f"__**Progress Bar**__\n\n{bar_full * full_score}{bar_empty * empty_score}"
        return msg

    @commands.Cog.listener()
    async def on_slash_command_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            return
        raise error

    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            return
        raise error

    # @commands.command()
    # async def travel_db(self, ctx):
    #     # default = '{"kanto" : {"permission" : 0, "ticket" : 0, "new_bark_town" : 0, "cherrygrove_city" : 0, "violet_city" : "{}", "azalea_town" : 0, "goldenrod_city" : 0, "ecruteak_city" : 0, "olivine_city" : 0, "cianwood_city" : 0, "mahogany_town" : 0, "secret_quest_1" : 0, "secret_quest_2" : "{}"}}'
    #     # default_escaped = default.replace('"', '""')
    #     # self.db.execute(f'''
    #     #                 CREATE TABLE IF NOT EXISTS Travel_test (
    #     #                     Ref INTEGER AUTO_INCREMENT PRIMARY KEY,
    #     #                     User_ID INTEGER,
    #     #                     Progress TEXT DEFAULT "{default_escaped}"
    #     #                     )
    #     #                 ''')
    #     # Delete all rows from the table
    #     self.db.execute("DELETE FROM Travel_test")
    #     self.db.commit()
        
    #     # Change the default value of the Progress column
    #     default = '{"kanto" : {"permission" : 0, "ticket" : 0, "new_bark_town" : 0, "cherrygrove_city" : 0, "violet_city" : "{}", "azalea_town" : 0, "goldenrod_city" : 0, "ecruteak_city" : 0, "olivine_city" : 0, "cianwood_city" : 0, "mahogany_town" : 0, "secret_quest_1" : 0, "secret_quest_2" : "{}"}}'
    #     default_escaped = default.replace('"', '\\"')
    #     self.db.execute(f"ALTER TABLE Travel_test ALTER COLUMN Progress SET DEFAULT '{default_escaped}'")
    #     # self.db.commit()
        

    #     self.db.execute(f'INSERT INTO Travel_test (User_ID) VALUES ({ctx.author.id})')
    #     self.db.commit()
    #     await ctx.send("Done")

    @commands.command()
    async def travel_db(self, ctx):
        # Delete all rows from the table
        self.db.execute("DELETE FROM Travel_test")
        self.db.commit()
        
        # Drop the existing table
        self.db.execute("DROP TABLE IF EXISTS Travel_test_old")
        self.db.commit()
        
        # Create a new table with the desired default value
        default = '{"kanto" : {"permission" : 0, "ticket" : 0, "new_bark_town" : 0, "cherrygrove_city" : 0, "violet_city" : "{}", "azalea_town" : 0, "goldenrod_city" : 0, "ecruteak_city" : 0, "olivine_city" : 0, "cianwood_city" : 0, "mahogany_town" : 0, "secret_quest_1" : 0, "secret_quest_2" : "{}"}}'
        self.db.execute(f'''
                        CREATE TABLE IF NOT EXISTS Travel_test_new (
                            Ref INTEGER AUTO_INCREMENT PRIMARY KEY,
                            User_ID INTEGER,
                            Progress TEXT DEFAULT '{default}'
                        )
                    ''')
        self.db.commit()
        
        # Copy data from old table to new table
        self.db.execute("INSERT INTO Travel_test_new (User_ID, Progress) SELECT User_ID, Progress FROM Travel_test")
        self.db.commit()
        
        # Drop the old table
        self.db.execute("DROP TABLE IF EXISTS Travel_test")
        self.db.commit()
        
        # Rename the new table to the original table name
        self.db.execute("ALTER TABLE Travel_test_new RENAME TO Travel_test")
        self.db.commit()

        # Insert data into the new table
        self.db.execute(f'INSERT INTO Travel_test (User_ID) VALUES ({ctx.author.id})')
        self.db.commit()
        
        await ctx.send("Done")

    @commands.check(Basic_checker().check_station_channel)
    # @commands.has_role("Management")
    @commands.slash_command(
        name="travel",
        description="Use this to travel around Johto!")
    async def _menu_main(self, ctx):
        # print("Travel called")
        try:
            await ctx.response.defer()
            category_name = ctx.channel.category.name
            # channel_location = channel_name.split("-")[0].split("丨")[1]
            category_location = category_name.split(" ")[0].lower()
            #print(category_location)
            # roles = await ChecksOfJohto.travel_roles()
            roles, tickets, region_id = await TravelChecks.check_gather(category_location)
            # database = self.db.execute(f"SELECT * FROM Travel WHERE User_ID = '{ctx.author.id}' ")
            database = self.db.execute(f"SELECT * FROM Johto WHERE User_ID = {ctx.author.id}")
            database = database.fetchone()
            print(database)
            role = ""
            if database:
                ticket = database[3]
                # ticket = progress[channel_location]["ticket"]
                # print(f"Ticket: {ticket}")
                for r in roles:
                    check = disnake.utils.get(ctx.guild.roles, name=r)
                    if check in ctx.author.roles:
                        role = r
                client = self.client
                await self._roleselect(ctx, role, ticket, client)
            else:
                mon = None
                client = self.client
                await self._starterselect(ctx, mon, client)
                # member = ctx.guild.get_member(ctx.user.id)
                # self.db.execute(f'INSERT INTO Travel (User_id, name) VALUES ({member.id}, "{member.name}")')
                # self.db.commit()
                # ticket = 0
                # role = disnake.utils.get(ctx.guild.roles, name="Pallet Town")
                # await member.add_roles(role)
                # await ctx.send("Welcome to the Johto Region! Your journey begins in Pallet Town")
                # return
        except commands.CommandError:
            pass

    @commands.check(Basic_checker().check_station_channel)
    # @commands.has_role("Management")
    @commands.slash_command(
        name="buy_ticket",
        description="Buy a train ticket to your next destination")
    async def buy_ticket(self, ctx):
        try:
            await ctx.response.defer()
            ticket_check = await ChecksOfJohto.travel_tickets()
            member = ctx.guild.get_member(ctx.user.id)
            database = self.db.execute(f"SELECT * FROM Johto WHERE User_ID = '{member.id}' ")
            database = database.fetchall()
            ticket = database[0][3]
            permit = database[0][4]
            kanto_coins = database[0][18]
            if permit > ticket and kanto_coins >= 25:
                self.db.execute(f'UPDATE Johto SET Ticket = Ticket + 1, Johto_Coins = Johto_Coins - 25 WHERE User_ID = {member.id}')
                self.db.commit()
                place = list(ticket_check.keys())[list(ticket_check.values()).index(ticket + 1)]
                msg = f"You purchased a ticket to travel to {place}!"
                await ctx.edit_original_message(content=msg)
                #await QuestsOfJohto.kanto_leaderboard(self, ctx)
            elif kanto_coins < 25:
                msg = f"Sorry you only have **{kanto_coins}** Johto coin(s), you need **25** to buy a train ticket!"
                await ctx.edit_original_message(content=msg)
            else:
                embed = await Custom_embed(
                        self.client, title = f"The path ahead is blocked", description = f"""You can't travel any further yet, there is a sleeping Snorlax blocking your path"""
                    ).setup_embed()
                embed.set_image(url = "https://raw.githubusercontent.com/Pr1nc3St4r/ff_images/main/misc/snorlax_sleeping.jpg")
                await ctx.edit_original_message(embed=embed)
        except commands.CommandError:
            pass

    @commands.slash_command(
        name="inventory",
        description="Check how many Johto Coins you own!")
    async def inventory(self, ctx):
        await ctx.response.defer()

        member = ctx.guild.get_member(ctx.user.id)
        database = self.db.execute(f"SELECT * FROM Johto WHERE User_ID = '{member.id}' ")
        database = database.fetchall()
        kanto_coins = database[0][18]
        amulet_count = database[0][20]
        # item_info = await ChecksOfJohto.shop_check()
        # item = item_info[item_id]
        # item_name, item_value, emoji = item

        day = datetime.datetime.today().weekday()
        if day < 5: # Normal weekday rates
            embed = await Custom_embed(
                    self.client, title = f"{member.display_name}'s Inventory", description = f"""Johto Coin(s): **{kanto_coins:,}** <:JohtoCoin:1474149692454731818>
Johto Amulet(s): **{amulet_count}** <:JohtoAmulet:1474149802441707612>
"""
                ).setup_embed()
            embed.set_thumbnail(url="https://raw.githubusercontent.com/Pr1nc3St4r/ff_images/main/misc/coin_bag1.png")
        else: # 5 Sat, 6 Sun.  Weekend bonus rates
            embed = await Custom_embed(
                    self.client, title = f"{member.display_name}'s Inventory", description = f"""🎉Weekend bonus rate is currently active🎉\n\nJohto Coin(s): **{kanto_coins:,}** <:JohtoCoin:1474149692454731818>
Johto Amulet(s): **{amulet_count}** <:JohtoAmulet:1474149802441707612>
"""
                ).setup_embed()
            embed.set_thumbnail(url="https://raw.githubusercontent.com/Pr1nc3St4r/ff_images/main/misc/coin_bag1.png")

        await ctx.edit_original_message(embed=embed)

    # @commands.slash_command(
    #     name="data_fix",
    #     description="What is this for?")
    # async def data_fix(self, ctx, user: disnake.Member = None):
    #     await ctx.response.defer()
    #     if user is None:
    #         member = ctx.guild.get_member(ctx.author.id)
    #     else:
    #         member = ctx.guild.get_member(user.id)
    #     mon_count = set()
    #     self.db.execute(f"UPDATE Travel SET Secret_Quest_2 = '{mon_count}' WHERE User_ID = {user.id}")
    #     self.db.commit()
    #     await ctx.edit_original_message("Data type fixed")

    # @commands.check(check_if_it_is_me)
    @commands.check(Basic_checker().check_admin)
    @commands.command()
    async def ticket(self, ctx, user: disnake.Member = None, zone: int = None):
        try:
            ticket_check = await ChecksOfJohto.travel_tickets()
            if user is None:
                await ctx.send("Please mention a user to get their ID")
                return
            if zone is None:
                await ctx.send("Please set a zone")
                return
            if zone >= 0:
                self.db.execute(f'UPDATE Travel SET Ticket = {zone} WHERE User_ID = {user.id}')
                self.db.commit()
                place = list(ticket_check.keys())[list(ticket_check.values()).index(zone)]
                await ctx.send(f"You were given a ticket to travel to {place}!")
            else:
                self.db.execute(f'DELETE FROM Travel WHERE User_ID = {user.id}')
                self.db.commit()
                await ctx.send(f"Removed")
        except commands.CommandError:
            pass

    # @commands.check(check_if_it_is_me)
    @commands.check(Basic_checker().check_admin)
    @commands.command()
    async def permit(self, ctx, user: disnake.Member = None, zone: int = None):
        try:
            ticket_check = await ChecksOfJohto.travel_tickets()
            if user is None:
                await ctx.send("Please mention a user to get their ID")
                return
            if zone is None:
                await ctx.send("Please set a zone")
                return
            if zone >= 0:
                self.db.execute(f'UPDATE Travel SET Permit = {zone} WHERE User_ID = {user.id}')
                self.db.commit()
                place = list(ticket_check.keys())[list(ticket_check.values()).index(zone)]
                await ctx.send(f"You were given permission to travel up to {place}!")
            else:
                self.db.execute(f'DELETE FROM Travel WHERE User_ID = {user.id}')
                self.db.commit()
                await ctx.send(f"Removed")
        except commands.CommandError:
            pass

    @commands.check(Basic_checker().check_travel_channel)
    @commands.slash_command(
        name="oak",
        description="Ring Professor Oak to ask for some advice on how to progress.")
    async def oak(self, ctx):
        try:
            await ctx.response.defer()
            user = ctx.author
            database = self.db.execute(f'SELECT * FROM Johto Where User_ID = {user.id}')
            database = database.fetchone()

            permit = database[4]
            ticket = database[3]

            newbark_count = database[5]
            newbark_needed = await ChecksOfJohto.newbark_check()

            running_shoes = database[6]
            pokegear = database[7]
            shoe_need, gear_need = await ChecksOfJohto.cherrygrove_check()

            violet_count = database[8]
            violet_needed = await ChecksOfJohto.violet_check()

            azalea_count = database[9]
            azalea_needed, azalea_mon = await ChecksOfJohto.azalea_check()

            goldenrod_count = len(database[10].split(","))
            goldenrod_needed = await ChecksOfJohto.goldenrod_check()
            goldenrod_needed = len(goldenrod_needed)

            ecruteak_count = database[11]
            ecruteak_needed = await ChecksOfJohto.ecruteak_check()

            olivine_count = database[12]
            olivine_needed = await ChecksOfJohto.olivine_check()

            cianwood_count = database[13]
            cianwood_mons, cianwood_needed = await ChecksOfJohto.cianwood_check()

            mahogany_count = database[14]
            mahogany_needed = await ChecksOfJohto.mahogany_check()

            blackthorn_count = database[15]
            blackthorn_needed, blackthorn_items = await ChecksOfJohto.blackthorn_check()

            embed = await Custom_embed(
                    self.client, 
                ).setup_embed()
            embed.set_image(url = "https://raw.githubusercontent.com/Pr1nc3St4r/ff_images/main/misc/proff_oak.png")
            embed.set_author(name= "You rang Professor Oak!",
            icon_url = "https://raw.githubusercontent.com/Pr1nc3St4r/ff_images/main/misc/oak_author.png")
            if permit == ticket:
                if permit == 0:
                    score = newbark_count / newbark_needed
                    comment = await self.oak_comment(score)
                    embed.description = f"""Hi {user.display_name}! So kind of you to call.

Grateful you're helping me explore the Johto region! Try to catch some more of the regions Pokémon for me!

{comment}"""
                elif permit == 1:
                    if shoe_need > running_shoes:
                        shoe_score = 0
                    else:
                        shoe_score = 0.5
                    if gear_need > pokegear:
                        gear_score = 0
                    else:
                        gear_score = 0.5
                    score = shoe_score + gear_score
                    comment = await self.oak_comment(score)
                    embed.description = f"""Hi {user.display_name}! How are you?
                
Now that you've taken the first steps on your Pokémon adventure, it's time to gather some equipment.  The Running Shoes and the Pokegear should come in handy!

{comment}"""
                elif permit == 2:
                    score = violet_count / violet_needed
                    comment = await self.oak_comment(score)
                    embed.description = f"""Hi {user.display_name}! It's great to hear from you!
                
You're really proving yourself to be a natural Pokémon trainer. This regions <:grasstype:854350473556525077> Pokémon seem to be different than those in Kanto...

{comment}"""
                elif permit == 3:
                    score = azalea_count / azalea_needed
                    comment = await self.oak_comment(score)
                    embed.description = f"""Hi {user.display_name}!
                
Did you know that Slowpoke can evolve into a different Pokémon here?! We should investigate this!

{comment}"""
                elif permit == 4:
                    score = goldenrod_count / goldenrod_needed
                    comment = await self.oak_comment(score)
                    embed.description = f"""Hi {user.display_name}! Great work so far!
                
Goldenrod City is known for its game corner, and while I condone gambling in any form, I wonder if we can get some lucky numbers while catching?

{comment}"""
                elif permit == 5:
                    score = ecruteak_count / ecruteak_needed
                    comment = await self.oak_comment(score)
                    embed.description = f"""Hi {user.display_name}! Did you enjoy your time in Johto so far?
                
Ecruteak City once had the Brass Tower standing tall before it **caught fire**.
*It's alao said that Ho-oh once resided here.*

{comment}"""
                elif permit == 6:
                    score = olivine_count / olivine_needed
                    comment = await self.oak_comment(score)
                    embed.description = f"""Hi {user.display_name}! 
                
Wow, what a coastline here in Olivine City! Just weird that the Lighthouse seems to be **out of power**...

{comment}"""
                elif permit == 7:
                    score = cianwood_count / cianwood_needed
                    comment = await self.oak_comment(score)
                    embed.description = f"""Hi {user.display_name}!
                
It looks like you made it to the Safari Zone, amazing!  It seems like a specific few Pokémon are found here.  Would you be so kind to catch some for my research?

{comment}"""
                elif permit == 8:
                    score = mahogany_count / mahogany_needed
                    comment = await self.oak_comment(score)
                    embed.description = f"""Hi {user.display_name}!
                
Mahogany's Gym Leader Pryce is an old friend of mine and a true Ice-type Pokémon connaisseur! Maybe he will grant you the badge if you show him a lot!

{comment}"""
                elif permit == 9:
                    score = blackthorn_count / blackthorn_needed
                    comment = await self.oak_comment(score)
                    embed.description = f"""Hi {user.display_name}!
                
Wow, did you know that the Dragon's Den is used by Ace Trainers to enhance their Pokémons? Maybe they don't know about Type-boosting items yet?!

{comment}"""
                else:
                    embed.description = f"""This area is still under construction"""
            else:
                embed.description = f"""Hi there {user.display_name}.  It looks like you have permission to travel to a new location.
            
Don't forget to buy your train ticket in <#1079409997496193145>"""

            embed.set_thumbnail(url=None)
            await ctx.send(embed=embed)
        except commands.CommandError:
            pass

    @commands.has_permissions(administrator=True)
    @commands.slash_command(
        name="admin_kanto",
        description="Admin command to check progress")
    async def admin_kanto(self, ctx):
        try:
            await ctx.response.defer()
            database = self.db.execute(f"SELECT * FROM Johto")
            database = database.fetchall()
            msg = "__**Johto Progress Check**__\n"
            for row in database:
                msg += f"<@{row[1]}>: **{row[4]}**\n"
            await ctx.send(msg)
        except commands.CommandError:
            pass

    @commands.has_permissions(administrator=True)
    @commands.slash_command(
        name="admin_kanto_coins",
        description="Admin command to check progress")
    async def admin_kanto_coins(self, ctx):
        try:
            await ctx.response.defer()
            database = self.db.execute(f"SELECT * FROM Johto")
            database = database.fetchall()
            msg = "__**Johto Coin Check**__\n"
            for row in database:
                msg += f"<@{row[1]}>: **{row[18]}**\n"
            await ctx.send(msg)
        except commands.CommandError:
            pass

    @commands.has_permissions(administrator=True)
    @commands.slash_command(
        name="compensation",
        description="compensate everyone!")
    async def compensation(self, ctx):
        try:
            await ctx.response.defer()
            db_pallet = self.db.execute(f'SELECT * FROM Johto')
            db_pallet = db_pallet.fetchall()
            self.db.execute(f"UPDATE Johto SET Johto_Coins = Johto_Coins + 5 WHERE Permit = 1")
            self.db.commit()
            names = "The following people have received +5 Johto coins <:JohtoCoin:1474149692454731818>\n"
            for row in db_pallet:
                if row[4] == 1:
                    names += f"<@{row[1]}>\n"
            await ctx.send(names)
        except commands.CommandError:
            pass

    @commands.has_permissions(administrator=True)
    @commands.slash_command(
        name="give",
        description="compensate everyone!")
    async def give(self, ctx, user: disnake.Member, coins: int):
        await ctx.response.defer()
        if user.bot:
            await ctx.send("Sorry, you can't send coins to bots.")
        else:
            # Check if entry exists for the user
            database = self.db.execute(f"SELECT * FROM Johto WHERE User_ID = {user.id}")
            database = database.fetchone()

            if database is None:
                await ctx.send(f"{user.display_name} has not begun their Johto adventure so can't receive Johto Coins.")
            else:
                self.db.execute(f"UPDATE Johto SET Johto_Coins = Johto_Coins + {coins} WHERE User_ID = {user.id}")
                self.db.commit()
                await ctx.send(f"{user.display_name} was given **{coins}** Johto Coins <:JohtoCoin:1474149692454731818>")


    @commands.has_permissions(administrator=True)
    @commands.command()
    async def mon(self, ctx, user: disnake.Member = None):
        dev_cat = 1101147200718917652
        if ctx.channel.category_id == dev_cat:
            if user is None:
                member = ctx.guild.get_member(ctx.author.id)
            else:
                member = ctx.guild.get_member(user.id)
            await asyncio.create_task(Mon_Cmd.mon_overview(self, ctx, member))
            try:
                database = self.db.execute(f"SELECT * FROM Johto WHERE User_ID = '{member.id}' ")
                database = database.fetchone()
                if database == None:
                    await ctx.send(f"Region 'Johto' not yet started for {member.name}",delete_after = 15)
                    await asyncio.sleep(15)
                    await ctx.message.delete()
                    return
                db = self.db.execute(f"SELECT Permit, Ticket FROM Johto WHERE User_ID = {member.id}")
                db = db.fetchone()
                checks, ticket_check = await asyncio.create_task(Mon_Cmd.mon_region_checker(self, ctx, "johto"))
                # if database:
                #     if database[5] is not None:
                #         pewter_count = eval(database[5])
                #         pewter_count = len(pewter_count)
                #     else:
                #         pewter_count = 0
                    # if database[0][17] is not None:
                    #     other_2_count = eval(database[0][17])
                    #     other_2_count = len(other_2_count)
                    # else:
                    #     other_2_count = 0
                # Handling Other 2 count
                #     if database[14] is not None:
                #         other_2_count = len(json.loads(database[14]))
                #     else:
                #         other_2_count = 0
                # else:
                #     return

                newbark_need = await ChecksOfJohto.newbark_check()
                shoe_need, gear_need = await ChecksOfJohto.cherrygrove_check()
                violet_need = await ChecksOfJohto.violet_check()
                azalea_need, catch_id = await ChecksOfJohto.azalea_check()
                goldenrod_need = await ChecksOfJohto.goldenrod_check()
                ecruteak_need = await ChecksOfJohto.ecruteak_check()
                olivine_need = await ChecksOfJohto.olivine_check()
                safari_mons, cianwood_need = await ChecksOfJohto.cianwood_check()
                mahogany_needed = await ChecksOfJohto.mahogany_check()
                blackthorn_needed, items_unused = await ChecksOfJohto.blackthorn_check()
                description = f"""__**Travel Stats**__
Ticket: {db[1]} {list(ticket_check.keys())[list(ticket_check.values()).index(db[1])]}
Permission: {db[0]} {list(ticket_check.keys())[list(ticket_check.values()).index(db[0])]}

__**Quest Stats**__
Chosen Starter: Dex No. {database[19]}\n"""
                database = self.db.execute(f"SELECT Newbark_Quest,Running_Shoes,Pokegear,Violet_Quest,Azalea_Quest,Goldenrod_Quest,Ecruteak_Quest,Olivine_Quest,Cianwood_Quest,Mahogany_Quest,Blackthorn_Quest FROM Johto WHERE User_ID = {member.id}")
                database = database.fetchone()
                newbark, shoes, gear, violet, azalea, goldenrod, ecruteak, olivine, cianwood, mahogany, blackthorn = database
                description += f"""Newbark: {newbark} / {newbark_need}
Cherrygrove: Shoes {shoes} / {shoe_need}, Gear {gear} / {gear_need}
Violet: {violet} / {violet_need}
Azalea: {azalea} / {azalea_need}
Goldenrod: {goldenrod} / {goldenrod_need}
Ecruteak: {ecruteak} / {ecruteak_need}
Olivine: {olivine} / {olivine_need}
Cianwood: {cianwood} / {cianwood_need}
Mahogany: {mahogany} / {mahogany_needed}
Blackthorn: {blackthorn} / {blackthorn_needed}"""
                database = self.db.execute(f"SELECT Secret_1, Secret_2 FROM Johto WHERE User_ID = {member.id}")
                database = database.fetchone()
                description +=f"\n    Other 1 count: {database[0]}\n    Other 2 count: {database[1]}"
                embed = await Custom_embed(
                        self.client, title = f"Stats for {member.name}", description = description
                    ).setup_embed()
                await ctx.send(embed=embed, delete_after = 15)
                try:
                    await ctx.message.delete()
                except:
                    return
            except commands.CommandError:
                pass

    # @commands.check(Basic_checker().check_management)
    # @commands.command()
    # async def progress(self, ctx):
    #     await QuestsOfJohto.kanto_leaderboard(self, ctx)
    #     await QuestsOfJohto.mew_leaderboard(self, ctx)

    @commands.check(Basic_checker().check_travel_channel)
    # @commands.has_permissions(administrator=True)
    @commands.slash_command(
        name="pokemart",
        description="testing")
    async def _kanto_shop(self, ctx):
        pass

    @_kanto_shop.sub_command(name="buy", description="buy an item", 
        options=[
            Option(
                name="item_id",
                description="Enter the Item ID you want to buy",
                type=4,
                required=True,
            ),
            Option(
                name="amount",
                description="Enter the amount you want to buy",
                type=4,
                required=True,
            ),
        ],)
    async def _buy_item(self, ctx, item_id, amount):
        user = ctx.user
        travel_database = self.db.execute(f"SELECT * FROM Travel WHERE User_ID = '{user.id}' ")
        travel_database = travel_database.fetchall()
        current_coins = travel_database[0][18]
        amulet_count = travel_database[0][20]
        item_info = await ChecksOfJohto.shop_check()
        item = item_info[item_id]
        item_name, item_value, emoji = item
        item_cost = item_value * amount
        if current_coins >= item_cost:
            if item_id == 1:
                if amulet_count < 10:
                    self.db.execute(f"UPDATE Travel SET Johto_Coins = Johto_Coins - {item_cost}, Johto_Amulet = Johto_Amulet + {amount} WHERE User_ID = {user.id}")
                    self.db.commit()
                    if amount == 1:
                        await ctx.send(f"{user.mention} bought a {item_name}! {emoji}")
                    else:
                        await ctx.send(f"{user.mention} bought {amount} {item_name}s! {emoji}")
                else:
                    await ctx.send(f"Sorry, you already have the maximum allowed for this item")
            else:
                await ctx.send(f"Sorry, this item is not in stock yet")
        else:
            await ctx.send(f"Sorry, you don't have enough Johto Coins <:JohtoCoin:1474149692454731818> to buy this item")

    @_kanto_shop.sub_command(name="view", description="view the shop")
    async def _view_shop(self, ctx):
        # await ctx.send("This is currently under construction")
        user = ctx.user
        travel_database = self.db.execute(f"SELECT * FROM Johto WHERE User_ID = '{user.id}' ")
        travel_database = travel_database.fetchone()
        current_coins = 0
        amulet_count = 0
        if travel_database:
            current_coins = travel_database[18]
            amulet_count = travel_database[20]

        item_info = await ChecksOfJohto.shop_check()
        msg = "__**Shop Inventory**__\n"
        msg += """`#ID Item         Price(Owned)`
--------------------------------\n"""

        for item_id, item in item_info.items():
            item_name, item_cost_value, emoji = item
            if item_id == 1:
                msg += f"`{item_id:<2}`{emoji} `{item_name.capitalize():<15} {item_cost_value}({amulet_count})`\n"
            else:
                msg += f"`{item_id:<2}`{emoji} `{item_name.capitalize():<15} {item_cost_value}`\n"
        embed = await Custom_embed(
                self.client, title = f"Johto Pokémart", description = f"""Welcome to the Johto Pokémart!

You currently have **{current_coins}** Johto coins.

*Prices in Johto coins* <:JohtoCoin:1474149692454731818>
{msg}"""
            ).setup_embed()
        embed.set_thumbnail(url="https://raw.githubusercontent.com/Pr1nc3St4r/ff_images/main/misc/pokemart.png")
        await ctx.send(embed=embed)

    @_kanto_shop.sub_command(name="item_info", description="view the shop")
    async def _item_info(self, ctx):
        # await ctx.send("This is currently under construction")
        
        item_info = await ChecksOfJohto.shop_check()
        msg = "__**Item Info**__\n"
        msg += """`Johto amulet` <:JohtoAmulet:1474149802441707612> - You can purchase up to **10** of these.  Each one improves your chances of finding Johto coins <:JohtoCoin:1474149692454731818> by **1%** (up to a max of **10%**). It also improves your chances of finding multiple coins at once."""
        embed = await Custom_embed(
                self.client, title = f"Johto Pokémart Item Info", description = f"""See below for information on the items available in the Pokémart.

{msg}"""
            ).setup_embed()
        embed.set_thumbnail(url="https://raw.githubusercontent.com/Pr1nc3St4r/ff_images/main/misc/pokemart.png")
        await ctx.send(embed=embed)



def setup(client):
    client.add_cog(Role_menu(client))