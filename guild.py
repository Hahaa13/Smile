import os 
import discord 
import random
import mysql.connector as Mysql
from discord.ext import commands
from discord_components import *
username = os.getenv('user')
hosts = os.getenv('ip')
passw = os.getenv('pass')



class guild(commands.Cog):
 def __init__(self,client):
   self.client =client
 @commands.Cog.listener()
 async def on_ready(self):
  print("guild on")      

 @commands.Cog.listener()
 async def on_guild_join(self,guild):
    db = Mysql.connect(host=hosts, user=username, passwd=passw, database=username )
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM guild WHERE guildID = {guild.id}")
    guild = cursor.fetchone()
    if guild == None:
     cursor.execute(f"INSERT INTO guild(guildID) VALUES({guild.id})")       
     cursor.execute(f"UPDATE guild SET prefix = 'smile' WHERE guildID = {guild.id}")
     cursor.execute(f"UPDATE guild SET lang = 'en' WHERE guildID = {guild.id}")
     cursor.execute(f"UPDATE guild SET perm = 'not' WHERE guildID = {guild.id}")       
     db.commit()
     cursor.close()
     db.close() 

 @commands.command(aliases=["lang"])
 @commands.has_permissions(administrator=True)       
 async def language(self,ctx,lange=None):
  db = Mysql.connect(host=hosts, user=username, passwd=passw, database=username )
  cursor = db.cursor()
  cursor.execute(f"SELECT * FROM guild WHERE guildID = {ctx.guild.id}")
  data = cursor.fetchone()
  g = await self.guildtd(ctx.guild)  
  lang = g[2]   
  if lange == None and lange != "en" and lange != "vi": 
   if lang == "en":
           await ctx.send(f"hey {ctx.author.name} what language you want change i have en and vi")
           return
   if lang == 'vi':
           await ctx.send(f"hey bro {ctx.author.name} muốn chọn language nào tôi có en và vi")
           return
            
  await ctx.send(f"{ctx.author.name} change language {lange} ")
  cursor.execute(f"UPDATE guild SET lang = '{lange}' WHERE guildID = {ctx.guild.id}")      
  db.commit()
  cursor.close()
  db.close()      
 async def guildtd(self,user):
    db = Mysql.connect(host=hosts, user=username, passwd=passw, database=username )
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM guild WHERE guildID = {user.id}")
    users = cursor.fetchone()

    cursor.close()
    db.close()

    return users

         
       

def setup(client):
        client.add_cog(guild(client))