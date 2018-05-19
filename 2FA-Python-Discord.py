import datetime
import pyotp
import discord
import asyncio
import os
from hashlib import md5
import base64

@client.event
async def on_message(message):
    try:
		if(message.author==client.user):
			return

		if message.content.startswith('$otp'):
			uid=str(message.author.id).encode()
			encoded = base64.b32encode(uid+key.encode())
			totp = pyotp.TOTP(encoded)
			print("OTP request for user: "+message.author.name)
			secs=datetime.datetime.now().timetuple()[5]
			if secs<30:

				secs=30-secs
				
			elif secs<60:    
				secs=60-secs
			print(encoded) #You can add this key to your Authenticator to Cross Verify the 2FA Code.	
			await client.send_message(message.channel,str(totp.now())+' valid for '+str(secs)+' seconds.')
			
    except Exception as e:
        print(e)
        

try:
    
    client.run('#DISCORD TOKEN')
except Exception as e:
    raise e
