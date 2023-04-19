import os
from open_ai.chat_ai import ws_app
from sanic.response import html





@ws_app.route('/')
async def index(request):
    content = open(os.path.join("open_ai", "chat_ai.html"), "r").read()
    return html(content)


if __name__ == "__main__":
    ws_app.run(host="0.0.0.0", port=10889, debug=True)