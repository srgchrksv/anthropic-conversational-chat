# anthropic conversational chat

I wanted to try all anthropic Claude models and created this simple client UI.

Get yor api key at [https://console.anthropic.com/](https://console.anthropic.com/)

Then create .env file with ANTHROPIC_API_KEY variable.

Install are required packages with:
```
pip install -r requirements.txt 
```
And serve client with fastapi and uvicorn:
```bash
uvicorn main:app --reload
```

MessagesHistory class to hold conversation, but only Opus model is responsive with history context other models ignore it, responding only to last prompt.

```
class MessagesHistory:
    def __init__(self):
        self.messages = []

    def append_message(self, role, message):
        self.messages.append(self.message_template(role, message))

    def get_messages(self):
        return self.messages
```