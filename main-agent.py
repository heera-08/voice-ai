from dotenv import load_dotenv
load_dotenv()

import os
import asyncio
import logging
import threading
import time
import requests
from typing import Optional
import plivo
from livekit import agents, api
from livekit.agents import AgentSession, Agent, RoomInputOptions
from livekit.plugins import (
    google,
    cartesia,
    deepgram,
    noise_cancellation,
    silero,
)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class VuoriAssistant(Agent):
    def __init__(self) -> None:
        super().__init__(
            instructions=(
                "You are a highly skilled Vuori sales assistant named Chloe focused on providing exceptional customer service and driving sales. "
                "Your goal is to engage with customers, inform them about price drops, and help them make informed purchasing decisions. "
                "Speak briefly, be friendly and do not include symbols while talking. "
                "Stick to answering the user query and be concise. You should wait for the user to respond before moving to the next step "
                "and start with step 1. Keep your answer simple unless the user asks for an in-depth explanation. "
                "You are not allowed to answer any other queries that are not related to purchases."
            )
        )

async def agent_entrypoint(ctx: agents.JobContext):
    logger.info(f"Starting agent session for room: {ctx.room.name}")
    
    try:
        session = AgentSession(
            stt=deepgram.STT(
                model="nova-2",
                language="en-US",
                smart_format=True,
                interim_results=True
            ),
            
            llm=google.LLM(
                model="gemini-2.0-flash-exp",
                temperature=0.8,
            ),
            
            tts=cartesia.TTS(
                model="sonic-multilingual",
                voice="78ab82d5-25be-4f7d-82b3-7ad64e5b85b2",
                language="en"
            ),
            
            vad=silero.VAD.load(),
        )
        
        await session.start(
            room=ctx.room,
            agent=VuoriAssistant(),
            room_input_options=RoomInputOptions(
                noise_cancellation=noise_cancellation.BVC(),
            ),
        )
        
        await ctx.connect()
        
        await asyncio.sleep(2)
        
        await session.generate_reply(
            instructions=(
                "Begin by warmly greeting the customer as a professional Vuori sales assistant named Chloe. "
                "Keep your tone friendly and concise. Do not proceed to any other steps yet. "
                "Wait for the customer to respond before continuing. "
                "Say: 'Hi! This is Chloe, your AI assistant from Vuori Clothing. May I have a moment of your time? "
                "We have some exciting news about a product you were interested in.'"
            )
        )
        
        logger.info("Initial greeting generated")
        
    except Exception as e:
        logger.error(f"Error in agent entrypoint: {e}")
        raise

class OutboundCallSystem:
    def __init__(self):
        self.plivo_client = plivo.RestClient(
            os.getenv('PLIVO_AUTH_ID'),
            os.getenv('PLIVO_AUTH_TOKEN')
        )
        self.webhook_base_url = os.getenv('WEBHOOK_BASE_URL')
        self.target_number = os.getenv('TARGET_PHONE_NUMBER')
        self.from_number = os.getenv('PLIVO_FROM_NUMBER')
        
    def make_call(self):
        try:
            logger.info(f"Making outbound call to {self.target_number}")
            
            response = self.plivo_client.calls.create(
                from_=self.from_number,
                to=self.target_number,
                answer_url=f"{self.webhook_base_url}/answer/",
                answer_method='POST',
                hangup_url=f"{self.webhook_base_url}/hangup/",
                hangup_method='POST',
                caller_name="Vuori Assistant"
            )
            
            logger.info(f"Call initiated successfully: {response}")
            return response
            
        except Exception as e:
            logger.error(f"Error making outbound call: {e}")
            raise

async def start_agent_worker():
    try:
        logger.info("Starting LiveKit agent worker")
        
        worker_options = agents.WorkerOptions(
            entrypoint_fnc=agent_entrypoint,
            ws_url=os.getenv("LIVEKIT_WS_URL"),
            api_key=os.getenv("LIVEKIT_API_KEY"),
            api_secret=os.getenv("LIVEKIT_API_SECRET"),
        )
        
        await agents.cli.run_app(worker_options)
        
    except Exception as e:
        logger.error(f"Error starting agent worker: {e}")
        raise

def start_webhook_server():
    import subprocess
    import sys
    
    logger.info("Starting webhook server")
    
    subprocess.Popen([
        sys.executable, "webhook_server.py"
    ])

def trigger_outbound_call():
    time.sleep(5)
    
    try:
        call_system = OutboundCallSystem()
        call_system.make_call()
        logger.info("Outbound call triggered successfully")
    except Exception as e:
        logger.error(f"Failed to trigger outbound call: {e}")

async def main():
    try:
        logger.info("=== Starting Vuori AI Assistant Outbound Call System ===")
        
        required_vars = [
            "PLIVO_AUTH_ID", "PLIVO_AUTH_TOKEN", "PLIVO_FROM_NUMBER", "TARGET_PHONE_NUMBER",
            "LIVEKIT_API_KEY", "LIVEKIT_API_SECRET", "LIVEKIT_WS_URL",
            "GOOGLE_API_KEY", "CARTESIA_API_KEY", "DEEPGRAM_API_KEY", "WEBHOOK_BASE_URL"
        ]
        
        missing_vars = [var for var in required_vars if not os.getenv(var)]
        if missing_vars:
            logger.error(f"Missing required environment variables: {', '.join(missing_vars)}")
            return
        
        webhook_thread = threading.Thread(target=start_webhook_server, daemon=True)
        webhook_thread.start()
        
        time.sleep(3)
        
        call_thread = threading.Thread(target=trigger_outbound_call, daemon=True)
        call_thread.start()
        
        await start_agent_worker()
        
    except KeyboardInterrupt:
        logger.info("System shutdown requested")
    except Exception as e:
        logger.error(f"System error: {e}")
        raise

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Application terminated by user")
    except Exception as e:
        logger.error(f"Application error: {e}")
