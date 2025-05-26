# reddit-summary

Small personal project to learn ML & NLP techniques. Use a pre-trained Transformer model to summarize top comments from a popular Reddit thread.

### Setup
Using python 3.11, create and activate a virtual environment and install dependencies:
```
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Create a Reddit app:
1. Login at https://www.reddit.com/prefs/apps
2. Create an app
    - Type: script
    - Redirect uri: fill in with anything (ex: `http://localhost:8080`) - won't use this, but can't leave it blank

Store credentials as environment variables:
1. Create an environment file (`.env`)
2. Populate the .env with the credentials from the Reddit app:
```
REDDIT_CLIENT_ID="<Reddit personal use script key>"
REDDIT_CLIENT_SECRET="<Reddit secret key>"
REDDIT_USER_AGENT="<platform>:<app ID>:<version string> (by u/<Reddit username>)"
```
