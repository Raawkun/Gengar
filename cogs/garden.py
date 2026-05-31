import disnake
from disnake.ext import commands
from sqlite3 import connect
from datetime import datetime, timedelta
import asyncio
from utility.info_dict import rem_emotes, emote_list, embed_color
from utility.id_lists import berry_times

class Garden(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.db = connect("database.db")

        #DB STYLE:
        #USER_ID, Can, Slot_1, Slot_2, Slot_3, Slot_4, Slot_5, Slot_6 {berry, hourly, next_stage}

    def garden_check(self, userid, entry):
        slot = entry.split("**")[0]
        stamp = entry.split("<t:")[1].split(":R>")[0]
        stage = entry.split("STAGE ")[1].split("/")[0]
        planted = entry.split(":>")[1].split(" Berry")[0]
        rate = berry_times[planted]
        check = self.db.execute(f"SELECT * FROM Garden WHERE User_ID = {userid}")
        check = check.fetchone()
        reply == ""
        if check == None:
            reply = f"What a nice garden you have there! Would you mind telling me which watering can you use?\nPlease use ``mcan wailmer/lotad/psyduck``so I can determine when to ping you for watering/harvesting!"
            return reply
        if check is not None:
            cslot = check[slot+1]
            if cslot is not None:
                old_stamp = cslot.split(":")[2]
                berry = cslot.split(":")[0]
            else:
                cslot = f"{planted}:{rate}:{stamp}"
                self.db.execute(f"UPDATE Garden SET Slot_{slot} = '{cslot}' WHERE User_ID = {userid}")
                self.db.commit()

        
    def harvest_check(self, slot, message):
        reply = f"``;berry harvest {slot}``"
        return reply

    def water_check(self, slot, message):
        reply = f"``;berry water {slot}``"
        return reply
                        
                        
    async def user_check(self, userid, message):
        check = self.db.execute(f"SELECT Garden, Emotes, Ping FROM Toggle WHERE User_ID = {userid}")
        check = check.fetchone()
        if (check == None) or (check[0] == 0):
            return
        else:
            emb = message.embeds[0]
            desc = emb.description
            if "Tip:" in desc:
                desc = desc.split("Tip:")[1]
            pots = desc.split("**Slot ")
            print(pots)
            reply = ""
            commands = f"Suggested commands are:\n"
            for entry in pots:
                slot = entry.split("**")[0]
                print(entry)
                if"Ready to harvest" in entry:
                    commands += await self.harvest_check(self, slot, message)
                elif "Needs watering" in entry:
                    commands += await self.harvest_check(self, slot, message)
                elif "Next stage" in entry:
                    reply += await self.garden_check(self, userid, entry)
                elif ":lock" in entry:
                    pass
                else:
                    continue
            reply += "\n"+commands
            await message.reply(reply)

def setup(client):
    client.add_cog(Garden(client))