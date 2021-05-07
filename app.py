from flask import Flask, request, abort
 
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
import os
 
app = Flask(__name__)
 
# 環境変数取得
# LINE Developers: アクセストークン/ChannelSecret
CHANNEL_ACCESS_TOKEN = "XRzSUfoGJbX0k+MXADXfz2AagQXJMjUP69HXRZDQvVTq6qW7xUQi44QMmIBQrQhV1cEvTlgUXjaHMM1PlO0XaENgJRRoqyQjXC33L7f3upRS2CHOcrBOAUEx6893hxuvkAzMzUNURDWXhCb1Inj8gAdB04t89/1O/w1cDnyilFU="
CHANNEL_SECRET = "32bffe0a9a78f6b47a2b02f4c2175d21"
 
line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)
 
# Webhookからのリクエストの署名検証部分
@app.route("/callback", methods=['POST'])
def callback():
    # 署名検証のための値
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    
    # 署名検証
    try:
        handler.handle(body, signature)
    except InvalidSignatureError: # 失敗したとき エラー
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

# 以降で ボット処理内容について記載 =========================================
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text_sent_by_user = event.message.text
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=text_sent_by_user))

# ====================================================================

# python main.py　で動作
if __name__ == "__main__":
    app.run(port=5000)