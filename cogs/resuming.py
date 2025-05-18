import disnake, asyncio
from disnake.ext import commands
import sqlite3, math
from sqlite3 import connect
from cogs.reminder import Reminders

class Resuming(commands.Cog):


    def __init__(self, client):
        self.client = client
        self.db = connect("database.db")
    
    async def cancel_all_tracked_tasks():
        print(list(Reminders.bg_tasks))
        for task in list(Reminders.bg_tasks):
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                print(f"✅ Cancelled: {task.get_coro().__name__}")
            except Exception as e:
                print(e)
        Reminders.bg_tasks.clear()




def setup(client):
    client.add_cog(Resuming(client))