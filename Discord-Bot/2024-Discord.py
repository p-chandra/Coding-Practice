import discord
import random
from dotenv import load_dotenv
import os
from discord.ext import commands
from discord import FFmpegPCMAudio
import spotipy
from spotipy.oauth2 import SpotifyOAuth

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

load_dotenv()
token = os.getenv("DISCORD_TOKEN")
if not token:
    raise ValueError("No DISCORD_TOKEN found in the .env file.")

# Use the token
print(token)

#pip install pynacl #this is so dicord can join vc
#pip install python-dotenv
#pip install discord.py
#pip install spotipy

#FOR GOOGLE API
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

#FOR SPOTIFY API
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
SPOTIFY_REDIRECT_URI = "http://localhost:8080"

#Authenticate your credentials
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
    redirect_uri=SPOTIFY_REDIRECT_URI,
    scope="user-modify-playback-state user-read-playback-state"
))

#FOR LOCAL FILES
friends_directory = 'Friends/'
music_directory = 'music/'

#BOT PREFIX as in this is the symbol you must enter before a command. Ex .join .play
bot = commands.Bot(command_prefix=".", intents=discord.Intents.all())

# When bot is online print ready
@bot.event
async def on_ready(): 
    print("Bot is Ready!")


# This command responds to the user who says hello
@bot.command()
async def hello(ctx):
    username = ctx.author # this is your unique discord tag so ucdropout
    username = ctx.author.display_name # this will use your server name so Evo
    username = ctx.author.mention # this will @ your server name so @Evo
    await ctx.send(f'Hello, {username}')


# aliases just means that you can call this function with other names. 
# In this case I gave the aliase a list of names I can use to call this function
@bot.command(aliases=["gm","morning"]) 
async def goodmorning(ctx):
    await ctx.send(f"Good Morning, {ctx.author.mention}!")

# This command displays the rules for the server.
@bot.command(aliases=['rules'])
async def rule(ctx,*,number):
    # Reading Rules from a text file.
    f = open('rules.txt', 'r')
    rules = f.readlines()
    with open('rules.txt') as f:
        count = sum(1 for _ in f)

    # check if the rule number arguement is a numeric value.
    if (number.isnumeric()):
        if (int(number) < count+1):
            await ctx.send(rules[int(number)-1])
        else:
            await ctx.send(f'There is no rule {number}. So far there are only {count} rules.')
    # the number argument is a string so check to if string equals "all".
    elif ((number) == "all"):
        for x in range(count):
            await ctx.send(rules[x])
    else:
        await ctx.send('I see you are trying to test my code... stop it.')

#This command tells you what skin care you should use
@bot.command(aliases=['skinroutine','skin'])
async def skincare(ctx):
    f = open('Skin_Care.txt', 'r')
    skin_routine = f.read()
    await ctx.send(skin_routine)

#This is just to show a picture of coconut. you can type .theboy or .cocoboy
@bot.command(aliases=["theboy","cocoboy"])
async def coconut(ctx):
    await ctx.send(file=discord.File('coconut.png'))

# This command goes inside the directory declare above "koopa" and pics a picture open up randomly
# Though its odd because I dont specify the file type, it just opens up that file regardless 
#
# files = [f for f in files if os.path.isfile(os.path.join(directory, f))] 
#
# line 64 fliters out directories and keeps only files so it opens only files
@bot.command()
async def friends(ctx):
    files = os.listdir(friends_directory)
    random_file = random.choice(files)
    with open(os.path.join(friends_directory, random_file), 'rb') as f:
        picture = discord.File(f)
        await ctx.send(file=picture)

#(PART 1) This command goes to my local folder and plays a song
@bot.command()
async def music(ctx):
    files = os.listdir(music_directory)
    random_file = random.choice(files)
    with open(os.path.join(music_directory, random_file), 'rb') as f:
        picture = discord.File(f)
        await ctx.send(file=picture)

#(PART 2) Have discord bot join VC. Note you must be in VC for it to join
@bot.command(pass_context = True)
async def join(ctx):
    if (ctx.author.voice):
        channel = ctx.message.author.voice.channel
        voice = await channel.connect()
        source = FFmpegPCMAudio('1.mp3')
        player = voice.play(source)
    else:
        await ctx.send('You gotta be in VC so I can join panget!')

#(PART 3) Make discord bot leave VC
@bot.command(pass_context = True)
async def leave(ctx):
    if (ctx.voice_client):
        await ctx.guild.voice_client.disconnect()
        await ctx.send('Adios :)')
    else:
        await ctx.send('Something went wrong and I cant leave')

#USEFUL debugging command. This command counts the number of arguements passed to arg.
@bot.command()
async def arg(ctx,*args):
    await ctx.send('{} arguments: {}'.format(len(args), ', '.join(args)))

#THIS command goes to my email, looks for emails from steam and prints the first few lines
@bot.command()
async def email(ctx):
    # Define the scope for Gmail API
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    query = f'subject:"{"Steam"}"'
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        # Call the Gmail API
        service = build("gmail", "v1", credentials=creds)
        results = service.users().messages().list(userId="me", q=query, maxResults=1).execute()
        messages = results.get('messages', [])

        if not messages:
            await ctx.send('No emails found')
            return

        latest_message_id = messages[0]['id']
        msg = service.users().messages().get(userId='me', id=latest_message_id).execute()

        # Extract and print email details
        headers = msg['payload'].get('headers', [])
        subject = next((header['value'] for header in headers if header['name'] == 'Subject'), "No Subject")
        snippet = msg.get('snippet', '')

        await ctx.send(f"Subject: {subject}")
        await ctx.send(f"Snippet: {snippet}")
        # Reading all emails associated with the subject
        #for message in messages:
        #    msg = service.users().messages().get(userId='me', id=message['id']).execute()
        #    headers = msg['payload'].get('headers', [])
        #    for header in headers:
        #        if header['name'] == 'Subject':
        #            print(f"Subject: {header['value']}")
        #    snippet = msg.get('snippet', '')
        #    print(f"Snippet: {snippet}")

    except HttpError as error:
        await ctx.send(f"An error occurred: {error}")

@bot.command(name="play")
async def play(ctx, *, query: str):
    """Play a song on Spotify"""
    results = sp.search(q=query, type="track", limit=1)
    if results["tracks"]["items"]:
        track = results["tracks"]["items"][0]
        track_uri = track["uri"]
        
        devices = sp.devices()
        if not devices["devices"]:
            await ctx.send("No active Spotify device found. Open Spotify on a device.")
            return
        
        device_id = devices["devices"][0]["id"]
        sp.start_playback(device_id=device_id, uris=[track_uri])

        await ctx.send(f"Now playing: {track['name']} by {track['artists'][0]['name']}")
    else:
        await ctx.send("Song not found.")

@bot.command(name="pause")
async def pause(ctx):
    """Pause playback on Spotify"""
    sp.pause_playback()
    await ctx.send("Playback paused.")

@bot.command(name="resume")
async def resume(ctx):
    """Resume playback on Spotify"""
    sp.start_playback()
    await ctx.send("Playback resumed.")

@bot.command(name="skip")
async def skip(ctx):
    """Skip to the next song"""
    sp.next_track()
    await ctx.send("Skipped to the next track.")
    
bot.run(token)
