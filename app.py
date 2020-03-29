from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, LocationSendMessage
)

app = Flask(__name__)

line_bot_api = LineBotApi('lOXlcsEO4tYTzfyesH99Uiw6BMNSNdr3OweMIsbIMQWwrLpKGkr2BKy4Vgh3vbrZdje4EEWeoMRd27kB+JxxQlaq7rOI5u8la92KvDBJ9dqPavDfJ96vchMTiQY5i7p4EUWbMZjGDlU9kHz9YRJFfQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('bde1b5cb3bb6de91d44e22dbe9c91099')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    r = '很抱歉我不懂'

    if msg == 'hi':
        r = 'hi'
    elif msg == '吃飯沒':
        r = '吃了'

    elif msg == '位置':
        r = LocationSendMessage(
        title='my location',
        address='Tokyo',
        latitude=35.65910807942215,
        longitude=139.70372892916203)
    
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=r))


if __name__ == "__main__":
    app.run()