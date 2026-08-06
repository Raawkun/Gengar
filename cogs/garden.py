import disnake
from disnake.ext import commands
from sqlite3 import connect
from datetime import datetime, timedelta
import asyncio, re
from utility.info_dict import rem_emotes, emote_list, embed_color
from utility.id_lists import berry_times
from cogs.reminder import Reminders

class Garden(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.db = connect("database.db")

    current_time = datetime.utcnow()
    timestamp = current_time.strftime('%Y-%m-%d %H:%M:%S')

        #DB STYLE:
        #USER_ID, Can, Slot_1, timestamp, Slot_3, Slot_4, Slot_5, Slot_6 {berry, hourly, next_stage}

    async def garden_ping(self, message, userid, check):
        slot = check[2]
        berry = check[4]
        timestamp = int(check[3])
        can = check[1]
        data = connect("database.db").execute(f"SELECT ToggleGarden, Ping, Emote FROM Toggle WHERE User_ID = {userid}")
        data = data.fetchone()
        if data[0] == 0:
            exit
        else:
            if data[2] == 0:
                if type == "water":
                    desc = f"<@{userid}> - 🍓 :{slot}: 💧"
                else:
                    desc = f"<@{userid}> - 🍓 :{slot}: ✅"
            else:
                if type == "water":
                    desc = f"<@{userid}> - your {berry} Berry at garden slot {slot} needs water!"
                else:
                    desc = f"<@{userid}> - your {berry} Berry at garden slot {slot} is ready to be harvested!"
            await asyncio.sleep(int(self.current_time.timestamp())-timestamp)
            if data[1] == 0:
                await message.channel.send(desc, allowed_mentions=disnake.AllowedMentions(users=False))
            else:
                await message.channel.send(desc)

            self.db.execute(f"UPDATE Garden SET Slot = None, timestamp = None, Berry = None WHERE User_ID = {userid}")
            self.db.commit()

    async def garden_reminder(self, userid, message):
        check = self.db.execute(f"SELECT * FROM Garden WHERE User_ID = {userid}")
        check = check.fetchone()
        if check != None:
            asyncio.create_task(Reminders.create_tracked_task(self, Garden.garden_ping(Garden,message,userid, check)))
        


    def garden_check(self, userid, desc, message):
        check = self.db.execute(f"SELECT * FROM Garden WHERE User_ID = {userid}")
        check = check.fetchone()
        reply = ""
        pots = desc.split("\n**Slot ")
        growing = {}
        print(pots)
        for entry in pots:
            if "Next stage" in entry:
                slot = entry.split("**")[0]
                name = entry.split(" Berry")[0].split("> ")[1]
                print(name)
                stagetime = berry_times[name]
                current_stage = entry.split("STAGE ")[1].split("/")[0]
                n_stamp = entry.split("t:")[1].split(":")[0]
                finishtime = int(n_stamp)+(4-(int(current_stage))*(int(stagetime)*60*60))
                growing[slot] = {"name":name,"finish":finishtime}

        try:
            best_key = min(growing, key=lambda k: growing[k]["finish"])
            best_entry = growing[best_key]

        except Exception as e:
            print(f"There was an error: {e}")

        if int(check[3]) <= best_entry["finish"]:
            return
        else:
            self.db.execute(f"UPDATE Garden SET Slot = {best_key}, timestamp = {best_entry['finish']}, Berry = '{growing[best_key]['name']}' WHERE User_ID = {userid}")
            self.db.commit()
            if check[1] == "psyduck":
                type = "harvest"
            else:
                type = "water"
            asyncio.create_task(Garden.garden_reminder(self,userid,message))
            reply += f"Added a reminder for slot {slot}\n"
            return reply

        
    def harvest_check(self, slot):
        reply = f"``;berry harvest {slot}``"
        return reply

    def water_check(self, slot):
        reply = f"``;berry water {slot}``"
        return reply
                        
                        
    async def user_check(self, userid, message):
        check = self.db.execute(f"SELECT ToggleGarden FROM Toggle WHERE User_ID = {userid}")
        check = check.fetchone()
        if (check == None) or (check[0] == 0):
            return
        else:
            check = self.db.execute(f"SELECT * FROM Garden WHERE User_ID == {userid}")
            check = check.fetchone()
            if check == None:
                msg = f"What a nice garden you have there! Would you mind telling me which watering can you use?\nPlease use ``mcan wailmer/lotad/psyduck``so I can determine when to ping you for watering/harvesting!"
                await message.reply(msg)
                exit
            else:
                emb = message.embeds[0]
                desc = emb.description
                if "Tip:" in desc:
                    desc = desc.split("Tip:")[1]
                target_word = "Next stage"
                matches = [s for s in desc if re.search(rf'{re.escape(target_word)}\b',s,re.IGNORECASE)]
                print(matches)
                if matches != None:
                    reply = ""
                    commands = f"Suggested commands are:\n"
                    growing = {}
                    reply += Garden.garden_check(self, userid, desc, message)

                            
                        

                    

                    
                reply += "\n"+commands
                await message.reply(reply)

def setup(client):
    client.add_cog(Garden(client))