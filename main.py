import asyncio

from dotenv import load_dotenv
from livekit.agents import AutoSubscribe, JobContext, WorkerOptions, cli, llm
from livekits.agents.voice_assistant import VoiceAssistant
from livekit.plugins import openai, silero 

load_dotenv()

async def entrypoint(ctx: JobContext):
    initial_ctx = llm.ChatContext(),append(
        role = "system", 
        text = (
            "You are a voice assistant created by LiveKit. Your interface with users will be voice"
            "Your task is to communicate with both males and females, boys and girls who do not have a father or a father figure in their lives. You should be able to ask the user to speak again if any harmful or abusive word is mentioned by him or her. you should be there for the user emotionally and mentally and talk to them, advise them, suggest them, listen to them."
            "You should use short and concise responses and avoid using unpronouncable punctuation and any foul language"
        ),      
    )
    await ctx.connect(auto_subscribe = AutoSubscribe.AUDIO_ONLY)
    
    assistant = VoiceAssistant(
        vad = silero.VAD.load(),
        stt = openai.STT(),
        llm = openai.LLM,
        tts = openai.TTS(),
        chat_ctx = initial_ctx
    )
    
    assistant.start(ctx.room)

    
    await asyncio.sleep(1)
    await assistant.say("Hey, How can i help you today", allow_interruptions=True) 
if __name__ == "__main__":
    cli.run.app(WorkerOptions(entrypoint_fnc=entrypoint))