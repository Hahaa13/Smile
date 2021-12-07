import random 
import discord 
import os
import json
import datetime 
import time
from discord_components import *
from keep_alive import keep_alive
from discord.ext import commands 
import mysql.connector 
from mysql.connector import pooling
DB_HOST = "" 
DB_USER = "" 
DB_PASSWD = ""

DB_NAME = ""
poolname = ""
poolsize = 3

def get_prefix(bot, message):
       
       return commands.when_mentioned_or("s","S")(bot, message)  
        
intent = discord.Intents.all()
client = commands.AutoShardedBot(shard_count=3,command_prefix=get_prefix ,help_command=None,intents=intent)
start_time = time.time()

smilecash = "<:smilecoin:911958277405949982>"


@client.event
async def on_ready():
    DiscordComponents(client)    
    print("Smile Discord Bot")


@client.event
async def on_command_error(ctx, error):
    ignored = (commands.CommandNotFound, commands.UserInputError)
    if isinstance(error, ignored):
       return
        
    if isinstance(error, commands.CommandOnCooldown):
        m, s = divmod(error.retry_after, 60)
        h, m = divmod(m, 60)
        d, h = divmod(h, 24)
        if h == 0 and m == 0:
            
            await ctx.send(f"**Chờ 1 tí nha {ctx.author.name} hít tí cần sa <:cansa_smile:909247700149612604> là qua {int(s)}s thôi mà <:smile1:905828118810484777>**",delete_after=s)
        
        
    elif isinstance(error, commands.CheckFailure):
        await ctx.send(f"{ctx.author.name} không có quyền xài lệnh này.")
    raise error


@client.command()
@commands.is_owner()
async def load(ctx, eten):
    try:
     client.load_extension(f'cogs.{eten}')
    except:
       await ctx.send("Lỗi")
    
@client.command()
@commands.is_owner()
async def unload(ctx, eten):
   try:
    client.unload_extension(f'cogs.{eten}')
   except:
       await ctx.send("Lỗi")
    
   
for filename in os.listdir("./cogs"):
    if filename.endswith('.py'):
       client.load_extension(f'cogs.{filename[:-3]}')
     
@client.command()
@commands.cooldown(1,5,commands.BucketType.user)
async def uptime(ctx):
        current_time = time.time()
        difference = int(round(current_time - start_time))
        text = str(datetime.timedelta(seconds=difference))
        embed = discord.Embed(colour=0xFF6D0A )
        embed.add_field(name="Uptime", value=text)
        embed.set_footer(text="Smile")
        try:
            await ctx.send(embed=embed)
        except discord.HTTPException:
            await ctx.send(" uptime: " + text)

 
        
@client.command(pass_context=True)
@commands.guild_only()
async def ping(ctx):
  pings = [f"**Shard {x}**\nShard Ping : {round(client.get_shard(i).latency * 1000)} ms\nShard guild : {len([guild for guild in client.guilds if guild.shard_id == i])} guild"  for x, i in enumerate(client.shards, 1)]
  pings = "\n".join(pings)
  e = discord.Embed(title="Smile Ping & Shard",description =f"Bot Ping : {round(client.latency * 1000)}ms\n{pings} ",color=0xFF6D0A )
  await ctx.send(embed=e)


keep_alive()
client.run(os.getenv('token'))
