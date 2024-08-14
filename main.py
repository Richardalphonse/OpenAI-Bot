from openai import OpenAI
from fastapi import FastAPI,Form, Request
from typing import Annotated
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from fastapi import Form
app= FastAPI()
templates= Jinja2Templates(directory='templates')

chat_log=[{'role':'system',
           'content':'you are python tutor AI.Completely dedicated to guide people in terms of learning python and its syntax'
           }]

@app.get('/',response_class=HTMLResponse)
async def chat_page(request:Request):
    return templates.TemplateResponse("home.html",{"request":request})

chat_responses=[]
@app.post('/',response_class=HTMLResponse)
async def chat(request:Request,user_input:Annotated[str,Form()]):
    chat_log.append({'role':'user','content':user_input})
    chat_responses.append(user_input)

    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=chat_log,
            temperature=.6
    )
    bot_response= response.choices[0].message.content
    chat_log.append({'role':'user','content':bot_response})
    chat_responses.append(bot_response)

    return templates.TemplateResponse("home.html",{"request":request,"chat_responses":chat_responses})

#print(response.choices[0].message.content)