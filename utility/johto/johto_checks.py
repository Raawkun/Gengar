from disnake.ext import commands
from sqlite3 import connect


class ChecksOfJohto(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.db = connect("database.db")

    async def travel_roles():
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

    async def travel_tickets():
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

    # async def pallet_mons():
        # pallet_quest = [1, 4, 7, 25]
        # return pallet_quest

    async def newbark_check(debug):
        if debug == 0:
            mons_needed = 500  #Catch 500 Johto mons
        else:
            mons_needed = 5
        return mons_needed
    
    async def cherrygrove_check():
        shoes_needed = 1 #Get the Running Shoes & Map
        pokegear_needed = 1
        return shoes_needed, pokegear_needed
    
    async def violet_check(debug):
        if debug == 0:
            mons_needed = 450 #Catch 450 amount of Grass mons
        else:
            mons_needed = 5
        return mons_needed

    async def azalea_check(debug): #NEEDS EDIT! Not yet decided.
        if debug == 0:
            mons_needed = 69 #Catch Slowpokes 69
        else:
            mons_needed = 1
        mon_id = 79
        return mons_needed, mon_id

    async def goldenrod_check(): #NEEDS EDIT! Not yet decided.
        coins_needed = [222, 333, 444, 555, 666, 777, 888, 999] #Get 777 coins from a single catch
        return coins_needed

    async def ecruteak_check(debug): #NEEDS EDIT! 
        if debug == 0:
            mons_needed = 250 #Catch Fire Mons
        else:
            mons_needed = 2
        return mons_needed

    async def olivine_check(debug): #Catch x amount of electric mons
        if debug == 0:
            mons_needed = 450
        else:
            mons_needed = 2
        return mons_needed

    async def cianwood_check(debug): #SAFARI ZONE 2 - Sentret Line 161 162, 179 Mareep, 183 Marill, (Hoppip Line) 187 188 189,  Sunkern 191, Wooper line 194 195, Murkrow 198, Misdreavus 200,  Wobbuffet 202,  Girafarig 203, Shuckle 213, Houndour 228 229, Stantler 234 , Smeargle 235 , Larvitar 246 
        safari_mons = [161, 162, 179, 183, 187, 188, 189, 191, 194, 195, 198, 200, 202, 203, 213, 228, 229, 234, 235, 246] 
        if debug == 0:
            mons_needed = 200
        else:
            mons_needed = 3
        return safari_mons, mons_needed

    async def mahogany_check(debug): #Catch Ice-Types
        if debug == 0:
            mons_needed = 450
        else:
            mons_needed = 3
        return mons_needed

    async def blackthorn_check(debug): #Catch x amount of type boosting items!
        if debug == 0:
            items_needed = 15
        else:
            items_needed = 1
        boosting = ["black belt", "black glasses", "charcoal", "dragon fang", "hard stone", "magnet", "metal coat", "miracle seed", "mystic water", "nevermeltice", "poison barb", "sharp beak", "silk scarf", "silver powder", "soft sand," "spell tag", "twisted spoon"]
        return items_needed, boosting
    
    async def secret_1_check():
        celebi = [251, 1251]
        mon_needed = 1
        return celebi, mon_needed
    
    async def secret_2_check():
        johto_legends = ["243", "244", "245", "249", "250"] #Raikou, Entei, Suicune, Lugia, Ho-oh
        mon_needed = len(johto_legends)
        return johto_legends, mon_needed
    
    async def coin_check(debug):
        # day = datetime.datetime.today().weekday()
        # if day < 5: # Normal weekday rates
        #     hunt_coinodds, fish_coinodds, battle_coinodds = 200, 150, 75
        # else: # 5 Sat, 6 Sun.  Weekend bonus rates
        #     hunt_coinodds, fish_coinodds, battle_coinodds = 175, 125, 60
        if debug == 0:
            hunt_coinodds, fish_coinodds, battle_coinodds = 170, 120, 55
        else:
            hunt_coinodds, fish_coinodds, battle_coinodds = 5, 5, 5
        return hunt_coinodds, fish_coinodds, battle_coinodds

    async def shop_check():
        item_cost = {1 : ["johto amulet", 50, "<:JohtoAmulet:1474149802441707612>"]}
                    # 2 : ["test", 500, "<a:Kantodex:1103758631708672110>"]}
        return item_cost

def setup(client):
    client.add_cog(ChecksOfJohto(client))