import discord
import pyttsx3
import time
from discord.ext import commands

bot = commands.Bot(command_prefix="-TTS ")
engine = pyttsx3.init()
female_voice = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0"
male_voice = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_DAVID_11.0"
user_preferences = {}

def save_user_preference(user, preference):
	with open("user_preferences.txt", "a") as file:
		file.write('\n' + str(user) + '/' + preference)

def get_user_preference():
	with open("user_preferences.txt") as file:
		for line in file:
			line = line.rstrip('\n')
			user, preference = line.split('/')
			user_preferences[user] = preference
			print(str(user) + "/" + preference)

@bot.event
async def on_ready():
	get_user_preference()
	print("TTS Bot is ready!")

@bot.command(name="ping")
async def ping_pong(context):
	await context.message.channel.send("pong!")

@bot.command(name="join")
async def join_user_vc(context):
	voice_channel_to_join = context.author.voice.channel
	await voice_channel_to_join.connect()
	await context.message.channel.send("Joined!")

@bot.command(name="leave")
async def leave_user_vc(context):
	await context.voice_client.disconnect()

@bot.command(name="say")
async def say_phrase(context, *words):
	if len(words) > 30:
		context.message.channel.send("Too many words!")
	if str(context.author.id) in user_preferences.keys():
		if user_preferences[str(context.author.id)] == "female":
			engine.setProperty('voice', female_voice)
		else:
			engine.setProperty('voice', male_voice)
	engine.save_to_file("{}".format(" ".join(words)), "voice.mp3")
	engine.runAndWait()
	guild = context.guild
	voice_client: discord.VoiceClient = discord.utils.get(bot.voice_clients, guild=guild)
	audio_source = discord.FFmpegPCMAudio(executable="C:/ffmpeg-4.3.1-2020-11-19-full_build/bin/ffmpeg.exe", source='voice.mp3')
	if not voice_client.is_playing():
		voice_client.play(audio_source, after=None)

@bot.command(name="volume")
async def set_volume(context, volume):
	if float(volume) < 0.0 or float(volume) > 1.0:
		await context.message.channel.send("Volume range is 0.0 to 1.0")
		return
	engine.setProperty("volume", float(volume))

@bot.command(name="set_voice")
async def set_voice(context, gender):
	if gender.lower() == "male":
		user_preferences[context.author.id] = "male"
		save_user_preference(context.author.id, "male")
		await context.message.channel.send("Set your voice preference to male.")
	if gender.lower() == "female":
		user_preferences[context.author.id] = "female"
		save_user_preference(context.author.id, "female")
		await context.message.channel.send("Set your voice preference to female.")

@bot.command(name="check_preference")
async def check_preference(context):
	if str(context.author.id) in user_preferences.keys():
		await context.message.channel.send("Your preference is: " + user_preferences[str(context.author.id)])
	else:
		await context.message.channel.send("No preference set.")
@bot.command(name="debug_info")
async def debug(context):
	await context.message.channel.send(user_preferences.keys())
	await context.message.channel.send(user_preferences.values())
bot.run("NzkxOTI0MjgyODYyOTkzNDQ5.X-WO9g.JXZMvhYKdo60DZfcANxktXGSj_4")