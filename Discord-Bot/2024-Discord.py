import discord
import glob
import random
from dotenv import load_dotenv
import os
import asyncio
from discord.ext import commands
from discord import FFmpegPCMAudio
import spotipy
from spotipy.oauth2 import SpotifyOAuth

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

load_dotenv()
token = os.getenv("DISCORD_TOKEN")
if not token:
    raise ValueError("No DISCORD_TOKEN found in the .env file.")

# Do not print the token directly; it is sensitive.
print("Discord token loaded; starting bot...")

#pip install pynacl #this is so dicord can join vc
#pip install python-dotenv
#pip install discord.py
#pip install spotipy

#FOR GOOGLE API
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

#FOR SPOTIFY API
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
SPOTIFY_REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")

#Authenticate your credentials
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
    redirect_uri=SPOTIFY_REDIRECT_URI,
    scope="user-modify-playback-state user-read-playback-state"
))

#FOR LOCAL FILES
friends_directory = 'Friends/'
ipod_directory = 'E:\\Music-Old-IPod'
FFMPEG_PATH = os.path.join(os.path.dirname(__file__), 'FFmpeg', 'bin', 'ffmpeg.exe')

#BOT PREFIX as in this is the symbol you must enter before a command. Ex .join .play
bot = commands.Bot(command_prefix=".", intents=discord.Intents.all())

# When bot is online print ready
@bot.event
async def on_ready(): 
    print("Bot is Ready!")

@bot.event
async def on_error(event, *args, **kwargs):
    print(f"Error in event {event}:", exc_info=True)


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
async def rule(ctx, *, number):
    try:
        with open('rules.txt', 'r', encoding='utf-8') as f:
            rules = [line.rstrip("\n") for line in f if line.strip()]
    except FileNotFoundError:
        await ctx.send('rules.txt not found.')
        return

    count = len(rules)

    # check if the rule number argument is a numeric value.
    if number.isnumeric():
        idx = int(number) - 1
        if 0 <= idx < count:
            await ctx.send(rules[idx])
        else:
            await ctx.send(f'There is no rule {number}. So far there are only {count} rules.')
    # the number argument is a string so check to if string equals "all".
    elif number.lower() == "all":
        for rule_text in rules:
            await ctx.send(rule_text)
    else:
        await ctx.send('Please provide a rule number or `all`.')
@rule.error
async def greet_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("You need to type in '.rules #'")

#This command tells you what skin care you should use
@bot.command(aliases=['skinroutine','skin'])
async def skincare(ctx):
    try:
        with open('Skin_Care.txt', 'r', encoding='utf-8') as f:
            skin_routine = f.read()
    except FileNotFoundError:
        await ctx.send('Skin_Care.txt not found.')
        return

    await ctx.send(skin_routine)

#This command tells you what skin care you should use
@bot.command(aliases=['suicide'])
async def kms(ctx):
    try:
        with open('happy.txt', 'r', encoding='utf-8') as f:
            lines = f.readlines()
            selected_line = random.choice(lines).strip()

    except FileNotFoundError:
        await ctx.send('happy.txt not found.')
        return

    await ctx.send(selected_line)


#This is just to show a picture of coconut. you can type .theboy or .cocoboy
@bot.command(aliases=["theboy","cocoboy"])
async def coconut(ctx):
    await ctx.send(file=discord.File('coconut.png'))

# This command goes inside the directory declare above "friends" and pics a picture open up randomly
# Though its odd because I dont specify the file type, it just opens up that file regardless 
#
# files = [f for f in files if os.path.isfile(os.path.join(directory, f))] 
#
# line 64 filters out directories and keeps only files so it opens only files
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
    if not ctx.author.voice:
        return await ctx.send('You gotta be in VC so I can join panget!')

    if ctx.voice_client and ctx.voice_client.is_connected():
        return await ctx.send('I am already in a voice channel.')

    channel = ctx.message.author.voice.channel
    await channel.connect()
    await asyncio.sleep(0.5)  # Wait for the voice client to be fully connected

    # if you check ffmpeg --version it will not show up. You need to add it to the path or point to the executable.
    hello_mp3_path = os.path.join(os.path.dirname(__file__), 'music', 'hello.mp3')
    source = FFmpegPCMAudio(hello_mp3_path, executable=FFMPEG_PATH)  # Plays this audio upon joining
    ctx.voice_client.play(source)

#(PART 3) Make discord bot leave VC
@bot.command(pass_context = True)
async def leave(ctx):
    if ctx.voice_client:
        await ctx.guild.voice_client.disconnect()
        await ctx.send('Adios :)')
    else:
        await ctx.send('Something went wrong and I cant leave')

#(PART 4) Play a song in VC
@bot.command(pass_context = True)
async def play(ctx, *, search: str = None):
    if not search:
        return await ctx.send("Please provide a song name, like `.play song_name`.")

    if not ctx.author.voice:
        return await ctx.send("You need to join a voice channel first.")

    if ctx.voice_client is None:
        return await ctx.send("I'm not connected to a voice channel. Use `.join` first.")

    # Search for file (case-insensitive match)
    files = glob.glob(os.path.join(ipod_directory, "*.mp3"))
    match = next((f for f in files if search.lower() in os.path.basename(f).lower()), None)

    if not match:
        return await ctx.send(f"No matching MP3 found for `{search}`.")
    
    source = discord.FFmpegPCMAudio(match, executable=FFMPEG_PATH)
    ctx.voice_client.stop()  # stop any current audio
    ctx.voice_client.play(source)

    await ctx.send(f"Now playing: `{os.path.basename(match)}`")

#USEFUL debugging command. This command counts the number of arguements passed to arg.
@bot.command()
async def arg(ctx,*args):
    await ctx.send('{} arguments: {}'.format(len(args), ', '.join(args)))






# PLEASE READ THIS
### EMAIL ###
# THIS command goes to my email, looks for emails from steam and prints the first few lines


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





# PLEASE READ
### SPOTIFY ###
# This feature allows you to control your spotify with your discord bot
# It unfortunately cannot play music through discord


@bot.command(name="playsp")
async def playsp(ctx, *, query: str):
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
async def pausesp(ctx):
    """Pause playback on Spotify"""
    sp.pause_playback()
    await ctx.send("Playback paused.")

@bot.command(name="resume")
async def resumesp(ctx):
    """Resume playback on Spotify"""
    sp.start_playback()
    await ctx.send("Playback resumed.")

@bot.command(name="skip")
async def skipsp(ctx):
    """Skip to the next song"""
    sp.next_track()
    await ctx.send("Skipped to the next track.")
    
bot.run(token)
