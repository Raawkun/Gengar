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
                    ball = entry.value.split("<:")[3].split(":")[0]
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
            
        
    async def check_catchlist(self, message, userid, method):
        emb = message.embeds[0]
        data = self.db.execute(f"SELECT DexID, Name FROM Dex WHERE Img_url = '{emb.image.url}'")
        data = data.fetchone()
        print(data[1])
        catchy = self.db.execute(f"SELECT * FROM Monthly_Catchlist WHERE Mon_ID = {int(data[0])}")
        catchy = catchy.fetchone()
        if catchy:
            print(catchy)
            if catchy[2] == method:
                check = self.db.execute(f"SELECT Mon_ID FROM User_Catchlist WHERE User_ID = {userid}")
                check = check.fetchone()
                if check:
                    check = check[0].split(", ")
                    if catchy[0] in check:
                        return
                    else:
                        await message.reply(f"Monthly Catchlist: {data[1]} with **{catchy[1]}**")
                else:
                    await message.reply(f"Monthly Catchlist: {data[1]} with **{catchy[1]}**")
                
    async def catch_catchlist(self, message, sender, method):
        emb = message.embeds[0]
        ballused = emb.description.split("with a")[1].split(":")[1]
        data = data = self.db.execute(f"SELECT DexID, Name FROM Dex WHERE Img_url = '{emb.image.url}'")
        data = data.fetchone()
        checklist = self.db.execute(f"SELECT * FROM Monthly_Catchlist WHERE Mon_ID = {data[0]}")
        checklist = checklist.fetchone()
        checkuser = self.db.execute(f"SELECT Mon_ID FROM User_Catchlist WHERE User_ID = {sender.id}")
        checkuser = checkuser.fetchone()
    
        if checklist:
            if checklist[2]==method:
                if ballused == checklist[1]:
                    if checkuser:
                        check = check[0].split(", ")
                        if data[0] in check:
                            return
                        else:
                            check.append(data[0])
                            check = check.join(", ")
                    else:
                        check = str(data[0])+", "
                    self.db.execute(f"INSERT or REPLACE INTO User_Catchlist VALUES ({sender.id}, '{check}')")
                    self.db.commit()
        return
                
                
    async def sz_catchlist(self, message, sender):
        emb = message.embeds[0]
        method=";safarizone"
        ballused = "safariball"
        data = data = self.db.execute(f"SELECT DexID, Name FROM Dex WHERE Img_url = '{emb.image.url}'")
        data = data.fetchone()
        checklist = self.db.execute(f"SELECT * FROM Monthly_Catchlist WHERE Mon_ID = {data[0]}")
        checklist = checklist.fetchone()
        checkuser = self.db.execute(f"SELECT Mon_ID FROM User_Catchlist WHERE User_ID = {sender.id}")
        checkuser = checkuser.fetchone()
    
        if checklist:
            if checklist[2]==method:
                if ballused == checklist[1]:
                    if checkuser:
                        check = checkuser[0].split(", ")
                        if data[0] in check:
                            return
                        else:
                            check.append(data[0])
                            check = check.join(", ")
                    else:
                        check = str(data[0])+", "
                    self.db.execute(f"INSERT or REPLACE INTO User_Catchlist VALUES ({sender.id}, '{check}')")
                    self.db.commit()
                await nessage.add_reaction('✅')
        return
            
 
            
            
def setup(client):
    client.add_cog(Catchlist(client))