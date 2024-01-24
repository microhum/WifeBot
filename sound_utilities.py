import requests
from discord.ext import commands
import discord
from discord import Intents, Message, app_commands, FFmpegPCMAudio, Spotify
import asyncio
from io import BufferedIOBase, BytesIO
import soundfile as sf
import os

def getSecDuration(sound) -> float:
    f = sf.SoundFile(sound)
    return f.frames / f.samplerate

async def join_play_sound(Interaction: discord.Interaction, sound_data: str | BufferedIOBase):
    try:
        channel = Interaction.user.voice.channel
        vc = await channel.connect()
        await Interaction.edit_original_response(content="Play Sound")
    except Exception as e:

        await Interaction.edit_original_response(content=f"Cannot join voice chat.")

    try:
        source = FFmpegPCMAudio(sound_data)
    except Exception as e:
        await Interaction.edit_original_response(content=f"Error Occured :{e}")
        return
    
    vc.play(source, after=lambda e: print('Player error: %s' % e) if e else None)

    while vc.is_playing():
        await asyncio.sleep(1)
    await Interaction.edit_original_response(content=f"Sound Finished at {getSecDuration(sound_data)}")
    await Interaction.guild.voice_client.disconnect()

async def get_speech(token: str, txt: str, speaker: int):
    Apikey= token
    
    url = 'https://api.aiforthai.in.th/vaja9/synth_audiovisual'
    headers = {'Apikey':Apikey,
            'Content-Type' : 'application/json'}
    text = f'{txt}'
    data = {'input_text':text,'speaker': speaker, 'phrase_break':0, 'audiovisual':0}
    response = requests.post(url, json=data, headers=headers)
    print(response.json())
    await asyncio.sleep(1)
    resp = requests.get(response.json()['wav_url'],headers={'Apikey':Apikey})
    if resp.status_code == 200:
        with open("speech.wav", "wb", buffering=0) as f:
            f.write(resp.content)
            return "speech.wav"

    else:
        print(resp.reason)
        