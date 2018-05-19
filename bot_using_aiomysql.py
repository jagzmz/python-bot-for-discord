
import discord
import asyncio
import os

from aiomysql import create_pool
import datetime
import pyotp
import base64
from hashlib import md5
import io
from bs4 import UnicodeDammit
import json

db_user = os.environ.get('DB_USER', None)
db_pass = os.environ.get('DB_PASS',None)
key=os.environ.get('skey',None)
db_name=os.environ.get('DB_NAME',None)
log_c=os.environ.get('log',None)

#discord
client = discord.Client()
game = discord.Game(name="Game Status")



@client.event
async def on_ready():
    await client.change_presence(game=game)
    print('Client Name: {}'.format(client.user.name))
    

def sender(m):
    return m.author
def is_me(m):
    return m.author == client.user

async def purge(message):
    if rolecheck(message):
        no=int(message.content.split()[1])
    return no+1

async def rolecheck(message):
    role_names = [role.name for role in message.author.roles]
    if "Admin" in role_names:
		#Do something if Admin
        return 1
    else:
        return 0




#Do something when user left
@client.event
async def on_member_remove(member):
	loop=asyncio.get_event_loop()
	async with create_pool(host='#HOST_NAME',
           	user=db_user, password=db_pass,
           	db=db_name, loop=loop) as pool:
		async with pool.get() as conn:
			async with conn.cursor() as cur:
				fetch=await cur.execute("""#SQL Query""",(param1,))
				
				print(fetch)
				if fetch>0:
					
					print("User {} left.".format(member.name))
					await client.send_message(member.server.get_channel(str(log_c)),"```Action Successful.```")
				else:
					await client.send_message(member.server.get_channel(str(log_c)),"```Action not successful.```")
					print("User {} left.".format(member.name))


            

