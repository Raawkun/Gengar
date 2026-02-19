from sqlite3 import connect
from disnake.ext import commands

from utility.johto.johto_checks import ChecksOfJohto

class Mon_Cmd(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.db = connect("database.db")

    async def mon_overview(self, ctx, member):
        db = self.db.execute(f"SELECT * FROM Travel WHERE User_ID = {member.id}")
        db = db.fetchone()
        if db:
            msg = f"""
__**Ticket Overview for {member.name}**__
Tour coins: {db[3]}
Region: Ticket | Permissions
Johto: {db[6]} | {db[7]}"""
            await ctx.message.reply(msg, delete_after = 15)
            await ctx.message.delete()
        else:
            await ctx.send("It seems that this user hasn't started their adventure.",delete_after = 15)
            await ctx.message.delete()

    async def mon_region_checker(self, ctx, region):
        checks = []
        if  region.lower() == "johto":
            ticket_check = await ChecksOfJohto.travel_tickets()
            one = await ChecksOfJohto.newbark_check()
            checks.append(one)
            two = await ChecksOfJohto.cherrygrove_check()
            checks.append(two)
            three = await ChecksOfJohto.violet_check()
            checks.append(three)
            useless, four = await ChecksOfJohto.azalea_check()
            checks.append(four)
            five = await ChecksOfJohto.goldenrod_check()
            checks.append(five)
            six = await ChecksOfJohto.ecruteak_check()
            checks.append(six)
            seven = await ChecksOfJohto.olivine_check()
            checks.append(seven)
            useless, eight = await ChecksOfJohto.cianwood_check()
            checks.append(eight)
            nine = await ChecksOfJohto.mahogany_check()
            checks.append(nine)
            ten = await ChecksOfJohto.blackthorn_check()
            checks.append(ten)
        return (checks, ticket_check)

def setup(client):
    client.add_cog(Mon_Cmd(client))