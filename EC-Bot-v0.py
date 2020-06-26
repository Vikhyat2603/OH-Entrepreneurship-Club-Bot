import discord
import random
from socket import gethostname
import traceback
import os

client = discord.Client()

########################################

welcomeMessage = '''Thank you for joining the us on Discord, we are so excited to have you on board!
Don’t worry if the new system seems challenging, we are here to help.
All the channels here are like different group chats where you can discuss anything you want (channel=chat).
Please feel free to message us if you are facing any difficulties.'''

debugMode = (gethostname() == 'VKSN-Desktop')

if debugMode:
    botToken, guildID = open('ECbotInfo.txt', 'r').readlines()
    guildID = int(guildID)
else:
    botToken = str(os.environ.get('BOT_TOKEN'))
    guildID = int(os.environ.get('GUILD_ID'))

despace = lambda s: s.replace(' ', '')
commandPrefix = '!'

########################################
# Log an error message and print if debugMode is on
async def logError(myText):
    expChannel = discord.utils.get(ohGuild.channels, name=f'bot-experiments')
    if debugMode:
        print(str(myText))
    await expChannel.send('<@!693797662960386069> **Log**: ' + str(myText))

# Greet new users on DM
@client.event
async def on_member_join(member):
    try:
        await member.create_dm()
        await member.dm_channel.send(f'Hi {member.name}, welcome to the **Openhouse Entrepreneurship Club** Server!')
        await member.dm_channel.send(welcomeMessage)
        await message.channel.send(file = discord.File('Welcome.jpg'))
    except Exception as e:
        await logError(f'Member join : {traceback.format_exc()}')

# Informs me when bot comes online
@client.event
async def on_ready():
    try:
        global ohGuild
        ohGuild = client.get_guild(guildID)
        expChannel = discord.utils.get(ohGuild.channels, name='bot-experiments')
        await logError('Bot Online')
        
    except Exception as e:
        await logError(traceback.format_exc())
    
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
                    await logError(traceback.format_exc())

            elif text.startswith('!exec'):
                code = text[6:]
                try:
                    await message.channel.send(str(exec(code)))
                except Exception:
                    await logError(traceback.format_exc())

        # Pass queries to the queries channel
        if text.startswith('!query'):
            query = text[6:]
            queryMessage = ('-' * 80) + f'\nUser : {authorStr}\nQuery : {query}'
            queryChannel = discord.utils.get(guild.channels, name='queries')
            await queryChannel.send(queryMessage)
            await message.channel.send('Sent:\n' + queryMessage)
            return

        text = despace(text.lower())

        # Check for command prefix
        if not text.startswith(commandPrefix):
            return

        # Remove command prefix
        text = text[len(commandPrefix):]
        if text in ['hello', 'hi', 'hey']:
            await message.channel.send(f'Hello there, {author}!')            
            return

        ############################################################
        
    except Exception as e:
        await logError(traceback.format_exc())

########################################
client.run(botToken)