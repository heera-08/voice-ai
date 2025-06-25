# 🎯 Vuori AI Sales Assistant - Outbound Call System

A sophisticated AI-powered outbound calling system that integrates **LiveKit**, **Plivo**, **Cartesia TTS**, and **Deepgram STT** to create an intelligent sales assistant named "Chloe" for Vuori Clothing.

![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
![LiveKit](https://img.shields.io/badge/LiveKit-Real--time-green.svg)
![Plivo](https://img.shields.io/badge/Plivo-Telephony-orange.svg)
![Status](https://img.shields.io/badge/status-production--ready-brightgreen.svg)

## 🌟 Overview

This system automatically makes outbound calls to customers, connects them with an AI assistant powered by cutting-edge speech recognition, natural language processing, and text-to-speech technologies. The AI assistant "Chloe" is specifically trained to handle sales conversations, inform customers about price drops, and drive purchasing decisions for Vuori Clothing products.

### 🎯 Key Features

- **🤖 AI Sales Assistant**: Powered by Google Gemini 2.0 Flash with specialized sales training
- **📞 Automated Outbound Calling**: Seamless integration with Plivo for telephony
- **🎙️ Advanced Speech Processing**: Deepgram Nova-2 for accurate speech-to-text
- **🗣️ Natural Voice Synthesis**: Cartesia Sonic for human-like text-to-speech
- **🔊 Real-time Communication**: LiveKit for low-latency audio streaming
- **🎧 Noise Cancellation**: Built-in noise reduction for crystal-clear conversations
- **📊 Call Management**: Comprehensive logging and call lifecycle management
- **🔗 Webhook Integration**: Real-time call status updates and event handling

## 🏗️ System Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Plivo API     │    │  Webhook Server  │    │   LiveKit       │
│   (Telephony)   │◄──►│  (Flask)         │◄──►│   (Real-time)   │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                        │                       │
         │                        │                       │
         ▼                        ▼                       ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│  Customer       │    │  Call Management │    │  AI Assistant   │
│  Phone Call     │    │  & Logging       │    │  (Chloe)        │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │                       │
                                │                       ▼
                                │              ┌─────────────────┐
                                │              │  AI Services    │
                                │              │  • Deepgram STT │
                                │              │  • Google LLM   │
                                │              │  • Cartesia TTS │
                                │              │  • Silero VAD   │
                                └──────────────┤  • Noise Cancel │
                                               └─────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Active accounts with:
  - [Plivo](https://www.plivo.com/) (Telephony)
  - [LiveKit](https://livekit.io/) (Real-time communication)
  - [Google Cloud](https://cloud.google.com/) (AI/LLM)
  - [Cartesia](https://cartesia.ai/) (Text-to-Speech)
  - [Deepgram](https://deepgram.com/) (Speech-to-Text)
- Public webhook URL (ngrok, Heroku, etc.)

### 📦 Installation

1. **Clone the repository:**
```bash
git clone <repository-url>
cd vuori-ai-assistant
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Configure environment variables:**
```bash
cp .env.template .env
# Edit .env with your actual credentials
```

4. **Set up webhook server:**
```bash
# Option 1: Using ngrok (for development)
ngrok http 8000

# Option 2: Deploy to cloud service (recommended for production)
# Deploy webhook_server.py to Heroku, AWS, etc.
```

5. **Run the system:**
```bash
python complete_runner.py
```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the root directory with the following variables:

```bash
# Plivo Configuration
PLIVO_AUTH_ID=your_plivo_auth_id
PLIVO_AUTH_TOKEN=your_plivo_auth_token
PLIVO_FROM_NUMBER=+1234567890          # Your Plivo phone number
TARGET_PHONE_NUMBER=+0987654321        # Number to call (your test number)

# LiveKit Configuration
LIVEKIT_API_KEY=your_livekit_api_key
LIVEKIT_API_SECRET=your_livekit_api_secret
LIVEKIT_WS_URL=wss://your-livekit-server.livekit.cloud

# AI Service API Keys
GOOGLE_API_KEY=your_google_api_key
CARTESIA_API_KEY=your_cartesia_api_key
DEEPGRAM_API_KEY=your_deepgram_api_key

# Webhook Server Configuration
WEBHOOK_BASE_URL=https://your-webhook-server.com
PORT=8000
```

### 🔑 API Key Setup Guide

#### 1. Plivo Setup
1. Sign up at [Plivo Console](https://console.plivo.com/)
2. Purchase a phone number for outbound calling
3. Set up outbound trunk (if required)
4. Get Auth ID and Auth Token from dashboard

#### 2. LiveKit Setup
1. Create account at [LiveKit Cloud](https://cloud.livekit.io/)
2. Create a new project
3. Generate API Key and Secret
4. Note your WebSocket URL

#### 3. Google Cloud Setup
1. Create project in [Google Cloud Console](https://console.cloud.google.com/)
2. Enable Generative AI API
3. Create service account and download JSON key
4. Set `GOOGLE_APPLICATION_CREDENTIALS` or use API key

#### 4. Cartesia Setup
1. Sign up at [Cartesia](https://cartesia.ai/)
2. Get API key from dashboard
3. Note voice ID: `78ab82d5-25be-4f7d-82b3-7ad64e5b85b2`

#### 5. Deepgram Setup
1. Create account at [Deepgram](https://deepgram.com/)
2. Get API key from console
3. Verify Nova-2 model access

## 📁 Project Structure

```
voice-ai-assistant/
├── main-agent.py          # Main application orchestrator
├── webhook_server.py           # Plivo webhook handler
├── requirements.txt            # Python dependencies
├── .env.template              # Environment variables template
├── .env                       # Your actual environment variables (not in git)
├── README.md                  # This documentation
├── logs/                      # Application logs (auto-created)
└── tests/                     # Unit tests (optional)
    ├── test_webhooks.py
    ├── test_plivo_integration.py
    └── test_livekit_integration.py
```

## 🔧 Component Details

### 1. Main Application 

The central orchestrator that:
- Initializes all services and validates configuration
- Starts the webhook server in a background thread
- Triggers outbound calls automatically
- Manages the LiveKit agent worker
- Handles system-wide error management and logging

**Key Classes:**
- `VuoriAssistant`: The AI agent with sales-specific instructions
- `OutboundCallSystem`: Manages Plivo call initiation
- Main coordination functions for system startup

### 2. Webhook Server (`webhook_server.py`)

Flask-based server handling Plivo webhooks:

**Endpoints:**
- `POST /answer/`: Handles call answer events, bridges to LiveKit
- `POST /hangup/`: Manages call termination and cleanup
- `POST /make_call/`: API endpoint to trigger outbound calls
- `GET /status/`: Returns system status and active calls

**Features:**
- XML response generation for Plivo call flow
- Room management and cleanup
- Call logging and monitoring
- Error handling and recovery

### 3. AI Assistant Configuration

**Speech-to-Text (Deepgram):**
- Model: Nova-2 (latest, most accurate)
- Language: English (US)
- Features: Smart formatting, interim results
- Optimized for sales conversations

**Large Language Model (Google Gemini):**
- Model: Gemini 2.0 Flash Experimental
- Temperature: 0.8 (balanced creativity/consistency)
- Specialized instructions for sales conversations
- Trained to handle Vuori-specific scenarios

**Text-to-Speech (Cartesia):**
- Model: Sonic Multilingual
- Voice: Professional female voice
- Language: English
- Optimized for clear, friendly communication

**Voice Activity Detection (Silero):**
- Real-time voice detection
- Minimizes false triggers
- Optimized for telephony audio quality

## 🔄 Call Flow Process

### 1. System Initialization
```
┌─────────────────────────────────────────────────────────────┐
│ 1. Load environment variables and validate configuration    │
│ 2. Start webhook server (Flask) in background thread       │
│ 3. Initialize LiveKit agent worker                         │
│ 4. Start outbound call trigger (5-second delay)           │
└─────────────────────────────────────────────────────────────┘
```

### 2. Outbound Call Initiation
```
┌─────────────────────────────────────────────────────────────┐
│ 1. Plivo API call to TARGET_PHONE_NUMBER                   │
│ 2. Set webhook URLs for answer/hangup events               │
│ 3. Call placed and ringing                                 │
└─────────────────────────────────────────────────────────────┘
```

### 3. Call Answer and Bridge
```
┌─────────────────────────────────────────────────────────────┐
│ 1. Customer answers → Plivo sends webhook to /answer/      │
│ 2. Generate unique LiveKit room (call-{uuid})              │
│ 3. Return XML to bridge call to LiveKit SIP endpoint       │
│ 4. Customer connected to LiveKit room                      │
└─────────────────────────────────────────────────────────────┘
```

### 4. AI Assistant Engagement
```
┌─────────────────────────────────────────────────────────────┐
│ 1. LiveKit agent joins room automatically                  │
│ 2. AI Assistant "Chloe" generates initial greeting         │
│ 3. Real-time conversation begins:                          │
│    • Customer speech → Deepgram STT                        │
│    • Text → Google Gemini LLM                              │
│    • Response → Cartesia TTS                               │
│    • Audio → Customer via Plivo                            │
└─────────────────────────────────────────────────────────────┘
```

### 5. Call Termination
```
┌─────────────────────────────────────────────────────────────┐
│ 1. Customer hangs up → Plivo sends webhook to /hangup/     │
│ 2. Clean up LiveKit room and connections                   │
│ 3. Log call details and duration                           │
│ 4. System ready for next call                              │
└─────────────────────────────────────────────────────────────┘
```

## 🎯 AI Assistant Behavior

### Sales Persona: "Chloe"
- **Role**: Professional Vuori sales assistant
- **Personality**: Friendly, concise, helpful
- **Expertise**: Product knowledge, pricing, customer service
- **Boundaries**: Sales-focused, won't answer unrelated queries

### Conversation Strategy
1. **Opening**: Warm greeting and value proposition
2. **Engagement**: Listen to customer needs and concerns
3. **Information**: Provide relevant product and pricing details
4. **Closing**: Guide toward purchase decision or next steps

### Sample Conversation Flow
```
Chloe: "Hi! This is Chloe, your AI assistant from Vuori Clothing. 
       May I have a moment of your time? We have some exciting news 
       about a product you were interested in."

Customer: "Sure, what's the news?"

Chloe: "Great! We've reduced the price on the [Product Name] you were 
       checking out. The new price is [X]% off the original price. 
       Would you like to know more about this offer?"

[Conversation continues based on customer responses...]
```

## 📊 Monitoring and Logging

### Log Levels and Categories

**INFO Level:**
- System startup and shutdown events
- Call initiation and termination
- Successful API calls and responses
- Room creation and cleanup

**ERROR Level:**
- API failures and network issues
- Authentication problems
- Call routing failures
- Unexpected system errors

**DEBUG Level:**
- Detailed API request/response data
- Internal state changes
- Performance metrics
- Webhook payload details

### Log File Structure
```
logs/
├── system.log              # General system events
├── calls.log               # Call-specific events
├── webhooks.log            # Webhook request/response logs
├── ai_assistant.log        # AI conversation logs
└── errors.log              # Error-only logs
```

### Monitoring Endpoints

**System Health:**
```bash
GET /status/
Response: {
  "active_calls": 2,
  "calls": ["call-uuid-1", "call-uuid-2"],
  "uptime": "2h 15m",
  "last_call": "2024-01-15T10:30:00Z"
}
```

## 🚨 Troubleshooting

### Common Issues and Solutions

#### 1. Environment Variable Issues
```bash
# Error: Missing required environment variables
# Solution: Verify all required variables are set
python -c "import os; print([k for k in ['PLIVO_AUTH_ID', 'LIVEKIT_API_KEY'] if not os.getenv(k)])"
```

#### 2. Webhook Connectivity Issues
```bash
# Error: Plivo cannot reach webhook endpoints
# Solution: Ensure webhook URL is publicly accessible
curl -X POST https://your-webhook-url.com/status/
```

#### 3. LiveKit Connection Issues
```bash
# Error: Cannot connect to LiveKit room
# Solution: Verify LiveKit credentials and URL
# Check: WebSocket URL format (wss://domain.livekit.cloud)
```

#### 4. Call Quality Issues
```bash
# Issue: Poor audio quality or delays
# Solutions:
# - Check internet connection stability
# - Verify Plivo trunk configuration
# - Test with different phone numbers
# - Check LiveKit server region
```

#### 5. AI Response Issues
```bash
# Issue: AI not responding or giving generic responses
# Solutions:
# - Verify all AI service API keys
# - Check API usage limits and quotas
# - Review conversation logs for errors
# - Test individual AI services separately
```

### Debug Mode

Enable debug logging:
```python
# In complete_runner.py, change logging level:
logging.basicConfig(level=logging.DEBUG)
```

Test individual components:
```bash
# Test Plivo connection
python -c "import plivo; client = plivo.RestClient('AUTH_ID', 'AUTH_TOKEN'); print(client.accounts.get())"

# Test LiveKit connection
python -c "from livekit import api; print('LiveKit OK')"

# Test webhook server
python webhook_server.py
# In another terminal:
curl -X GET http://localhost:8000/status/
```

## 🔒 Security Considerations

### API Key Protection
- Never commit `.env` files to version control
- Use environment variables in production
- Rotate API keys regularly
- Implement API key validation

### Webhook Security
- Validate Plivo webhook signatures
- Use HTTPS for all webhook endpoints
- Implement rate limiting
- Log all webhook requests for audit

### Call Privacy
- Log minimal personal information
- Implement call recording compliance
- Follow GDPR/CCPA guidelines
- Secure call logs and transcripts

### Network Security
- Use TLS/SSL for all connections
- Implement firewall rules
- Monitor for suspicious activity
- Regular security audits

## 📈 Performance Optimization

### Scaling Considerations

**Horizontal Scaling:**
- Deploy multiple webhook server instances
- Use load balancer for webhook distribution
- Implement Redis for shared call state
- Scale LiveKit agents based on call volume

**Vertical Scaling:**
- Optimize for high-concurrency scenarios
- Use connection pooling for API calls
- Implement caching for frequently accessed data
- Monitor memory and CPU usage

### Performance Metrics

**Key Performance Indicators:**
- Call connection time (target: <3 seconds)
- AI response latency (target: <1 second)
- Call quality score (target: >4.0/5.0)
- System uptime (target: 99.9%)

**Monitoring Tools:**
- LiveKit metrics dashboard
- Plivo call analytics
- Custom performance logging
- External monitoring services

## 🧪 Testing

### Unit Tests
```bash
# Run all tests
python -m pytest tests/

# Run specific test categories
python -m pytest tests/test_webhooks.py
python -m pytest tests/test_plivo_integration.py
python -m pytest tests/test_livekit_integration.py
```

### Integration Tests
```bash
# Test full call flow (requires all services)
python tests/integration_test.py

# Test webhook endpoints
python tests/test_webhook_endpoints.py
```

### Manual Testing Checklist

- [ ] Environment variables loaded correctly
- [ ] Webhook server starts and responds
- [ ] Outbound call initiates successfully
- [ ] Call connects to LiveKit room
- [ ] AI assistant generates initial greeting
- [ ] Speech recognition works accurately
- [ ] AI responses are relevant and helpful
- [ ] Text-to-speech is clear and natural
- [ ] Call terminates gracefully
- [ ] Logs are generated correctly

## 🚀 Deployment

### Development Environment
```bash
# Local development with ngrok
ngrok http 8000
# Update WEBHOOK_BASE_URL in .env
python complete_runner.py
```

### Production Deployment

**Option 1: Heroku**
```bash
# Deploy webhook server
git add .
git commit -m "Deploy webhook server"
git push heroku main

# Set environment variables
heroku config:set PLIVO_AUTH_ID=your_auth_id
heroku config:set LIVEKIT_API_KEY=your_api_key
# ... (set all required variables)
```

**Option 2: AWS/Docker**
```dockerfile
# Dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "complete_runner.py"]
```

**Option 3: Google Cloud Run**
```yaml
# cloudbuild.yaml
steps:
- name: 'gcr.io/cloud-builders/docker'
  args: ['build', '-t', 'gcr.io/$PROJECT_ID/vuori-assistant', '.']
- name: 'gcr.io/cloud-builders/docker'
  args: ['push', 'gcr.io/$PROJECT_ID/vuori-assistant']
```

### Environment-Specific Configuration

**Development:**
- Use ngrok for webhook URLs
- Enable debug logging
- Use test phone numbers
- Lower call volumes

**Staging:**
- Production-like environment
- Real API endpoints
- Limited call volumes
- Comprehensive testing

**Production:**
- Secure webhook endpoints
- Production API keys
- Full call volumes
- 24/7 monitoring

## 📚 API Reference

### Webhook Endpoints

#### POST /answer/
Handles call answer events from Plivo.

**Request Body (Form Data):**
```
CallUUID: string          # Unique call identifier
From: string              # Caller's phone number
To: string                # Called phone number
CallStatus: string        # Current call status
```

**Response:**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Speak voice="WOMAN">
        Hello! Please hold while we connect you to our AI assistant Chloe.
    </Speak>
    <Dial>
        <Sip>sip:room-name@domain.livekit.cloud/</Sip>
    </Dial>
</Response>
```

#### POST /hangup/
Handles call termination events.

**Request Body (Form Data):**
```
CallUUID: string          # Unique call identifier
HangupCause: string       # Reason for call termination
CallDuration: integer     # Call duration in seconds
```

**Response:**
```
HTTP 200 OK
"Call terminated successfully"
```

#### POST /make_call/
Programmatically trigger outbound calls.

**Request Body (JSON):**
```json
{
  "to_number": "+1234567890",
  "caller_name": "Vuori Assistant"
}
```

**Response:**
```json
{
  "success": true,
  "call_uuid": "12345678-1234-1234-1234-123456789012",
  "message": "Call initiated to +1234567890"
}
```

#### GET /status/
Get current system status.

**Response:**
```json
{
  "active_calls": 2,
  "calls": ["call-uuid-1", "call-uuid-2"],
  "uptime": "2h 15m",
  "last_call": "2024-01-15T10:30:00Z",
  "version": "1.0.0"
}
```

## 🤝 Contributing

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Set up development environment
4. Make changes and test thoroughly
5. Submit pull request

### Code Standards
- Follow PEP 8 style guidelines
- Add type hints for all functions
- Include docstrings for all classes and methods
- Write unit tests for new features
- Update documentation for changes

### Pull Request Process
1. Ensure all tests pass
2. Update README if needed
3. Add/update docstrings
4. Follow semantic versioning
5. Request review from maintainers

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **LiveKit Team** for the excellent real-time communication platform
- **Plivo** for reliable telephony services
- **Cartesia** for natural-sounding text-to-speech
- **Deepgram** for accurate speech recognition
- **Google** for powerful language models
- **Open Source Community** for the foundational libraries

## 📞 Support

### Documentation
- [LiveKit Documentation](https://docs.livekit.io/)
- [Plivo API Reference](https://www.plivo.com/docs/)
- [Cartesia API Docs](https://docs.cartesia.ai/)
- [Deepgram Documentation](https://developers.deepgram.com/)

### Community
- [LiveKit Discord](https://discord.gg/livekit)
- [Plivo Support](https://support.plivo.com/)
- [Stack Overflow](https://stackoverflow.com/questions/tagged/livekit)

### Issues and Bug Reports
Please report issues on our [GitHub Issues](https://github.com/your-repo/issues) page with:
- Detailed description of the problem
- Steps to reproduce
- Environment information
- Relevant log files
- Expected vs actual behavior

---

**Built with ❤️ for Vuori Clothing by the AI Development Team**

*Last updated: June 25, 2025*
