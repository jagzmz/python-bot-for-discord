import datetime
import pyotp

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
                
            await client.send_message(message.channel,str(totp.now())+' valid for '+str(secs)+' seconds.')