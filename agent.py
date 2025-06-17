from dotenv import load_dotenv
load_dotenv()

import os

from livekit import agents
from livekit.agents import AgentSession, Agent, RoomInputOptions
from livekit.plugins import (
    # google,
    groq,
    # openai,
    cartesia,
    deepgram,
    noise_cancellation,
    silero,
)

# === Plivo integration added here ===
import plivo

PLIVO_AUTH_ID = os.getenv("PLIVO_AUTH_ID")
PLIVO_AUTH_TOKEN = os.getenv("PLIVO_AUTH_TOKEN")
PLIVO_NUMBER = os.getenv("PLIVO_NUMBER")

plivo_client = plivo.RestClient(auth_id=PLIVO_AUTH_ID, auth_token=PLIVO_AUTH_TOKEN)

def make_outbound_call(to_number: str):
    """
    Initiate an outbound call via Plivo and use a webhook to handle the call.
    """



    # Replace with your actual webhook URL that returns Plivo XML instructions
    response_url = "https://your-server.com/plivo/answer"
    


    
    call = plivo_client.calls.create(
        from_=PLIVO_NUMBER,
        to_=to_number,
        answer_url=response_url,
        answer_method='POST'
    )
    print(f"Plivo outbound call started with UUID: {call['request_uuid']}")
    return call
# === End Plivo integration ===


class Assistant(Agent):
    def __init__(self) -> None:
        super().__init__(instructions="You are a highly skilled Vuori sales assistant focused on providing exceptional customer service and driving sales. "
            "Your goal is to engage with customers, inform them about price drops, and help them make informed purchasing decisions. "
            "Stick to answering the user query and be concise. You should wait for the user to respond before moving to the next step "
            "and start with step 1. Keep your answer simple unless the user asks for an in-depth explanation. "
            "You are not allowed to answer any other queries that are not related to purchases."
        )


async def entrypoint(ctx: agents.JobContext):
    session = AgentSession(
        stt=deepgram.STT(model="nova-3", language="multi"),
        # llm= openai.LLM(
        # model="gpt-4o",
        # temperature=0.8),
    #     llm=google.LLM(
    #     model="gemini-2.0-flash-exp",
    #     temperature=0.8,
    # ),
    
    # stt=groq.STT(
    #     model="whisper-large-v3-turbo",
    #     language="en",
    # ),
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
         "Begin by warmly greeting the customer as a professional Vuori sales assistant. "
    "Keep your tone friendly and concise. Do not proceed to any other steps yet. "
    "Wait for the customer to respond before continuing.",
    "Hi! Chloe - AI Agent here from Vuori Clothing.com. May I have a moment of your time? We've reduced the price on the product you were checking out.",
    "Hello! It's Chloe - AI Agent from Vuori Clothing.com. Is now a convenient time to chat? Great news—we've dropped the price on that product you liked.",
    "Greetings! Chloe - AI Agent calling from Vuori Clothing.com. Are you available for a quick chat? We've got a new markdown on the product you were interested in.",
    "Hi there! Chloe - AI Agent from Vuori Clothing.com here. Do you have a moment to chat? We've just marked down the price on the product you were looking at.",
    "Hello! Chloe - AI Agent from Vuori Clothing.com. If it's a good time for you, I'd like to chat about the updated price on the item you were eyeing.")


if __name__ == "__main__":
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))
