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
    TextComponent, SpacerComponent, IconComponent, ButtonComponent,
    SeparatorComponent, QuickReply, QuickReplyButton,
    ImageSendMessage
)

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


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    #re = "超過回覆範圍喔! 麻煩重新再輸入一次"

    if "最新消息" in msg:
        carousel_template = CarouselTemplate(columns=[
            CarouselColumn(thumbnail_image_url='https://scontent.ftpe8-2.fna.fbcdn.net/v/t1.0-9/78858712_3020675774617584_8482206259481673728_n.jpg?_nc_cat=103&_nc_ohc=LcqCtsc9Mg4AQkWAfO3bHQkSFkQehfvv6JcB8Uph07V7mgieZ6G3k749w&_nc_ht=scontent.ftpe8-2.fna&oh=d0720b979ae3ae5e8164f4c3f7bcb2b1&oe=5E7D327A',
                           text='請填寫表單，完成後來電確認到貨日期，取貨時付款即可', title='台中高鐵站門市(自取)',
                           actions=[
                URIAction(label='訂購表單', uri='https://bit.ly/2Lhgrnx'),
                MessageAction(label='門市地址、電話及營業時間', text='高鐵門市地址')
            ]),
            CarouselColumn(thumbnail_image_url='https://scontent.ftpe8-2.fna.fbcdn.net/v/t1.0-9/79327003_3020675734617588_111192146333138944_n.jpg?_nc_cat=103&_nc_ohc=TtWIs9eKc-sAQmpge1FFJnBDoRemxWS3a0-LVR6sHLhT35_mS8IKxTsXg&_nc_ht=scontent.ftpe8-2.fna&oh=27b81efab9bcbdf4f8d92525515d998b&oe=5EB39E9E',
                           text='請填寫表單，完成後來電確認到貨日期，取貨時付款即可', title='美村門市(自取)',
                           actions=[
                URIAction(label='訂購表單', uri='https://bit.ly/2sAgS4I'),
                MessageAction(label='門市地址、電話及營業時間', text='美村本店地址')
            ]),
            CarouselColumn(thumbnail_image_url='https://scontent.ftpe8-2.fna.fbcdn.net/v/t1.0-9/78918939_3020675737950921_6237532466555387904_n.jpg?_nc_cat=103&_nc_ohc=uxxSk9XOLYUAQmc7lzkDRhNhk_h3LuzTRyKHIboEsX2zHsU8rSeqA6H0g&_nc_ht=scontent.ftpe8-2.fna&oh=015d9b93ba1d4b91c68abba29933dca0&oe=5E7DC110',
                           text='全台冷凍宅配，請先來電確到貨日期及數量，填寫完訂單後再行匯款 或 貨到付款', title='宅配預訂',
                           actions=[
                URIAction(label='訂購表單', uri='https://bit.ly/2sAgS4I'),
                MessageAction(label='合作宅配廠商', text='合作宅配廠商')
            ])
        ])
        template_message = TemplateSendMessage(
            alt_text='Carousel alt text', template=carousel_template)
        line_bot_api.reply_message(event.reply_token, template_message)
        return

    if "關於商品" in msg:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(
            text='詳情請上我們官方網站喔謝謝您~'))
        return

    if "我有問題" in msg:
        bubble = BubbleContainer(
            direction='ltr',
            hero=ImageComponent(
                url='https://scontent.ftpe8-1.fna.fbcdn.net/v/t1.0-9/79700129_3028430623842099_7126640471203381248_n.jpg?_nc_cat=105&_nc_ohc=EVvK1FJ1Hx0AQkYVs6ZndjKBRxnCe4kkCqozIAoPsgbYC-F1KyP5-9ycA&_nc_ht=scontent.ftpe8-1.fna&oh=a19374d1a71bffe76e0befb5470eacec&oe=5E70FB25',
                size='full',
                aspect_ratio='20:13',
                aspect_mode='cover',
                action=URIAction(uri='https://scontent.ftpe8-1.fna.fbcdn.net/v/t1.0-9/79700129_3028430623842099_7126640471203381248_n.jpg?_nc_cat=105&_nc_ohc=EVvK1FJ1Hx0AQkYVs6ZndjKBRxnCe4kkCqozIAoPsgbYC-F1KyP5-9ycA&_nc_ht=scontent.ftpe8-1.fna&oh=a19374d1a71bffe76e0befb5470eacec&oe=5E70FB25', label='label')
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
                        action=MessageAction(label='有團購優惠嗎?', text="有團購優惠嗎?")
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
                        action=MessageAction(label='期待新的商品推出', text="期待新的產品推出")
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

    if "專題成員有誰?" in msg:
        re = "成員包含: (組長)夏浩庭、(技術長)黃凱廷、劉哲文、黃冠華、王泓智 "
    elif "訓練時數多久?" in msg:
        re = "跨域Java工程師就業養成班 訓練時數為546小時"
    elif "為何選擇此主題?" in msg:
        re = "目前國際疫情持續延燒，且有越演越烈的趨勢，因此不論是強制隔離或自主居家檢疫，人們待在家中與家人相處的時間大幅增加，但3C產品往往佔據目光，造成'明明相處時間增加，但彼此感情未見增長，衝突反而變多'的情況出現，此時桌遊即為多人互動的好選擇，既可以遠離螢幕，又可充分與他人互動，故本組以桌遊作為題目進行專題發想，目標建立一個桌遊相關的網站。"
    elif "網站特色?" in msg:
        re = "網站提供完整的桌遊檢索系統供使用者搜尋以及購買、追蹤想體驗的桌遊，亦有關於桌遊的討論區和消息專區，讓使用者觀看其他玩家的評論、遊戲體驗、開箱文，也可透過網站報名桌遊相關的課程、培訓活動。此外，前端頁面全為組員自行設計，未套用任何現成版面，敬請您觀賞指教。"
    elif "網站品項總共有多少?" in msg:
        re = "網站品項目前共有439個品項可供選購。"
    elif "有團購優惠嗎?" in msg:
        re = "目前並無此設定，但未來已有此規劃，敬請期待!"
    elif "資料來源是哪?" in msg:
        re = "網站主要商品資訊來源，皆來自新天鵝堡桌遊官方網站提供，真的非常感謝!"
    elif "可以告訴我完整的訂購流程嗎?" in msg:
        re = "恩...請上我們的官方網站，將想購買的商品加入購物車中，點擊結帳按鈕，系統即會導引您完成購買流程，非常感謝您的支持!"
    elif "期待新的商品推出" in msg:
        re = "網站如果有新商品推出，皆會公布在最新消息上喔!我們也會發送通知給您~"
   

    

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=re))


if __name__ == "__main__":
    app.run()