@client.event
async def on_message(message):
    try:
        if message.content.startswith('$manual'):
        	usr=message.mentions[0]
        	hwiid=message.content.split()[2]
        	print(message.content.split()[2])
        	role_names = [role.name for role in message.author.roles]
        	print(role_names)
        	print(usr.id)
        	print(hwiid)
        	if "Head-Mod" in role_names:
        		print(usr.id)
        		print(key)
        		async with create_pool(host='#HOST_NAME',
					user=db_user, password=db_pass,
					db=db_name) as pool:
        			async with pool.get() as conn:
        				async with conn.cursor() as cur:
        					fetch=await cur.execute("""UPDATE `DB` set `KEY`=%s WHERE discid=%s""",(key,usr.id,))
        					print(fetch)
        					if fetch>0:
        						print("User {} Added.".format(member.name))
        						await client.send_message(message.channel,"```Done.\nKey of {0} Added```".format(member.name))
        					else:
        						await client.send_message(message.channel,"```Error.```".format(member.name))
        						print("User {} error.".format(member.name))


			if(message.content.startswith('$purge')):
            role_names = [role.name for role in message.author.roles]
            print(role_names)
            if "Admin" in role_names:
                await client.purge_from(message.channel, limit=await purge(message))

		if message.content.startswith('$time'):
            await client.send_message(message.channel,await cmd.time(message))


        if message.content.startswith('$search'):
            return
            trck=message.mentions[0]
            print('Search Query for {}'.format(message.mentions[0].name))
            loop=asyncio.get_event_loop()
            async with create_pool(host='#HOST_NAME',
                            user=db_user, password=db_pass,
                            db=db_name, loop=loop) as pool:
                    async with pool.get() as conn:
                        async with conn.cursor() as cur:
                            await cur.execute("""SELECT * FROM `DB` WHERE discid=%s""",(int(trck.id),))
                            fetch=await cur.fetchall()

                            if len(fetch)>0:
                                print(fetch)
                                chrs=1
                            else:
                                chrs=0
            if(chrs>0):
                
                await client.send_message(message.channel,'User `{}` present in database 🙂\nkey\n`{}`'.format(trck.name,fetch[0][3].replace("@","").replace("`","")))
            elif(chrs==0):
                await client.send_message(message.channel,'User `{}` not found in database 😕\nContact Admins if problem persists.'.format(message.author.name.replace("`","")))

        if message.content.startswith('$users'):

            loop=asyncio.get_event_loop()
            async with create_pool(host='#HOST_NAME',
                            user=db_user, password=db_pass,
                            db=db_name, loop=loop) as pool:
                    async with pool.get() as conn:
                        async with conn.cursor() as cur:
                            await cur.execute("""SELECT * FROM `DB`;""")
                            fetch=await cur.fetchall()
            await client.send_message(message.channel,'{0} users present in DB :tada: {1}'.format(len(fetch),ocemo))
            
        if message.content.startswith('$key'):
        	if message.channel.name=="key-acceptor":
	            print('key Query for '+message.author.name)
	            try:
	                try:
	                    msg=message.content.split()[1].replace("@","X").replace("`","X")
	                except Exception as e:
	                    await client.send_message(message.channel,"Invalid arguments.\nPlease enter in format\n`$key 'your key here'`")
	                    return
	                await client.send_message(message.channel,'Processing please wait...')
	                #loop=asyncio.get_event_loop()
	                ems = discord.Embed(title='🎉 Congratulations 🎉', description='', colour=0xFADBF)
	                ems.set_thumbnail(url=message.author.avatar_url)
	                ems.add_field(name='Result:',value='```key added to server.\nTry logging to our application again.\nUser-Id:     '+message.author.name+'\nkey-Status: Accepted🎉```',inline=True)
	                ems.set_thumbnail(url=message.author.avatar_url)
	                eme=discord.Embed(title='Existing key', description='', colour=0xFADBF)
	                eme.set_thumbnail(url=message.author.avatar_url)
	                eme.add_field(name='Result:',value='```\nTry logging to our application again.\nUser-Id:     '+message.author.name+'\nkey-Status: Already Accepted🤔```',inline=False)
	                async with create_pool(host='#HOST_NAME',
	                            user=db_user, password=db_pass,
	                            db=db_name) as pool:
	                    async with pool.get() as conn:
	                        async with conn.cursor() as cur:
	                            await cur.execute("""SELECT * FROM `DB` WHERE discid=%s""",(int(message.author.id,)))
	                            fetch=await cur.fetchall()
	                            if len(fetch)>0:
	                                print(fetch)
	                                chrs=1
	                            else:
	                                chrs=0
	                    conn.close()
	                pool.close()
	                await pool.wait_closed()

	                if chrs==1:
	                    print('Id Found: '+message.author.name)
	                    await client.send_message(message.channel,embed=eme)
	                elif chrs==0:
	                    
	                    try:
	                        
	                        async with create_pool(host='#HOST_NAME',
	                            user=db_user, password=db_pass,
	                            db=db_name,autocommit=True) as pool:
	                            async with pool.get() as conn:
	                                async with conn.cursor() as cur:
	                                    keye=msg
	                                    m=md5(str(keye).encode()).hexdigest()
	                                    try:
	                                        usernm=message.author.name.replace("'","").replace("@","X").replace("`","X").replace("update","X")
	                                        
	                                        await cur.execute("""INSERT INTO `DB` (`ban`, `dntr`, `usrnm`, `key`, `discid`)  VALUES (1,0,%s,%s,%s)""",(usernm,keye,int(message.author.id),))
	                                        await client.send_message(message.channel,message.author.mention,embed=ems)
	                                    except UnicodeEncodeError as e:
	                                        await client.send_message(message.channel,"{}\n```There's some problem with your name.\nPlease consider changing it to simple one removing fancy characters.```".format(message.author.mention))
	                                    
	                    except Exception as e:
	                        print(e)

	                    
	                    
	                print('=================')
	            except Exception as e:
	                print(e)
                



        if message.content.startswith('$update'):
            if message.channel.name=="key-acceptor":
            	nhwd=message.content.split()[1].replace("@","X").replace("`","X").replace("update","X")
            	loop=asyncio.get_event_loop()
            	async with create_pool(host='#HOST_NAME',
            	                user=db_user, password=db_pass,
            	                db=db_name, loop=loop,autocommit=True) as pool:
            	        async with pool.get() as conn:
            	            async with conn.cursor() as cur:
            	                await cur.execute("""UPDATE `DB` SET key=%s where discid=%s""",(nhwd,message.author.id))
            	                fetch=await cur.fetchall()
            	await client.send_message(message.channel,'Updated key for {}'.format(message.author.mention))
            

    except Exception as e:
        print(e)
        
 


try:
    
    client.run('#DISCORD TOKEN')
except Exception as e:
    raise e
