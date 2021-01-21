from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    SourceUser, SourceGroup, SourceRoom,
    TemplateSendMessage, ConfirmTemplate, MessageAction,
    ButtonsTemplate, ImageCarouselTemplate, ImageCarouselColumn, URIAction,
    PostbackAction, DatetimePickerAction,
    CameraAction, CameraRollAction, LocationAction,
    CarouselTemplate, CarouselColumn, PostbackEvent,
    StickerMessage, StickerSendMessage, LocationMessage, LocationSendMessage,
    ImageMessage, VideoMessage, AudioMessage, FileMessage,
    UnfollowEvent, FollowEvent, JoinEvent, LeaveEvent, BeaconEvent,
    MemberJoinedEvent, MemberLeftEvent,
    FlexSendMessage, BubbleContainer, ImageComponent, BoxComponent,
    TextComponent, IconComponent, ButtonComponent,
    SeparatorComponent, QuickReply, QuickReplyButton,
    ImageSendMessage
)
from langconv import Converter

app = Flask(__name__)

line_bot_api = LineBotApi('mBIw+EFCaWAUQQXEG0T+oVbStMFJNLW4ALCwGB1GHah7SY+TxjBQYhjEWNrB4/uFCquqTatbuGCepVEHhcrwMEPABK1WYv/3WIyFUBg0ddUpLeaBr05ov4Zm7n5cX3GMxfGxPHWOKAq6B7KQbToyHQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('99d6a44e0aeee2f51b66d2b601d5f34c')


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
    
# handle msg
import os
import speech_recognition as sr

def transcribe(wav_path):
    '''
    Speech to Text by Google free API
    language: en-US, zh-TW
    '''
    
    r = sr.Recognizer()
    with sr.AudioFile(wav_path) as source:
        audio = r.record(source)
    try:
        return r.recognize_google(audio,language="zh-CHT")
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
    return None


@handler.add(MessageEvent, message=AudioMessage)
def handle_audio(event):

    name_mp3 = 'recording.mp3'
    name_wav = 'recording.wav'
    message_content = line_bot_api.get_message_content(event.message.id)
    
    with open(name_mp3, 'wb') as fd:
        for chunk in message_content.iter_content():
            fd.write(chunk)
    
    os.system('ffmpeg -y -i ' + name_mp3 + ' ' + name_wav + ' -loglevel quiet')
    text = transcribe(name_wav)
    new_text = Converter('zh-hant').convert(text)
    
    print('Transcribe:', new_text)
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text = new_text))
    
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    #re = "超過回覆範圍喔! 麻煩再試試看~"

    if "最新商品消息"in msg or "商品"in msg or "消息"in msg or "最新"in msg:
        carousel_template = CarouselTemplate(columns=[
            CarouselColumn(thumbnail_image_url='https://uploads-ssl.webflow.com/575714cc825e8dbc6c83b98a/5fd9c3b6cbffe80c6574ffbe_Animal%20Upon%20Animal_X%27mas_Box_3D_DE.jpg',
                           text='聖誕節!所有的動物決定以一場堆疊友誼賽來慶祝佳節。遊戲中，誰能率先將自己所有配件疊上金字塔？', title='動物疊疊樂 聖誕金字塔',
                           actions=[
                URIAction(label='介紹影片', uri='https://www.youtube.com/watch?v=LfsPqDwt5aU&feature=emb_title&ab_channel=%E6%96%B0%E5%A4%A9%E9%B5%9D%E5%A0%A1%E6%A1%8C%E9%81%8ASwanPanasia')
                ]),
            CarouselColumn(thumbnail_image_url='https://uploads-ssl.webflow.com/575714cc825e8dbc6c83b98a/5f6d89f01b318a3b7ff66db5_Night%20of%20Witnesses_Box.jpg',
                           text='山中作客的夜晚，主人慘遭殺害！賓客能否藉由各自職業上的優勢，識破殺人魔與其共犯羅織的謊言？', title='目擊者之夜',
                           actions=[
                URIAction(label='介紹影片', uri='https://www.youtube.com/watch?v=do9kypzitus&feature=emb_title&ab_channel=%E6%96%B0%E5%A4%A9%E9%B5%9D%E5%A0%A1%E6%A1%8C%E9%81%8ASwanPanasia')
            ]),
            CarouselColumn(thumbnail_image_url='https://uploads-ssl.webflow.com/575714cc825e8dbc6c83b98a/5ab8f125ff9c8b071bceccc8_Bamboleo_Box_3D.jpg',
                           text='平衡天使是給所有重力學專家的一款極富技巧性的遊戲！參與遊戲或旁觀都十分有趣。', title='平衡天使',
                           actions=[
                URIAction(label='介紹影片', uri='https://www.youtube.com/watch?v=EmPR8leNWhk&ab_channel=%E6%96%B0%E5%A4%A9%E9%B5%9D%E5%A0%A1%E6%A1%8C%E9%81%8ASwanPanasia')
            ]),

            CarouselColumn(thumbnail_image_url='https://uploads-ssl.webflow.com/575714cc825e8dbc6c83b98a/5d1c01a5d9148d107e01c93c_BOOOOOM_Box_3D.jpg',
                           text='這是個與和平完全無關的遊戲。\n遊戲中展現弱肉強食的黑暗面，讓自己成為唯一倖存的玩家。', title='你炸我彈他',
                           actions=[
                URIAction(label='介紹影片', uri='https://www.youtube.com/watch?v=eeGmS_ZjFR8&ab_channel=%E6%96%B0%E5%A4%A9%E9%B5%9D%E5%A0%A1%E6%A1%8C%E9%81%8ASwanPanasia'),
            ]),
            CarouselColumn(thumbnail_image_url='https://uploads-ssl.webflow.com/575714cc825e8dbc6c83b98a/5e282a8b8fc29850b3980b60_CamelUp_2020_BOX.jpg',
                           text='快來見識有史以來最瘋狂的駱駝大賽！對自己看好的駱駝下注，以期在分段賽及賽終時贏得最多獎金。', title='駱駝大賽',
                           actions=[
                URIAction(label='介紹影片', uri='https://www.youtube.com/watch?v=3Iye_KoLu6M&ab_channel=%E6%96%B0%E5%A4%A9%E9%B5%9D%E5%A0%A1%E6%A1%8C%E9%81%8ASwanPanasia'),
            ])
        ])
        template_message = TemplateSendMessage(
            alt_text='Carousel alt text', template=carousel_template)
        line_bot_api.reply_message(event.reply_token, template_message)
        return

    if "店鋪位置"in msg or "位置"in msg or "店鋪"in msg:
        line_bot_api.reply_message(event.reply_token,LocationSendMessage(
            title='Enjoy Board Game Location',
            address='NCU EEIT',
            latitude=24.969388594485057,
            longitude=121.19105616458904)
        )
        return

    if "我有問題"in msg or "問題"in msg or "疑問"in msg or "QA"in msg:
        bubble = BubbleContainer(
            direction='ltr',
            hero=ImageComponent(
                url='https://img.ruten.com.tw/s1/5/5a/87/21715845113479_395.PNG',
                size='full',
                aspect_ratio='15:10',
                aspect_mode='cover',
                action=URIAction(uri='https://img.ruten.com.tw/s1/5/5a/87/21715845113479_395.PNG', label='label')
            ),
            body=BoxComponent(
                layout='vertical',
                contents=[
                    # title
                    TextComponent(text='常見問題', weight='bold', size='xl')
                        ]
                    ),
                
            footer=BoxComponent(
                layout='vertical',
                spacing='sm',
                contents=[
                    # callAction, separator, websiteAction
                    SeparatorComponent(),
                    # callAction
                    ButtonComponent(
                        style='link',
                        height='sm',
                        action=MessageAction(label='專題成員有誰?', text="專題成員有誰?"),
                    ),
                    # separator
                    SeparatorComponent(),
                    # websiteAction
                    ButtonComponent(
                        style='link',
                        height='sm',
                        action=MessageAction(label='訓練時數多久?', text="訓練時數多久?")
                    ),
                    SeparatorComponent(),
                    ButtonComponent(
                        style='link',
                        height='sm',
                        action=MessageAction(label='為何選擇此主題?', text="為何選擇此主題?")
                    ),
                    SeparatorComponent(),
                    ButtonComponent(
                        style='link',
                        height='sm',
                        action=MessageAction(label='資料來源是哪?', text="資料來源是哪?")
                    ),
                    SeparatorComponent(),
                    ButtonComponent(
                        style='link',
                        height='sm',
                        action=MessageAction(label='網站特色?', text="網站特色?")
                    ),
                    SeparatorComponent(),
                    ButtonComponent(
                        style='link',
                        height='sm',
                        action=MessageAction(label='網站品項總共有多少?', text="網站品項總共有多少?")
                    ),
                    SeparatorComponent(),
                    ButtonComponent(
                        style='link',
                        height='sm',
                        action=MessageAction(label='有優惠嗎?', text="有優惠嗎?")
                    ),
                    SeparatorComponent(),
                    ButtonComponent(
                        style='link',
                        height='sm',
                        action=MessageAction(label='可以告訴我完整的訂購流程嗎?', text="可以告訴我完整的訂購流程嗎?")
                    ),
                    SeparatorComponent(),
                    ButtonComponent(
                        style='link',
                        height='sm',
                        action=MessageAction(label='期待新的商品推出', text="期待新的商品推出")
                    )
                ]
            ) 
        )
        message = FlexSendMessage(alt_text="享玩桌遊 EnjoyBoardGame", contents=bubble)
        line_bot_api.reply_message(
            event.reply_token,
            message
        )
        return

    if "專題成員有誰?"in msg or "成員"in msg:
        re = "成員包含:\n(組長)夏浩庭\n(技術長)黃凱廷\n(組員)劉哲文\n(組員)王泓智 "
    elif "訓練時數多久?"in msg or "時數"in msg or "訓練"in msg:
        re = "跨域Java工程師就業養成班，總訓練時數為546小時!"
    elif "為何選擇此主題?"in msg or "主題"in msg:
        re = "目前國際疫情持續延燒，且有越演越烈的趨勢，因此不論是強制隔離或自主居家檢疫，人們待在家中與家人相處的時間大幅增加，但3C產品往往佔據目光，造成\t'''明明相處時間增加，但彼此感情未見增長，衝突反而變多'''\t的情況出現。\n此時桌遊即為多人互動的好選擇!\n既可以遠離螢幕，又可充分與他人互動，故本組以桌遊作為題目進行專題發想，目標建立一個桌遊相關的網站。"
    elif "網站特色?"in msg or "特色"in msg:
        re = "網站提供完整的桌遊檢索系統供使用者搜尋以及購買、追蹤想體驗的桌遊\n亦有關於桌遊的討論區和消息專區，讓使用者觀看其他玩家的評論、遊戲體驗、開箱文，也可透過網站報名桌遊相關的課程、培訓活動。\n此外，前端頁面全為組員自行設計，未套用任何現成版面，敬請您觀賞指教!"
    elif "網站品項總共有多少?"in msg or "品項"in msg or "數量"in msg:
        re = "網站品項目前共有439個品項可供選購。"
    elif "有優惠嗎?"in msg or "優惠"in msg or "折扣"in msg:
        re = "請至選單點選折扣券圖示即可領取並至官網使用"
    elif "資料來源是哪?"in msg or "資料"in msg or "來源" in msg:
        re = "網站主要商品資訊來源，皆來自新天鵝堡桌遊官方網站提供，真的非常感謝!"
    elif "可以告訴我完整的訂購流程嗎?"in msg or "訂購"in msg or "購買"in msg or "買"in msg:
        re = "請上我們的官方網站，將想購買的商品加入購物車中，點擊結帳按鈕，系統即會導引您完成購買流程，非常感謝您的支持!"
    elif "期待新的商品推出" in msg:
        re = "網站如果有新商品推出，皆會公布在最新消息上喔!我們也會發送通知給您~"
   

    

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=re))


if __name__ == "__main__":
    app.run()
