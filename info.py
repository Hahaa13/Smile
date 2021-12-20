import os 
import random 
import discord
from discord.ext import commands
from discord_components import *
import mysql.connector as Mysql
username = os.getenv('user')
hosts = os.getenv('ip')
passw = os.getenv('pass')
import platform 
class info(commands.Cog):
 def __init__(self,client):
         self.client=client
 @commands.Cog.listener()
 async def on_ready(self):
  DiscordComponents(self.client)       
  print("info on")       

 @commands.command()
 async def help(self,ctx):
  e = discord.Embed(description=f"**Prefix : @smile**\n**Support :** [link](https://discord.gg/2SqnPmTfTt)\n **🏓 Smile Ping** : {round(self.client.latency * 1000) }ms",color=0xFF6D0A )         
  e.add_field(name="💰 Economy",value="profile register battle",inline=False)
  e.add_field(name="🛠️ Utility",value="language",inline=False)
  e.add_field(name="🧐 Info", value="help ping avatar bot", inline=False)
  await ctx.send(embed=e)

 @commands.command()
 async def ping(self,ctx):
         
         e = discord.Embed(description =f"🏓 Bot Ping : {round(self.client.latency * 1000)}ms",color=0xFF6D0A )
         await ctx.send(embed=e)

 @commands.command(aliases=["av","avt"])
 async def avatar(self,ctx,m: discord.Member=None):

  if m == None:

          m = ctx.author
  e = discord.Embed(title=f"{m.name} avatar",color=0xFF6D0A )
  e.set_image(url=m.avatar_url)
  await ctx.send(embed=e)

 @commands.command()
 async def bot(self,ctx):
  version = "0.1.5"       
  pythonVersion = platform.python_version()
  dpyVersion = discord.__version__
           
  e = discord.Embed(title="**Smile Info**",color=0xFF6D0A )
  e.add_field(name="📡 Version",value=f"\n **Smile : {version}**\n **API : {dpyVersion}**\n **Python : {pythonVersion}**",inline=False)     
  e.add_field(name="🤔 Guilds & Members",value=f"\n **Guilds : {len(self.client.guilds) }**\n **Members : {len(set(self.client.get_all_members()))}**",inline=False)
  e.set_author(name=self.client.user.name, icon_url=self.client.user.avatar_url)
  await ctx.send(embed=e)   


def setup(client):        
 client.add_cog(info(client))