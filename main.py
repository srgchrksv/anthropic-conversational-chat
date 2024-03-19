import anthropic
from fastapi import FastAPI,  Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from dotenv import load_dotenv

# load .env file with ANTHROPIC_API_KEY
load_dotenv() 

# prompt message structure
class Prompt(BaseModel):
     prompt: str

# chat history
class MessagesHistory:
    def __init__(self):
        self.messages = []

    def append_message(self, role, message):
        self.messages.append({
            "role": role,
            "content": [
                {
                    "type": "text",
                    "text": message
                }
            ]
        })

    def get_messages(self):
        return self.messages

# init fastapi and chat historu
app = FastAPI()
messagesHistory  = MessagesHistory()

# mouunt static folder and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="static/templates")



async def anthropic_request(prompt, messages=[]):
    '''anthropic_request makes request to anthropic api'''
    client = anthropic.Anthropic(
        # defaults to os.environ.get("ANTHROPIC_API_KEY")
    )
    print(messagesHistory.get_messages())
    messagesHistory.append_message('user', prompt)
    message = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=1000,
        temperature=0,
        messages=messagesHistory.get_messages()
    )
    response = message.content[0].text
    messagesHistory.append_message('assistant', response)

    return response


# a example of response to test the markdown rendeing on the frontend
response = '''To write a simple Python function, follow this syntax:

```python
def function_name(parameters):
    # function body
    # do something
    return result
```

1. Use the `def` keyword followed by the function name and parentheses `()`.
2. If needed, specify parameters inside the parentheses.
3. Add a colon `:` after the parentheses.
4. Indent the function body with 4 spaces or a tab.
5. Write the code inside the function body.
6. Use the `return` statement to send a result back (optional).

Example:

```python
def greet(name):
    return f"Hello, {name}!"
'''


# router and handlers 
@app.get("/",response_class=HTMLResponse)
async def home(request: Request):
     messages = messagesHistory.get_messages()
    #  print(dict_messages)
     return templates.TemplateResponse(request=request,name='index.html', context={'messages':messages})

# handles the prompt request
@app.post('/api/prompt')
async def handle_prompt(prompt: Prompt):
    response = await  anthropic_request(prompt.prompt)
    return {'response' : response, 'status': 200}

#  get chat histroy
@app.get('/api/history')
async def get_history():
    return {'response': messagesHistory.get_messages()}
