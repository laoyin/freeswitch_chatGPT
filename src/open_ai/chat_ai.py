

import openai
import json
import asyncio
import websockets
from sanic import Request, Websocket
from sanic import Sanic
from sanic.response import text
from config import token

ws_app = Sanic("task-server")
ws_app.ctx.ws_dict = {}


async def chat_ai(command, ws):
    question = command["text"]
    openai.api_key = token
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[
            {'role': 'user', 'content': question}
        ],
        temperature=0,
        stream=True  # this time, we set stream=True
    )

    await ws.send("--start--")
    for chunk in response:
        data = chunk.get("choices")
        if data:
            data = data[0]
            data = data.get("delta", {}).get("content", "")
        await asyncio.sleep(0.01)
        await ws.send(data)
    await ws.send("--end--")


@ws_app.websocket("/ws")
@ws_app.exception(websockets.exceptions.ConnectionClosed)
async def ws(request: Request, ws: Websocket):
    try:
        while True:
            data = await ws.recv()
            print("Received: " + data)
            if data:
                try:
                    print(data)
                    command = json.loads(data)
                except Exception as e:
                    print(e)
                    print("what")
                if command.get("cmd", "") == "qa":
                    await chat_ai(command, ws)
                    # Authorization = command.get("Authorization")
                    # if Authorization:
                        # flag, user_message = JwtToken.parse_token(Authorization[7:])

    except websockets.exceptions.ConnectionClosed:
        # print(e)
        print("close ws")
    except asyncio.CancelledError:
        print("asyncio cancell close ws")





