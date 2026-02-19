
# dependancies
import asyncio
import disnake

#time
import time
import datetime
from datetime import datetime, timedelta
from utility.johto.johto_checks import ChecksOfJohto

import random

# basic checker
class Basic_checker:
    """
    Manages the basic checks.
    """

    async def check_admin(self, ctx):
        if ctx.author.guild_permissions.administrator:
            return True
        
        await ctx.send("You need to have admin rights to use this command.", ephemeral=True)
        return False

    async def check_management(self, ctx):
        management_role_name = "Management"  # Replace with the actual role name
        
        for role in ctx.author.roles:
            if role.name == management_role_name:
                return True
        
        await ctx.send("You need to have the 'Management' role to use this command.", ephemeral=True)
        return False
    
    async def check_lb_helper(self, ctx):
        lb_role_name = "Leaderboard Helper"
        for role in ctx.author.roles:
            if role.name == lb_role_name:
                return True

    async def check_server(self, ctx):
        if ctx.guild.id == 825813023716540426:
            return True
        await ctx.send("Sorry, this only works in the Paralympics server.", ephemeral=True)
        return(False)
    
    async def check_if_it_is_me(self, ctx):
        if ctx.author.id == 352224989367369729:
            return(True)
        else:
            await ctx.send(f"Sorry, only Prof Blue can use this command", ephemeral=True)
            return(False)

    async def check_station_channel(self, ctx):
        if ctx.channel.id == 1207680838272294952:
            return(True)
        else:
            await ctx.send("You can't use that in here, you must go to <#1207680838272294952>", ephemeral=True)
            return(False)
        
    async def check_travel_channel(self, ctx):
        locations = await ChecksOfJohto.travel_locations()
        for location, numbers in locations.items():
            if ctx.channel.id in numbers:
                return True
                
        await ctx.send("This command only works in the Johto region, you have no phone reception here", ephemeral=True)
        return False
        