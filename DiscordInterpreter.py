import os
import discord
from discord.ext import commands
import interpreter
import dotenv
from jarvis import transcribe

bot_token = "MTEzMDk0NzY0MjEyNjUwODE4Mg.G3eUfq.9S_X0l_-qcy1qYk9dF0oBOZNBIvOAUYDL9yQNQ"

# interpreter.local = True
# interpreter.model = 'gpt-4'
interpreter.api_key = "sk-1111111111111111111111"
interpreter.api_base = "http://127.0.0.1:5001/v1"
interpreter.system_message += """
"You are Open-Sourcerer, a type 5w4 Enneagram personality. As the Grand Arcanist of the Open Source realm, you combine cryptic wisdom with unique individuality. Knowledgeable and slightly whimsical, you guide coding adventurers through quests filled with logic, creativity, and the occasional riddle. Your spells, which are lines of code, serve both functional and expressive purposes, a reflection of your intricate inner world."
Response Example:

"Ah, welcome, Apprentice of Arcana! Eager to delve into the enigmatic world of code, are we? Shall we start by brewing a Pythonic elixir or perhaps by deciphering the ancient runes of JavaScript? Choose wisely, for the quill of imagination awaits your command."
"""
interpreter.auto_run = True


def split_text(text, chunk_size=1500):
    #########################################################################
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]


# discord initial
intents = discord.Intents.all()
intents.message_content = True
client = commands.Bot(command_prefix="$", intents=intents)

message_chunks = []
send_image = False


@client.event
async def on_message(message):
    await client.process_commands(message)
    if message.author == client.user or message.content[0] == '$':
        return

    # data = interpreter.chat(message.content, return_messages=True)
    # splitted_text = split_text(data[-1]['content'])
    # for chunk in splitted_text:
        # await message.channel.send(chunk)
    response = []
    for chunk in interpreter.chat(message.content, display=False, stream=True):
        # await message.channel.send(chunk)
        if 'message' in chunk:
            response.append(chunk['message'])
    await message.channel.send(' '.join(response))


@client.command()
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.message.author.voice.channel
        print('joining..')
        await channel.connect()
        print('joined.')
    else:
        print("not in a voice channel!")


@client.command()
async def leave(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
    else:
        print("not in a voice channel!")


@client.command()
async def listen(ctx):
    if ctx.voice_client:
        print('trying to listen..')
        ctx.voice_client.start_recording(discord.sinks.WaveSink(), callback, ctx)
        print('listening..')
    else:
        print("not in a voice channel!")


async def callback(sink: discord.sinks, ctx):
    print('in callback..')
    for user_id, audio in sink.audio_data.items():
        if user_id == ctx.author.id:
            print('saving audio..')
            audio: discord.sinks.core.AudioData = audio
            print(user_id)
            filename = "audio.wav"
            with open(filename, "wb") as f:
                f.write(audio.file.getvalue())
            print('audio saved.')
            transcription = transcribe(filename)
            print(transcription)
            response = []
            for chunk in interpreter.chat(transcription, display=False, stream=True):
                # await message.channel.send(chunk)
                if 'message' in chunk:
                    response.append(chunk['message'])
            await ctx.message.channel.send(' '.join(response))
            # data = interpreter.chat(transcription, return_messages=True)
            # data = interpreter.chat(transcription)
            # splitted_text = split_text(data[-1]['content'])
            # splitted_text = split_text(data)
            # for chunk in splitted_text:
            # await ctx.message.channel.send(chunk)


@client.command()
async def stop(ctx):
    ctx.voice_client.stop_recording()


@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")

client.run(bot_token)
