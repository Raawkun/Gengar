import disnake
from disnake.ext import commands
import math

class Methods(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.db = connect("database.db")

