import discord
from discord.ext import commands
import random

client = discord.Client()
bot = commands.Bot(command_prefix='$') #Must type this before any command so the bot recognizes its call


@bot.event
async def on_ready():
    print("{} Bot is ready:".format(bot.user.name))
    stats = bot.is_logged_in
    print(stats)


# Input a even number of elements in a list and displays two teams of random elements
@bot.command()
async def team(*arg):
    ar = []
    for k in arg:
        ar.append(k)
    random.shuffle(ar)
    half = len(ar)//2
    j = 0+half
    if len(ar) % 2 == 0:
        await bot.say("*Team One   --vs--   Team Two*\n")
        for i in range(half):   
            await bot.say("|{0:^20}  ----  {1:^20}|".format(ar[i], ar[j]))
            j += 1
    else:
        await bot.say("Please enter even number of members")


# Displays the creator of this bot
@bot.command()
async def creator():
    await bot.reply("Hi, I am a coding bot created by Sphrial")


# Displays a list of all the server this bot is connected to
@bot.command()
async def getserver():
    for i in bot.servers:
        await bot.say("{}".format(i))


# Enter a channel name and it will display the userID of that channel
@bot.command()
async def getchanuserid(name: str):
    chanary = []
    for server in bot.servers:
        for chan in server.channels:
            chanary.append(chan)
    channel = discord.utils.find(lambda c: c.name == name, chanary)
    if channel is not None:
        await bot.say('{}'.format(channel.id))


# Enter a members name and it will display the userID of that member
@bot.command()
async def getmemuserid(name: str):
    memary = []
    for i in bot.servers:
        for member in i.members:
            memary.append(member)
    member = discord.utils.find(lambda m: m.name == name, memary)
    if member is not None:
        await bot.say('{}'.format(member.id))


# Displays a list of all members and their status
@bot.command()
async def getmem():
    for i in bot.servers:
        for member in i.members:
            await bot.say('{:<15} -- {}'.format(member.status, member.name))


# Displays a list of all members that are online
@bot.command()
async def online():
    for i in bot.servers:
        for member in i.members:
            if member.status == discord.Status.online:
                await bot.say('{} -- {}'.format(member.name, member.status))


# Displays a list of all members that are online
@bot.command()
async def offline():
    for i in bot.servers:
        for member in i.members:
            if member.status == discord.Status.offline:
                await bot.say('{} -- {}'.format(member.name, member.status))


# Displays a list of all members that are offline
@bot.command()
async def getchan():
    for i in bot.servers:
        for chan in i.channels:
            await bot.say("{}".format(chan))


# Displays a list of all the voice channels
@bot.command()
async def getvoicechan():
    for i in bot.servers:
        for chan in i.channels:
            if chan.type == discord.ChannelType.voice: 
                await bot.say("{}".format(chan))


# Enter a @username and channel name that you would like to move them too
@bot.command()
async def move(member: discord.Member, channel: discord.Channel):
    await bot.move_member(member, channel)


@bot.command()
async def custom():
    await bot.say("Type 'join' to enter the game and 'done' once done with the list")
    teamlist = []

    def teamcheck(msg):
        if msg.content == "join" or msg.content == "done":
            return msg.content
    while len(teamlist) <= 12:
        teamplayer = await bot.wait_for_message(check=teamcheck)
        if teamplayer.content == "done":
            await bot.say("Getting Teams Ready")
            break
        if teamplayer.author not in teamlist:
            teamlist.append(teamplayer.author)
            await bot.say("{} player(s) in".format(len(teamlist)))
        else:
            await bot.say("User already in in team")
    random.shuffle(teamlist)
    chanary = []
    for server in bot.servers:
        for chan in server.channels:
            chanary.append(chan)
    channel = discord.utils.find(lambda c: c.name == 'Overwatch 2', chanary)
    for j in range(len(teamlist)):
        if j % 2 == 0:
            player = teamlist[j]
            await bot.move_member(player, channel)
bot.run("ENTER ID HERE")
