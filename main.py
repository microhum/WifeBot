from typing import Final, List
from flask import Flask
from threading import Thread
from waitress import serve
from dotenv import load_dotenv
import os
from discord.ext import commands, tasks
import discord
from discord import Intents, Message, app_commands, FFmpegPCMAudio, Spotify
from responses import get_response
from sound_utilities import get_speech, join_play_sound
import asyncio
from datetime import time
import json
import requests
from itertools import cycle
from GPT3 import get_GPT_response

# Flask Server Keep Bot Alive
app = Flask(__name__)

@app.route("/")
def returnHTML():
    return "Hi, This is Wife-Bot Hosting service"

def run():
    # app.run(host="0.0.0.0", port=80)
    serve(app, host='0.0.0.0', port=80)

def keep_alive():
    server = Thread(target=run)
    server.start()
    
status = cycle(['Thinking About Puping','Miss Puping'])

@tasks.loop(seconds=10)
async def change_status(): 
    await client.change_presence(status=discord.Status.idle, activity=discord.Streaming(name=next(status), url="https://www.youtube.com/watch?v=dQw4w9WgXcQ"))

# Declare Client(Bot) Class
class Client(commands.Bot):
  def __init__(self):
    super().__init__(command_prefix="!" ,intents=Intents.all())
    load_dotenv()
    self.TOKEN : Final[str] = os.getenv('DISCORD_TOKEN')
    self.API_ENDPOINT: Final[str] = os.getenv('GPT_API_ENDPOINT')
    self.HUGGINGFACE_TOKEN: Final[str] = os.getenv('HUGGINGFACE_TOKEN')
    self.TSS_TOKEN: Final[str] = os.getenv('TSS_TOKEN')
    self.request_headers = {
            'Authorization': 'Bearer {}'.format(self.HUGGINGFACE_TOKEN)
        }
    

  def query(self, payload):
    """
    make request to the Hugging Face model API
    """
    data = json.dumps(payload)
    response = requests.request('POST',
                                self.API_ENDPOINT,
                                headers=self.request_headers,
                                data=data)
    ret = json.loads(response.content.decode('utf-8'))
    return ret
  
  async def on_ready(self):
    print(" Logged in as " + self.user.name)
    change_status.start()
    synced = await self.tree.sync()
    print(" Slash CMDs Synced "+ str(len(synced)) + " Commands")
    
client = Client()

@client.command(name="chat", description="Talking ")
async def chat(Interaction: discord.Interaction, text: str) -> None:    
    await Interaction.response.send_message(get_response(text, Interaction.user))

# @client.tree.command(name="talk", description="Talk with DialoGPT (GPT2)")
# async def talk(Interaction: discord.Interaction, text: str) -> None:
#     payload = {'inputs': {'text': text}}
#     async with Interaction.channel.typing():
#         response = client.query(payload)
#     bot_response = response.get('generated_text', None)
    
#     # we may get ill-formed response if the model hasn't fully loaded
#     # or has timed out
#     if not bot_response:
#         if 'error' in response:
#             bot_response = '`Error: {}`'.format(response['error'])
#         else:
#             bot_response = 'Hmm... something is not right.'

#     # send the model's response to the Discord channel
#     chat_dialogue = f"```{Interaction.user}: {text}\nBot: {bot_response}```"
#     await Interaction.response.send_message(chat_dialogue)

@client.tree.command(name="talk", description="Talk with ChatGPT")
async def talk(Interaction: discord.Interaction, text: str, clear: bool = False) -> None:

    async with Interaction.channel.typing():
        bot_response = get_GPT_response(message=text, IsPuping=Interaction.user == "vermillixn", clear=clear)
    

    # send the model's response to the Discord channel
    chat_dialogue = f"```{Interaction.user}: {text}\nBot: {bot_response}```"
    await Interaction.response.send_message(chat_dialogue)

@client.tree.command(name="copy", description="Talking ")
async def copy(Interaction: discord.Interaction, text: str) -> None:    
    await Interaction.response.send_message(text)

@client.tree.command(name='join', description='Join a voice channel')
async def join(Interaction: discord.Interaction) -> None:
    channel = Interaction.user.voice.channel
    await Interaction.response.send_message("Joining...", ephemeral=True)
    await channel.connect()

@client.tree.command(name='leave', description='Leave the voice channel')
async def leave(Interaction: discord.Interaction) -> None:
    await Interaction.response.send_message("Leaving...", ephemeral=True)
    await Interaction.guild.voice_client.disconnect()

@client.tree.command(name='speak', description='Speak Whatever')
async def speak(Interaction: discord.Interaction, text: str = 'สวัสดีค่ะฉันคือเมียภูพิงค์.. ฉันรักผัวของฉันมาก', speaker: int = 3) -> None:
   await Interaction.response.send_message("Trying Play Sound...", ephemeral=True)
   speech_data = await get_speech(client.TSS_TOKEN, text, speaker)
   await join_play_sound(Interaction=Interaction, sound_data=speech_data)
   
@client.tree.command(name="hee", description="Summon Hee King")
async def hee(Interaction: discord.Interaction) -> None:
    await Interaction.response.send_message("Trying Play Sound...", ephemeral=True)
    sound_path = f'assets/sounds/thanprathan.mp3'
    await join_play_sound(Interaction=Interaction, sound_data=f'{sound_path}')
    
def main() -> None:
    keep_alive()
    client.run(token=client.TOKEN)

if __name__ == '__main__':
    main()
    

