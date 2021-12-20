import os 
import random 
import discord 
import asyncio 
from discord.ext import commands ,tasks
from discord_components import *
from keep_alive import keep_alive
import mysql.connector as Mysql



nameuser = os.getenv('user')
hosts = os.getenv('ip')
passw = os.getenv('pass')

def get_prefix(bot,message):
        return commands.when_mentioned_or("smile")(bot,message)
                                          
client = commands.Bot(command_prefix=get_prefix,help_command=None,intents=discord.Intents.all())

@client.event
async def on_ready():
        print("online")
                              
                           
                 
async def statusbot(): 
      await client.wait_until_ready() 

      status = ["@smile help",f"Make smile in {len(client.guilds)} guilds",f"Make smile {len(set(client.get_all_members()))} members"]  
      while not client.is_closed(): 
       activity = random.choice(status)
       await client.change_presence(status=discord.Status.dnd, activity=discord.Game(name=activity))
       await asyncio.sleep(7)               
               
client.loop.create_task(statusbot())
            
for filename in os.listdir('./cogs'):

  if filename.endswith('.py'):

    client.load_extension(f'cogs.{filename[:-3]}')

@client.command(aliases=["reload"])
@commands.is_owner()
async def re(ctx,en):
 try:
  msg = await ctx.send(f"Đang reload {en}")        
  client.unload_extension(f"cogs.{en}")
  client.load_extension(f"cogs.{en}")
  await msg.edit(f"load thành công {en}")       
 except:
  
  await ctx.send(f"Lỗi không thể reload\n```\n{error}\n```")  

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
            
            await ctx.send(f"<:cansa_smile:909247700149612604> **{ctx.author.name} ** please wait **{int(s)}s** to try again",delete_after=s)
        elif d == 0 and h == 0:
           await ctx.send(f"<:cansa_smile:909247700149612604> **{ctx.author.name}** please wait **{int(m)}m {int(s)}s **",delete_after=s)
             
        
    elif isinstance(error, commands.CheckFailure):
        await ctx.send(f"{ctx.author.name} you don't have permission for use this commands.")
    raise error

         
keep_alive()
client.run(os.getenv('token'))