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
        #conn = await Listener.get_db_connection(self)
        #async with conn.cursor() as cursor:
            #await cursor.execute(f"SELECT * FROM Tasks")
            #result = await cursor.fetchall()
            #await conn.ensure_closed()
        #print(list(Reminders.bg_tasks))
        for task in list(Reminders.bg_tasks):
        #for entry in result:
            #result[1].cancel()
            task.cancel()
            try:
                await result[1]
            except asyncio.CancelledError:
                print(f"✅ Cancelled: {result[1].get_coro().__name__}")
            except Exception as e:
                print(e)
        Reminders.bg_tasks.clear()
        #conn = await Listener.get_db_connection(self)
        #async with conn.cursor() as cursor:
            #await cursor.execute(f"DELETE * FROM Tasks")
            #print("Task DB Cleared")
            #await cursor.commit()
            #await conn.ensure_closed()
        
    @commands.command()
    async def tasks(self, ctx):
        listing = ""
        conn = await Listener.get_db_connection(self)
        async with conn.cursor() as cursor:
            await cursor.execute(f"SELECT * FROM Tasks")
            result = await cursor.fetchall()
            await conn.ensure_closed()
        for entry in result:
            listing += entry[0]
        print(listing)



def setup(client):
    client.add_cog(Resuming(client))