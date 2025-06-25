from quart import Quart, request, Response
import plivo
import logging
from dotenv import load_dotenv
import os

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Quart(__name__)
active_calls = {}

@app.route('/answer/', methods=['POST'])
async def handle_answer():
    try:
        form = await request.form
        call_uuid = form.get('CallUUID')
        from_number = form.get('From')
        to_number = form.get('To')
        
        logger.info(f"Call answered - UUID: {call_uuid}, From: {from_number}, To: {to_number}")
        
        room_name = f"call-{call_uuid}"
        active_calls[call_uuid] = {
            'room_name': room_name,
            'from_number': from_number,
            'to_number': to_number
        }
        
        response_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Speak voice="WOMAN">
        Hello! Please hold while we connect you to our AI assistant.
    </Speak>
    <Dial>
        <Sip>sip:{room_name}@{os.getenv('LIVEKIT_SIP_DOMAIN')}/</Sip>
    </Dial>
</Response>"""
        
        return Response(response_xml, mimetype='text/xml')
    
    except Exception as e:
        logger.error(f"Error handling answer: {e}")
        return Response("""<?xml version="1.0" encoding="UTF-8"?>
<Response><Speak>Service unavailable</Speak><Hangup/></Response>""", 
        mimetype='text/xml')

@app.route('/hangup/', methods=['POST'])
async def handle_hangup():
    try:
        form = await request.form
        call_uuid = form.get('CallUUID')
        if call_uuid in active_calls:
            del active_calls[call_uuid]
        return "OK", 200
    except Exception as e:
        logger.error(f"Error handling hangup: {e}")
        return "Error", 500

@app.route('/make_call/', methods=['POST'])
async def make_outbound_call():
    try:
        data = await request.get_json()
        target_number = data.get('to_number', os.getenv('TARGET_PHONE_NUMBER'))
        
        plivo_client = plivo.RestClient(
            os.getenv('PLIVO_AUTH_ID'),
            os.getenv('PLIVO_AUTH_TOKEN')
        )
        
        response = plivo_client.calls.create(
            from_=os.getenv('PLIVO_FROM_NUMBER'),
            to=target_number,
            answer_url=f"{os.getenv('WEBHOOK_BASE_URL')}/answer/",
            answer_method='POST',
            hangup_url=f"{os.getenv('WEBHOOK_BASE_URL')}/hangup/",
            hangup_method='POST'
        )
        
        return {
            "call_uuid": response.call_uuid,
            "status": "initiated"
        }, 200
        
    except Exception as e:
        logger.error(f"Call failed: {e}")
        return {"error": str(e)}, 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
