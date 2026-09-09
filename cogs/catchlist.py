import disnake, asyncio
from disnake.ext import commands
import sqlite3, math
from sqlite3 import connect


class Catchlist(commands.Cog):


    def __init__(self, client):
        self.client = client
        self.db = connect("database.db")
    
    async def update_catchlist(self, message):
        emb = message.embeds[0]
        data = ""
        #print(emb.fields)
        for entry in emb.fields:
            if " from " in entry.value:
                #print(entry.value)
                try:
                    method = entry.value.split("`")[1]
                    mon_id = int(entry.value.split(":")[1])
                    ball = entry.value.split("**")[1]
                    print(f"{mon_id}, {ball}, {method}")
                except Exception as e:
                    print(e) 
                try:
                    self.db.execute(f"INSERT or REPLACE INTO Monthly_Catchlist VALUES ({mon_id}, '{ball}', '{method}')")
                    self.db.commit()
                except Exception as e:
                    print(e)
                data = data+" "+str(mon_id)
                    
        print(data)
            
        
    async def check_catchlist(self, message, method):
        emb = message.embeds[0]
        data = self.db.execute(f"SELECT DexID, Name FROM Dex WHERE Img_url = '{emb.image.url}'")
        data = data.fetchone()
        print(data[1])
    
 
            
            
def setup(client):
    client.add_cog(Catchlist(client))