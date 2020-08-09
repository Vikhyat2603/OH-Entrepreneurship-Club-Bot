import discord
import random
from socket import gethostname
import traceback
import os
 
client = discord.Client()

########################################

debugMode = (gethostname() == 'VKSN-Desktop')

if debugMode:
    botToken = open('BOT_TOKEN.txt', 'r').read()
else:
    botToken = str(os.environ.get('BOT_TOKEN'))

despace = lambda s: s.replace(' ', '')
commandPrefix = '!'

########################################
# Log an error message and print if debugMode is on
async def logError(guild, myText):
    expChannel = discord.utils.get(guild.channels, name=f'bot-experiments')
    if debugMode:
        print(str(myText))
    await expChannel.send('<@!693797662960386069> **Log**: ' + str(myText))

# Greet new users on DM
@client.event
async def on_member_join(member):
    try:
        await member.create_dm()
        await member.dm_channel.send(f'Hi {member.name}, welcome to the **Openhouse Entrepreneurship Club** Server!')
        await member.dm_channel.send(file=discord.File(r'assets/WelcomePoster.jpg'))
    except Exception as e:
        await logError(client.guilds[0], f'Member join : {traceback.format_exc()}')

# Informs me when bot comes online
@client.event
async def on_ready():
    await logError(client.guilds[0], 'Bot Online')
    
# Respond to messages
@client.event
async def on_message(message):
    try:
        text = message.content
        author = message.author
        authorStr = str(author)
        authorID = author.id
        guild = message.guild

        if authorID == client.user.id:
            return

        # Let Vikhyat debug code
        if (authorStr == 'Vikhyat#5088'):
            if text.startswith('!debug'):
                code = text[6:]
                try:
                    await message.channel.send(str(eval(code)))
                except Exception:
                    await logError(guild, traceback.format_exc())

            elif text.startswith('!exec'):
                code = text[6:]
                try:
                    await message.channel.send(str(exec(code)))
                except Exception:
                    await logError(guild, traceback.format_exc())

        text = despace(text.lower())

        # Check for command prefix
        if not text.startswith(commandPrefix):
            return

        # Remove command prefix
        text = text[len(commandPrefix):]
        if text in ['hello', 'hi', 'hey']:
            await message.channel.send(f'Hello there, {author}!')            
            return
        
    except Exception as e:
        await logError(guild, traceback.format_exc())

########################################
client.run(botToken)
