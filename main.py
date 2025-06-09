import asyncio
import os
import disnake
from disnake.ext import commands
from disnake.ext.commands import CommandNotFound
from disnake.ext.commands import CommandSyncFlags


f = open("key.txt", "r")
token = f.read()

intents = disnake.Intents.all()
sync_flags = CommandSyncFlags.default()
sync_flags.sync_commands_debug = True

def __init__(self, client):
    self.client = client

client = commands.AutoShardedBot(intents = intents, command_prefix =commands.when_mentioned_or("m", "M"),help_command=None, reload = True, command_sync_flags=sync_flags)

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        return
        
@client.event
async def on_type_error(self, message, error):
    if isinstance(error, TypeError):
        log = self.client.get_channel(1210143608355823647)
        await log.send(f"Original message: [Click here](message.url)\n{message.content}")
        return

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')


client.loop.run_until_complete(client.start(token))