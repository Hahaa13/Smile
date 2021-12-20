import os 
import discord 
import random
import asyncio 
import mysql.connector as Mysql
from discord.ext import commands
from discord_components import *
username = os.getenv('user')
hosts = os.getenv('ip')
passw = os.getenv('pass')

class eco(commands.Cog):
 def __init__(self,client):
  self.client = client
 @commands.Cog.listener()
 async def on_ready(self):
         DiscordComponents(self.client)
         print("economy on")


 @commands.command(aliases=["profile","account","acc","p","a"])
 async def coin(self,ctx,m: discord.Member=None): 
  if m == None:
    m = ctx.author
  
  db = Mysql.connect(host=hosts, user=username, passwd=passw, database=username )
  cursor = db.cursor()
  cursor.execute(f"SELECT * FROM user WHERE id = {m.id}")
  data = cursor.fetchone()
  g = await self.guild(ctx.guild)
  lang = g[2]       
  if data is None:
   if lang == "en":
         await ctx.send(f"{m.name} you do not have account try register !")
         return
   if lang == "vi":
         await ctx.send(f"{m.name} bạn chưa có tài khoản hãy thử đăng kí !")       
         return
  acc = await self.account(m)  
  coin = acc[1]
  máu = acc[2]
  thức = acc[3]  
  nước = acc[4] 
  age = acc[5] 
  job = acc[6] 
  lv = acc[7]
  xp = acc[8]
  city = acc[9] 
  e = discord.Embed(title=f"**Profile**",description =f"**Name: {m.name}   Age: {age}\nJob: {job}   City: {city}\nLevel: {lv}   EXP: {xp}/{int(200*((1/2)*lv))}**",color=0xFF6D0A )
  e.add_field(name="Stats 📊", value=f"**<:heartsm:921702930481049651>Heart: {máu}/100** \n**<:bottle_smile:909253362707484692>Thirsty: {nước}/100**\n**<:thits:921703629667332127>Hungry: {thức}/100**", inline=False)
  e.add_field(name="Coins", value=f"**<:smilecoin:911958277405949982>Coin**: {coin}", inline=False)       
  e.set_thumbnail(url=m.avatar_url)       
  await ctx.send(embed=e) 

 @commands.command(aliases=["battle","b"])
 @commands.cooldown(1, 30, commands.BucketType.user)       
 async def fight(self,ctx):
  db = Mysql.connect(host=hosts, user=username, passwd=passw, database=username )
  cursor = db.cursor()
  cursor.execute(f"SELECT * FROM user WHERE id = {ctx.author.id}")
  data = cursor.fetchone()
  g = await self.guild(ctx.guild)
  lang = g[2]       
  if data is None:
   if lang == "en":
         await ctx.send(f"{m.name} you do not have account try register !")
         return
   if lang == "vi":
         await ctx.send(f"{m.name} bạn chưa có tài khoản hãy thử đăng kí !")       
         return
  acc = await self.account(ctx.author)
  máu = acc[2]
  if máu <= 0:
   if lang == "en":
       await ctx.send("You die try again 💀")
       return  
   if lang == "vi":
       await ctx.send("Bạn đã chết hãy thử lại 💀")    
       return  
  gen = random.randint(1,20)         
  cursor.execute(f"UPDATE user SET thức = thức - 3 WHERE id = {ctx.author.id}")
  db.commit()  
  cursor.execute(f"UPDATE user SET nước = nước - 3 WHERE id = {ctx.author.id}")
  db.commit()          
  emy = ["Smile God","Smile Fat","Smile Golem"] 
  emy = random.choice(emy)
  link = "" 
  if emy == "Smile God":
    link = "https://media.discordapp.net/attachments/910166129027198986/921782144387383356/Khong_Co_Tieu_e153_20211218221231.png"     
    he = 50
    sh = 20
    gen = 10

    cl = random.randint(10,100)      
  elif emy == "Smile Fat":
    he = 80
    sh = 30
    gen = 10

    cl = random.randint(50,200)      
       
    link = "https://media.discordapp.net/attachments/905830835041730610/921786579977134080/Webp.net-gifmaker_16.gif"       
  elif emy == "Smile Golem":
    he = 100
    sh = 30
    gen = 20      
    cl = random.randint(50,250)             
          
    link = "https://media.discordapp.net/attachments/905830835041730610/921789001189429258/Webp.net-gifmaker_28.gif"     
  power = 0         
  e = discord.Embed(title=f"**{ctx.author.name}** going to fighting !",description=f"You Find {emy} \n **<:heartsm:921702930481049651>Heart: {he}**\n **🛡️Shield: {sh}**\n**You**:\n **<:heartsm:921702930481049651>Heart: {máu}/100**\n**<:powerr:922498996239495219>Power: {power}/10**",color=0xFF6D0A ) 
  e.set_image(url=link)        
  msg = await ctx.send(embed=e,components=[
       [Button(style=ButtonStyle.green, label="HIT",emoji="✊"),
        Button(style=ButtonStyle.red, label="HEAL",emoji="❤"),
        Button(style=ButtonStyle.grey, label="RUN",emoji="🏃"),
       
       ],
       ])
  p = True
  def check(reponse):
    return reponse.user == ctx.author
  while p:
   reponse = await self.client.wait_for("button_click",check=check,timeout=10.0)
   if reponse.component.label=="HIT":
    dmg = random.randint(1,10)
    dmg1 = random.randint(1,3)
    if sh > 0:
     sh -= dmg
    else:
     he -= dmg   
    if máu > 0:
     cursor.execute(f"UPDATE user SET máu = máu - {dmg1} WHERE id = {ctx.author.id}")
     db.commit()      
     máu -= dmg1
    if máu <= 0:
     await msg.edit(components=[
       [Button(style=ButtonStyle.green, label="HIT",emoji="✊",disabled=True),
        Button(style=ButtonStyle.red, label="HEAL",emoji="❤",disabled=True ),
        Button(style=ButtonStyle.grey, label="RUN",emoji="🏃",disabled=True ),
       
       ],
       ])
     p = False
     await ctx.send("You die 💀") 
     return       
    if he <= 0:
     await msg.edit(components=[
       [Button(style=ButtonStyle.green, label="HIT",emoji="✊",disabled=True),
        Button(style=ButtonStyle.red, label="HEAL",emoji="❤",disabled=True ),
        Button(style=ButtonStyle.grey, label="RUN",emoji="🏃",disabled=True ),
       
       ],
       ])
     p = False
     await ctx.send(f"You win and earned {cl}<:smilecoin:911958277405949982> and {gen} xp")
     cursor.execute(f"UPDATE user SET xp = xp + {gen} WHERE id = {ctx.author.id}")
     db.commit()      
     cursor.execute(f"UPDATE user SET coin = coin + {cl} WHERE id = {ctx.author.id}")
     db.commit() 
     lv = acc[7]
     xp = acc[8]      
     xp = ((50*((lv-1)**2))+(50*(lv-1)))      

     if xp == 0:
        cursor.execute(f"UPDATE user SET lv = lv + 1 WHERE id = {ctx.author.id}")
        db.commit()  
        cursor.execute(f"UPDATE user SET xp = 0 WHERE id = {ctx.author.id}")
        db.commit()       
        await ctx.send(f"You leveled up {lv+1}")    
     return 
    power += 1        
    e = discord.Embed(title=f"**{ctx.author.name}** going to fighting !",description=f"You Find {emy} \n **<:heartsm:921702930481049651>Heart: {he}**\n **🛡️Shield: {sh}**\n**You**:\n **<:heartsm:921702930481049651>Heart: {máu}/100**\n**<:powerr:922498996239495219>Power: {power}/10** ",color=0xFF6D0A )
    e.set_image(url=link)        
    await msg.edit(embed=e,components=[
       [Button(style=ButtonStyle.green, label="HIT",emoji="✊"),
        Button(style=ButtonStyle.red, label="HEAL",emoji="❤"),
        Button(style=ButtonStyle.grey, label="RUN",emoji="🏃"),
       
       ],
       ])
   if reponse.component.label=="HEAL":
           if power <= 10:
                   await ctx.send("You do not have 10 power for use heal !")
                   return
           power -= 10


           heal = random.randint(1,5)    
           cursor.execute(f"UPDATE user SET máu = máu + {heal} WHERE id = {ctx.author.id}")
           db.commit()  
          
           máu += heal
           e = discord.Embed(title=f"**{ctx.author.name}** going to fighting !",description=f"You Find {emy} \n **<:heartsm:921702930481049651>Heart: {he}**\n **🛡️Shield: {sh}**\n**You**:\n **<:heartsm:921702930481049651>Heart: {máu}/100**\n**<:powerr:922498996239495219>Power: {power}/10** ",color=0xFF6D0A )
           e.set_image(url=link)        
           await msg.edit(embed=e,components=[
       [Button(style=ButtonStyle.green, label="HIT",emoji="✊"),
        Button(style=ButtonStyle.red, label="HEAL",emoji="❤"),
        Button(style=ButtonStyle.grey, label="RUN",emoji="🏃"),
       
       ],
       ])
            
   if reponse.component.label=="RUN":  
    await ctx.send("You run")
    await msg.edit(components=[
       [Button(style=ButtonStyle.green, label="HIT",emoji="✊",disabled=True),
        Button(style=ButtonStyle.red, label="HEAL",emoji="❤",disabled=True ),
        Button(style=ButtonStyle.grey, label="RUN",emoji="🏃",disabled=True ),
       
       ],
       ])
    p = False
     










   
           
 @commands.command()
 @commands.cooldown(1, 300, commands.BucketType.user)              
 async def heal(self,ctx):
 
  db = Mysql.connect(host=hosts, user=username, passwd=passw, database=username )
  cursor = db.cursor()
  cursor.execute(f"SELECT * FROM user WHERE id = {ctx.author.id}")
  data = cursor.fetchone()
  g = await self.guild(ctx.guild)
  lang = g[2]       
  if data is None:
   if lang == "en":
         await ctx.send(f"{ctx.author.name} you do not have account try register !")
         return
   if lang == "vi":
         await ctx.send(f"{ctx.author.name} bạn chưa có tài khoản hãy thử đăng kí !")       
         return

  heal = random.randint(1,8)        
  db = Mysql.connect(host=hosts, user=username, passwd=passw, database=username )
  cursor = db.cursor()
  e = discord.Embed(description=f"Healing...for {ctx.author.name}",color=0xFF6D0A )
  e.add_field(name="Heal Life", value=f"**{heal}**<:heartsm:921702930481049651> ", inline=False)     
  cursor.execute(f"UPDATE user SET máu = máu + {heal} WHERE id = {ctx.author.id}")
  db.commit()   
  await ctx.send(embed=e)        
 @commands.command(aliases=["dangki","reg"])
 async def register(self,ctx):
  db = Mysql.connect(host=hosts, user=username, passwd=passw, database=username )
  cursor = db.cursor()
  cursor.execute(f"SELECT * FROM user WHERE id = {ctx.author.id}")
  data = cursor.fetchone()
  g = await self.guild(ctx.guild)
  lang = g[2]     
  user = ctx.author       
  if data == None:
    cursor.execute(f"INSERT INTO user(id) VALUES({ctx.author.id})")
    db.commit()
          
    cursor.execute(f"UPDATE user SET coin = 500 WHERE id = {user.id}")
    db.commit()    
    cursor.execute(f"UPDATE user SET máu = 100 WHERE id = {user.id}")
    db.commit()    
    cursor.execute(f"UPDATE user SET nước = 100 WHERE id = {user.id}")
    db.commit()
    cursor.execute(f"UPDATE user SET thức = 100 WHERE id = {user.id}")
    db.commit()      
    cursor.execute(f"UPDATE user SET age = 1 WHERE id = {user.id}")
    db.commit()
    cursor.execute(f"UPDATE user SET job = 'jobless' WHERE id = {user.id}")
    db.commit()
    cursor.execute(f"UPDATE user SET lv = 1 WHERE id = {user.id}")
    db.commit()
    cursor.execute(f"UPDATE user SET xp = 0 WHERE id = {user.id}")
    db.commit()      
    cursor.execute(f"UPDATE user SET city = 'SmileCity' WHERE id = {user.id}")
    db.commit()
    
         
    cursor.close()
    db.close()
    await ctx.send(f"I created an account for you {ctx.author.mention} ")      
  if data != None:
          await ctx.send(f"{ctx.author.mention} already you have account !")

          
 
 async def guild(self,user):
    db = Mysql.connect(host=hosts, user=username, passwd=passw, database=username )
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM guild WHERE guildID = {user.id}")
    users = cursor.fetchone()

    cursor.close()
    db.close()

    return users

 async def account(self,user):
    db = Mysql.connect(host=hosts, user=username, passwd=passw, database=username )
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM user WHERE id ={user.id}")
    users = cursor.fetchone()

    cursor.close()
    db.close()

    return users

         
def setup(client):
        client.add_cog(eco(client))