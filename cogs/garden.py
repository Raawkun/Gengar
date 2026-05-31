import disnake
from disnake.ext import commands
from sqlite3 import connect
from datetime import datetime, timedelta
import asyncio
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
        #USER_ID, Can, Slot_1, Slot_2, Slot_3, Slot_4, Slot_5, Slot_6 {berry, hourly, next_stage}

    async def garden_ping(self, message, userid, type, stamp, slot):
        numbers = {"1":"one", "2":"two","3":"three","4":"four","5":"five","6":"six"}
        if slot != "all":
            og_slot=slot
            slot = numbers[slot]
        data = self.db.execute(f"SELECT Garden, Ping, Emote FROM Toggle WHERE User_ID = {userid}")
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
                    desc = f"<@{userid}> - your berry at garden slot {slot} needs water!"
                else:
                    desc = f"<@{userid}> - your berry at garden slot {slot} is ready to be harvested!"
            await asyncio.sleep(int(self.current_time.timestamp())-stamp)
            if data[1] == 0:
                await message.channel.send(desc, allowed_mentions=disnake.AllowedMentions(users=False))
            else:
                await message.channel.send(desc)
            if slot == "all":
                self.db.execute(f"UPDATE Garden SET Slot_1 = None, Slot_2 = None, Slot_3 = None, Slot_4 = None, Slot_5 = None, Slot_6 = None WHERE User_ID = {userid}")
                self.db.commit()
            else:
                self.db.execute(f"UPDATE Garden SET Slot_{og_slot} = None WHERE User_ID = {userid}")
                self.db.commit()

    async def garden_reminder(self, userid, type, slot, stamp,message):
        slots = self.db.execute(f"SELECT * FROM Garden WHERE User_ID = {userid}")
        slots = slots.fetchone()
        slots = slots.pop(0).pop(0)
        timers = []
        for entry in slots:
            if entry is not None:
                timers.append(int(entry.split(":")[3]))
        timers = sorted(timers)
        if max(timers)-min(timers) <=300:
            slot = "all"
            print("All for one, make the timer only once")
            asyncio.create_task(Reminders.create_tracked_task(self, Garden.garden_ping(Garden,message,userid,type,stamp,slot)))
        else:
            for t in timers:
                print(t)
                asyncio.create_task(Reminders.create_tracked_task(self, Garden.garden_ping(Garden,message,userid,type,stamp,slot)))


    def garden_check(self, userid, entry, message):
        slot = entry.split("**")[0]
        stamp = entry.split("<t:")[1].split(":R>")[0]
        stage = entry.split("STAGE ")[1].split("/")[0]
        planted = entry.split("> ")[1].split(" Berry")[0]
        rate = berry_times[planted]
        check = self.db.execute(f"SELECT * FROM Garden WHERE User_ID = {userid}")
        check = check.fetchone()
        reply == ""
        if check == None:
            reply = f"What a nice garden you have there! Would you mind telling me which watering can you use?\nPlease use ``mcan wailmer/lotad/psyduck``so I can determine when to ping you for watering/harvesting!"
            return reply
        if check is not None:
            cslot = check[slot+1]
            if cslot is None:
                cslot = f"{planted}:{rate}:{stamp}"
                self.db.execute(f"UPDATE Garden SET Slot_{slot} = '{cslot}' WHERE User_ID = {userid}")
                self.db.commit()
            else:
                old_stamp = cslot.split(":")[2]
                berry = cslot.split(":")[0]
                if old_stamp != stamp:
                    cslot = f"{planted}:{rate}:{stamp}"
                    self.db.execute(f"UPDATE Garden SET Slot_{slot} = '{cslot}' WHERE User_ID = {userid}")
                    self.db.commit()
                    asyncio.create_task(Garden.garden_reminder())

        
    def harvest_check(self, slot):
        reply = f"``;berry harvest {slot}``"
        return reply

    def water_check(self, slot):
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
                    commands += await Garden.harvest_check(self, slot, message)
                elif "Needs watering" in entry:
                    commands += await Garden.harvest_check(self, slot, message)
                elif "Next stage" in entry:
                    reply += await Garden.garden_check(self, userid, entry, message)
                elif ":lock" in entry:
                    pass
                else:
                    continue
            reply += "\n"+commands
            await message.reply(reply)

def setup(client):
    client.add_cog(Garden(client))