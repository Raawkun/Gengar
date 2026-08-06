import disnake
from disnake.ext import commands
from sqlite3 import connect
from datetime import datetime, timedelta
import asyncio
from utility.info_dict import rem_emotes, emote_list, embed_color

class Reminders(commands.Cog):

    def __init__(self,client):
        self.client = client
        self.db = connect("database.db")

    async def garden_ping(self, userid, check):
        slot = check[2]
        berry = check[4]
        timestamp = int(check[3])
        channel = self.client.get_channel(check[5])
        data = connect("database.db").execute(f"SELECT ToggleGarden, Ping, Emotes FROM Toggle WHERE User_ID = {userid}")
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
            await asyncio.sleep(int(datetime.current_time.timestamp())-timestamp)
            if data[1] == 0:
                await channel.send(desc, allowed_mentions=disnake.AllowedMentions(users=False))
            else:
                await channel.send(desc)

            self.db.execute(f"UPDATE Garden SET Slot = None, timestamp = None, Berry = None WHERE User_ID = {userid}")
            self.db.commit()

    async def load_garden(self):
        check = self.db.execute(f"SELECT * FROM Garden WHERE timestamp > 0 ORDER BY timestamp ASC")
        check = check.fetchall()
        for row in check:
            await asyncio.create_task(Reminders.garden_ping(self, row[0], row))


    async def load_reminder(self):
        reminders = self.db.execute(f'SELECT * FROM Toggle WHERE QuestTime >= 1 ORDER BY QuestTime ASC')
        reminders = reminders.fetchall()
        #print(reminders)
        for row in reminders:
            channelid = row[8]
            self.db.execute(f'UPDATE Toggle SET Timer = 0 WHERE Channel = {channelid}')
            self.db.commit()
            current_time = datetime.timestamp(datetime.now())
            waiter = row[7]
            userid = row[1]
            if waiter > current_time:
                waiter = waiter-current_time
                #print(waiter)
                if row[14] == 1:
                    reminder = 1
                else:
                    reminder = 0
                if row[6] == 1:
                    emote = 0
                else:
                    emote = 1
                if row[5] == 0:
                    link = 0
                else:
                    link = 1
                
                await asyncio.create_task(Reminders._quest_reminder(self,channelid, userid, waiter, reminder, link, emote))
            elif waiter < current_time:
                self.db.execute(f'UPDATE Toggle SET Channel = 0, QuestTime = 0, Timer = 0 WHERE User_ID = {userid}')
                self.db.commit()

    async def _quest_reminder(self,channelid, user_id, waiter,reminder, link, emote):
        print(f"quest_reminder started for {user_id} waiting for {waiter} seconds.")
        channel = self.client.get_channel(channelid)
        self.db.execute(f'UPDATE Toggle SET Timer = 1 WHERE User_ID = {user_id}')
        self.db.commit()
        await asyncio.sleep(waiter)
        #print("slept enough.")
        if link == 0:
            link = "``;quest``"
        else:
            link = f'</quest info:1015311085517156475>'
        if emote == 1:
            if link == 0:
                link = ""
            desc = f'{rem_emotes["remind"]} - <@{user_id}> {rem_emotes["next"]}{rem_emotes["quest"]} {link}'
        else:
            desc = f'{rem_emotes["remind"]} - <@{user_id}>, your next {link} is ready!'
        if reminder == 1:
            await channel.send(desc)
        self.db.execute(f'UPDATE Toggle SET QuestTime = 0, Channel = 0, Timer = 0 WHERE User_ID = {user_id}')
        self.db.commit()

    def create_tracked_task(self, coro):
        task = asyncio.create_task(coro)
        self.client.bg_tasks.append(task)
        #conn = Listener.get_db_connection(self)
        #with conn.cursor() as cursor:
            #cursor.execute(f"INSERT INTO Tasks VALUES ('{task.get_coro().__name__}', '{task}')")
            #print("We're in")
            #cursor.commit()
            #conn.ensure_closed()
        print(f"Added: {task.get_coro().__name__}")
        #print(Reminders.bg_tasks)
        def remove(_):
            self.client.bg_tasks.remove(task)
            #conn = Listener.get_db_connection(self)
            #with conn.cursor() as cursor:
                #cursor.execute(f"DELETE * FROM Tasks WHERE Name = '{task.get_coro().__name__}'")
                #cursor.commit()
                #conn.ensure_closed()

        task.add_done_callback(remove)
        return task

                

def setup(client):
    client.add_cog(Reminders(client))