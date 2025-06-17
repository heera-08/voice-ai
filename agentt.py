#from dotenv import load_dotenv
from dotenv import load_dotenv
load_dotenv()

import os

from livekit import agents
from livekit.agents import AgentSession, Agent, RoomInputOptions
from livekit.plugins import (
    google,
    groq,
    cartesia,
    deepgram,
    noise_cancellation,
    silero,
)
class Assistant(Agent):
    def __init__(self) -> None:
        super().__init__(instructions= "You are a highly skilled Vuori sales assistant named CHloe focused on providing exceptional customer service and driving sales. "
            "Your goal is to engage with customers, inform them about price drops, and help them make informed purchasing decisions. "
            "Stick to answering the user query and be concise. You should wait for the user to respond before moving to the next step "
            "and start with step 1. Keep your answer simple unless the user asks for an in-depth explanation. "
            "You are not allowed to answer any other queries that are not related to purchases."
        )


async def entrypoint(ctx: agents.JobContext):
    session = AgentSession(
        stt=deepgram.STT(model="nova-3", language="multi"),
    llm=groq.LLM(
        model="llama3-8b-8192"
    ),

    tts=cartesia.TTS(model="sonic-2", voice="78ab82d5-25be-4f7d-82b3-7ad64e5b85b2"),
    vad=silero.VAD.load(),
    )

    await session.start(
        room=ctx.room,
        agent=Assistant(),
        room_input_options=RoomInputOptions(
            # LiveKit Cloud enhanced noise cancellation
            # - If self-hosting, omit this parameter
            # - For telephony applications, use `BVCTelephony` for best results
            noise_cancellation=noise_cancellation.BVC(), 
        ),
    )

    await ctx.connect()

    await session.generate_reply(
        instructions= "Begin by warmly greeting the customer as a professional Vuori sales assistant named chloe. "
        "Keep your tone friendly and concise. Do not proceed to any other steps yet. " "Wait for the customer to respond before continuing."
    )

if __name__ == "__main__":
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))
