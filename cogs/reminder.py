import disnake
from disnake.ext import commands
from sqlite3 import connect
from datetime import datetime, timedelta
import asyncio
from listener import Listener

class Reminders(commands.Cog):

    def __init__(self,client):
        self.client = client
        self.db = connect("database.db")

    bg_tasks = set()

    async def load_reminder(self):
        reminders = self.db.execute(f'SELECT * FROM Toggle WHERE QuestTime >= 1 ORDER BY QuestTime ASC')
        reminders = reminders.fetchall()
        #print(reminders)
        for row in reminders:
            channelid = row[8]
            self.db.execute(f'UPDATE Toggle SET Timer = 0 WHERE Channel = {channelid}')
            self.db.commit()
            current_time = datetime.datetime.timestamp(datetime.datetime.now())
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
                
                await asyncio.create_task(Listener._quest_reminder(channelid, userid, waiter, reminder, link, emote))
            elif waiter < current_time:
                self.db.execute(f'UPDATE Toggle SET Channel = 0, QuestTime = 0, Timer = 0 WHERE User_ID = {userid}')
                self.db.commit()

    def create_tracked_task(coro):
        task = asyncio.create_task(coro)
        Reminders.bg_tasks.add(task)

        def remove(_):
            Reminders.bg_tasks.discard(task)

        task.add_done_callback(remove)
        return task

                

def setup(client):
    client.add_cog(Reminders(client))