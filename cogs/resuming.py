import disnake, asyncio
from disnake.ext import commands
import sqlite3, math
from sqlite3 import connect

class Resuming(commands.Cog):


    def __init__(self, client):
        self.client = client
        self.db = connect("database.db")
    
    async def cancel_user_tasks():
        current = asyncio.current_task()
        for task in asyncio.all_tasks():
            if task is current:
                continue  # Don't cancel yourself

            # Filter 1: Task must have a stack trace (i.e., it's running Python code)
            stack = task.get_stack()
            if not stack:
                continue

            # Filter 2: Ignore internal library tasks
            if any("disnake" in frame.f_globals.get("__name__", "") or
                "discord" in frame.f_globals.get("__name__", "")
                for frame in stack):
                continue

            # Optional Filter 3: If you know your tasks share a module or name pattern
            if not any("my_module" in frame.f_globals.get("__name__", "") for frame in stack):
                continue

            # Cancel the task
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                print(f"Cancelled: {task.get_coro().__name__}")



def setup(client):
    client.add_cog(Resuming(client))