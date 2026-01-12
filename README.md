# PDF to Video Automation Agent - Setup Guide

## Overview
This guide walks you through setting up the complete automation pipeline from scratch.

---

## Prerequisites

- Python 3.8 or higher
- pip package manager
- Google Cloud account (for YouTube)
- X (Twitter) Developer account
- Instagram account
- Anthropic API account

---

## Step 1: Project Setup

### 1.1 Create Project Directory
```bash
mkdir pdf-video-agent
cd pdf-video-agent
```

### 1.2 Create Virtual Environment
```bash
python -m venv venv

# Activate on macOS/Linux:
source venv/bin/activate

# Activate on Windows:
venv\Scripts\activate
```

### 1.3 Install Dependencies
```bash
pip install -r requirements.txt
```

### 1.4 Create Folder Structure
```bash
mkdir -p ~/content_dropbox/processed
mkdir -p ~/content_dropbox/failed
mkdir -p ~/videos
```

---

## Step 2: Anthropic API Setup

### 2.1 Get API Key
1. Go to https://console.anthropic.com/
2. Sign up or log in
3. Navigate to API Keys
4. Create a new API key
5. Copy the key (starts with `sk-ant-api03-`)

### 2.2 Add to Environment
```bash
# In your .env file:
ANTHROPIC_API_KEY=sk-ant-api03-xxxxx
```

---

## Step 3: YouTube API Setup

### 3.1 Create Google Cloud Project
1. Go to https://console.cloud.google.com/
2. Create a new project (e.g., "PDF Video Agent")
3. Enable YouTube Data API v3:
   - Go to "APIs & Services" > "Library"
   - Search for "YouTube Data API v3"
   - Click "Enable"

### 3.2 Create OAuth Credentials
1. Go to "APIs & Services" > "Credentials"
2. Click "Create Credentials" > "OAuth client ID"
3. Configure OAuth consent screen (if prompted):
   - User Type: External
   - App name: "PDF Video Agent"
   - Add your email
   - Add scopes: YouTube Data API v3
4. Create OAuth client ID:
   - Application type: Desktop app
   - Name: "PDF Video Agent"
5. Download JSON file and save as `client_secrets.json`

### 3.3 Initial OAuth Flow
```bash
# Run the script once to authenticate:
python video_agent.py

# This will:
# 1. Open a browser window
# 2. Ask you to log in to Google
# 3. Request YouTube permissions
# 4. Save credentials to youtube_token.json
```

### 3.4 Test Upload
Create a test video and upload:
```bash
# The agent will handle this automatically
# Or test manually with a sample PDF
```

---

## Step 4: X (Twitter) API Setup

### 4.1 Apply for Developer Account
1. Go to https://developer.twitter.com/
2. Sign up for a developer account
3. Create a new App
4. Apply for Elevated access (required for v1.1 endpoints)

### 4.2 Get API Credentials
1. In your app dashboard, go to "Keys and tokens"
2. Generate/copy these credentials:
   - API Key (Consumer Key)
   - API Key Secret (Consumer Secret)
   - Access Token
   - Access Token Secret
   - Bearer Token

### 4.3 Add to Environment
```bash
# In your .env file:
TWITTER_API_KEY=your_api_key
TWITTER_API_SECRET=your_api_secret
TWITTER_ACCESS_TOKEN=your_access_token
TWITTER_ACCESS_SECRET=your_access_secret
TWITTER_BEARER_TOKEN=your_bearer_token
```

### 4.4 Enable Required Permissions
In your app settings, ensure you have:
- Read and Write permissions
- (Optional) Direct Messages for DM features

---

## Step 5: Instagram Setup

### Option A: Official Instagram Graph API (Recommended for Production)

**Requirements:**
- Facebook Business account
- Instagram Business or Creator account
- Facebook Page linked to Instagram

**Setup:**
1. Go to https://developers.facebook.com/
2. Create an app with Instagram Basic Display or Instagram Graph API
3. Link your Instagram account
4. Get access token
5. Update the Instagram posting code to use Graph API

### Option B: Unofficial API (Simpler, Less Reliable)

**Setup:**
1. Use your regular Instagram credentials
2. Add to .env:
```bash
INSTAGRAM_USERNAME=your_username
INSTAGRAM_PASSWORD=your_password
```

**⚠️ Warning:** 
- Unofficial API may violate Instagram's ToS
- Risk of account suspension
- Less reliable for production
- Consider official API for business use

---

## Step 6: Video Generation Tool Setup

You need to choose and integrate a video generation tool. Options include:

### Option 1: Synthesia
1. Sign up at https://www.synthesia.io/
2. Get API key from dashboard
3. Update `VideoGenerator` class with Synthesia API calls

### Option 2: D-ID
1. Sign up at https://www.d-id.com/
2. Get API credentials
3. Implement D-ID API integration

### Option 3: Heygen
1. Sign up at https://www.heygen.com/
2. Access API documentation
3. Implement Heygen integration

### Option 4: Pictory.ai
1. Sign up at https://pictory.ai/
2. Note: May not have public API
3. Consider alternatives if API not available

### Implementation Template
```python
# In VideoGenerator.generate_video():
import requests

response = requests.post(
    'https://api.your-video-tool.com/v1/videos',
    headers={'Authorization': f'Bearer {Config.VIDEO_TOOL_API_KEY}'},
    json={
        'script': script,
        'voice': 'en-US-Professional',
        'avatar': 'business_casual',
        # Tool-specific parameters
    }
)

video_id = response.json()['id']

# Poll for completion
while True:
    status = requests.get(
        f'https://api.your-video-tool.com/v1/videos/{video_id}',
        headers={'Authorization': f'Bearer {Config.VIDEO_TOOL_API_KEY}'}
    ).json()
    
    if status['state'] == 'completed':
        video_url = status['download_url']
        break
    
    time.sleep(10)

# Download video
video_data = requests.get(video_url).content
video_path = Config.VIDEO_OUTPUT_FOLDER / f"{title}.mp4"

with open(video_path, 'wb') as f:
    f.write(video_data)

return video_path
```

