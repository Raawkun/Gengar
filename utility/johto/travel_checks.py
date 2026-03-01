import disnake
from disnake.ext import commands
from disnake import Option, OptionChoice, OptionType, ApplicationCommandInteraction
import asyncio
import math
import random
from sqlite3 import connect
import datetime

class TravelChecks(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.db = connect("database.db")

    """Region IDs:
    Johto = 1
    """

    async def check_gather(location):
        if location == "johto":
            roles = await TravelChecks.johto_roles()
            #print(roles)
            tickets = await TravelChecks.johto_tickets()
            #print(tickets)
            region_id = 1
        return roles, tickets, region_id


    async def johto_roles():
        roles = [
"New Bark Town",
"Cherrygrove City",
"Violet City",
"Azalea Town",
"Goldenrod City",
"Ecruteak City",
"Olivine City",
"Cianwood City",
"Mahogany Town",
"Blackthorn Island"
]
        return roles

    async def johto_tickets():
        ticket_check = {
"New Bark Town" : 0,
"Cherrygrove City" : 1,
"Violet City" : 2,
"Azalea Town" : 3,
"Goldenrod City" : 4,
"Ecruteak City" : 5,
"Olivine City" : 6,
"Cianwood City" : 7,
"Mahogany Town" : 8,
"Blackthorn Island" : 9,
"Anywhere" : 10
}
        return ticket_check
    
    async def travel_locations():
        locations = {
"Chat" : [1209176219317440512],
"New Bark Town" : [1211070035729322024, 1211070062644043966, 1211070085267988500],
"Cherrygrove City" : [1211070223415910470, 1211070242906701884, 1211070265287647363],
"Violet City" : [1211070322233712670, 1211070353338531890, 1211070388843319348],
"Azalea Town" : [1211070494904819733, 1211070533349806101, 1211070553532932257],
"Goldenrod City" : [1211070660462248028, 1211070685825204224, 1211070702304886784],
"Ecruteak City" : [1211070812384272510, 1211070831795642410],
"Olivine City" : [1211070882848444446, 1211070909742456843],
"Cianwood City" : [1211071052055314482, 1211071069801160704],
"Mahogany Town" : [1211071126718124032, 1211071149145063486],
"Blackthorn Island" : [1211071221710458880],
"Johto" : [1227329210830553188]}
        return locations

def setup(client):
    client.add_cog(TravelChecks(client))