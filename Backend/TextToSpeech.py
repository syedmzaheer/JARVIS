import pygame
import random
import asyncio
import edge_tts
import os
from dotenv import dotenv_values

env_vars = dotenv_values(".env")
AssistantVoice = env_vars.get("AssistantVoice")

async def TextToAudioFile(text) → None:
    file_path = r"Data\Speech.mp3"

    if os.path.exists(file_path):
        os.remove(file_path)
    
    communicate = edge_tts.Communicate(text, AssistantVoice, pitch='+5Hz', rate='13%')
    await communicate.save(r'Data\speech.mp3')

def     