---

## Step 7: Configuration

### 7.1 Create .env File
```bash
cp .env.template .env
# Edit .env with your actual credentials
```

### 7.2 Verify Configuration
```bash
# Check all required variables are set:
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print('ANTHROPIC_API_KEY:', 'SET' if os.getenv('ANTHROPIC_API_KEY') else 'MISSING')"
```

---

## Step 8: Testing

### 8.1 Test Individual Components

**Test PDF Extraction:**
```python
from pathlib import Path
from video_agent import PDFExtractor

extractor = PDFExtractor()
text = extractor.extract_text(Path('test.pdf'))
print(f"Extracted {len(text)} characters")
```

**Test Claude Processing:**
```python
from video_agent import ClaudeProcessor

processor = ClaudeProcessor()
content = processor.process("Sample text here")
print(content['title'])
```

**Test YouTube Upload:**
```python
from video_agent import YouTubeUploader
from pathlib import Path

uploader = YouTubeUploader()
url = uploader.upload(
    Path('test_video.mp4'),
    'Test Title',
    'Test Description',
    privacy_status='unlisted'  # Use unlisted for testing
)
print(url)
```

### 8.2 End-to-End Test
```bash
# Create a test PDF
# Drop it in ~/content_dropbox/
# Watch the logs

python video_agent.py
```

### 8.3 Monitor Logs
```bash
# In another terminal:
tail -f video_agent.log
```

---

## Step 9: Running in Production

### 9.1 Run as Background Service (Linux/macOS)

Create a systemd service file:
```bash
sudo nano /etc/systemd/system/pdf-video-agent.service
```

```ini
[Unit]
Description=PDF to Video Automation Agent
After=network.target

[Service]
Type=simple
User=your_username
WorkingDirectory=/path/to/pdf-video-agent
Environment="PATH=/path/to/venv/bin"
ExecStart=/path/to/venv/bin/python video_agent.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable pdf-video-agent
sudo systemctl start pdf-video-agent
sudo systemctl status pdf-video-agent
```

### 9.2 Run with Screen (Simple Alternative)
```bash
screen -S video-agent
python video_agent.py
# Press Ctrl+A then D to detach

# Reattach with:
screen -r video-agent
```

### 9.3 Run with Docker (Advanced)
Create `Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "video_agent.py"]
```

Build and run:
```bash
docker build -t pdf-video-agent .
docker run -d --name video-agent \
  -v ~/content_dropbox:/root/content_dropbox \
  -v ~/videos:/root/videos \
  --env-file .env \
  pdf-video-agent
```

---

## Troubleshooting

### YouTube Upload Fails
- Check quota limits (default: 6 uploads/day)
- Verify OAuth token hasn't expired
- Check video file isn't corrupted
- Ensure video meets YouTube requirements

### Twitter Posting Fails
- Verify API access level (need Elevated)
- Check character count (280 limit)
- Ensure app has write permissions
- Check rate limits

### Instagram Login Issues
- Enable 2FA and use app password
- Check for unusual login activity blocks
- Consider using official Graph API
- Verify account isn't restricted

### PDF Extraction Issues
- Install additional dependencies: `pip install PyMuPDF`
- Check PDF isn't password protected
- Verify PDF isn't corrupted
- Try alternative extraction library

### Claude API Errors
- Check API key is valid
- Verify account has credits
- Check for rate limiting
- Ensure request format is correct

---

## Best Practices

1. **Error Handling**: The agent moves failed files to a separate folder with error logs
2. **Logging**: All actions are logged to `video_agent.log`
3. **Privacy**: Use unlisted/private for testing YouTube uploads
4. **Rate Limits**: Be aware of API quotas and limits
5. **Security**: Never commit `.env` file to version control
6. **Monitoring**: Set up alerts for failed processing
7. **Backup**: Keep original PDFs for at least 30 days

---

## Security Checklist

- [ ] `.env` file added to `.gitignore`
- [ ] API keys never committed to repository
- [ ] YouTube OAuth tokens secured
- [ ] Instagram credentials encrypted
- [ ] File permissions properly set (600 for .env)
- [ ] Logs don't contain sensitive information
- [ ] Regular credential rotation implemented

---

## Maintenance

### Daily Tasks
- Check logs for errors
- Verify processing queue is clear
- Monitor API quotas

### Weekly Tasks
- Review failed files folder
- Check storage space
- Verify all integrations working

### Monthly Tasks
- Rotate API credentials
- Update dependencies: `pip install -r requirements.txt --upgrade`
- Review and archive old logs
- Backup processed files

---

## Getting Help

- **Claude API**: https://docs.anthropic.com/
- **YouTube API**: https://developers.google.com/youtube/
- **Twitter API**: https://developer.twitter.com/en/docs
- **Instagram API**: https://developers.facebook.com/docs/instagram-api/

For issues with this agent, check:
1. Log file (`video_agent.log`)
2. Error files in `failed` folder
3. Verify all environment variables are set
4. Test components individually

---

## Next Steps

After setup:
1. Drop a test PDF in `~/content_dropbox/`
2. Monitor the logs
3. Verify video appears on YouTube
4. Check Twitter and Instagram posts
5. Review the processed folder

Good luck! 🚀
