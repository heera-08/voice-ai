from dotenv import load_dotenv
load_dotenv()

import os
import logging
from flask import Flask, request, Response
import plivo
from livekit import api
import xml.etree.ElementTree as ET

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

active_calls = {}

@app.route('/answer/', methods=['POST'])
def handle_answer():
    try:
        call_uuid = request.form.get('CallUUID')
        from_number = request.form.get('From')
        to_number = request.form.get('To')
        
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
        Hello! Please hold while we connect you to our AI assistant Chloe.
    </Speak>
    <Dial>
        <Sip>
            sip:{room_name}@{get_livekit_sip_domain()}/
        </Sip>
    </Dial>
</Response>"""
        
        return Response(response_xml, mimetype='text/xml')
        
    except Exception as e:
        logger.error(f"Error handling answer webhook: {e}")
        error_xml = """<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Speak voice="WOMAN">
        Sorry, we're experiencing technical difficulties. Please try again later.
    </Speak>
    <Hangup/>
</Response>"""
        return Response(error_xml, mimetype='text/xml')

@app.route('/hangup/', methods=['POST'])
def handle_hangup():
    try:
        call_uuid = request.form.get('CallUUID')
        hangup_cause = request.form.get('HangupCause')
        
        logger.info(f"Call ended - UUID: {call_uuid}, Cause: {hangup_cause}")
        
        if call_uuid in active_calls:
            call_info = active_calls.pop(call_uuid)
            logger.info(f"Cleaned up call: {call_info}")
            
        return "OK", 200
        
    except Exception as e:
        logger.error(f"Error handling hangup webhook: {e}")
        return "Error", 500

@app.route('/make_call/', methods=['POST'])
def make_outbound_call():
    try:
        target_number = request.json.get('to_number') or os.getenv('TARGET_PHONE_NUMBER')
        
        if not target_number:
            return {"error": "No target phone number provided"}, 400
        
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
        
        logger.info(f"Outbound call initiated: {response}")
        
        return {
            "success": True,
            "call_uuid": response.call_uuid,
            "message": f"Call initiated to {target_number}"
        }
        
    except Exception as e:
        logger.error(f"Error making outbound call: {e}")
        return {"error": str(e)}, 500

@app.route('/status/', methods=['GET'])
def get_status():
    return {
        "active_calls": len(active_calls),
        "calls": list(active_calls.keys())
    }

def get_livekit_sip_domain():
    ws_url = os.getenv('LIVEKIT_WS_URL', '')
    domain = ws_url.replace('wss://', '').replace('ws://', '')
    return domain

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8000))
    app.run(host='0.0.0.0', port=port, debug=True)
