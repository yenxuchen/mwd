from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, StickerSendMessage, LocationSendMessage
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

    if '貼圖' in msg:
        sticker_message = StickerSendMessage(
        package_id='1',
        sticker_id='1'
        )

        line_bot_api.reply_message(
        event.reply_token,
        sticker_message)

        return

    if msg == ['hi', 'Hi']:
        r = '嗨'
    elif msg == '吃飽了沒':
        r = '還沒'
    elif msg == '你是誰':
        r = '我是機器人'
    elif '定位' in msg:
        r = '幾位呢？'

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=r))

if __name__ == "__main__":
    app.run()