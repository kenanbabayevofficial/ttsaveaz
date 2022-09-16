import json
import time
import requests
import os
from requests import *
from datetime import datetime
from config import *
from tiktok_module import downloader

api = "https://api.telegram.org/bot" + token_bot
update_id = 0


def SendVideo(userid, msgid):
    tg_url = api + "/sendvideo"
    data = {
        "chat_id": userid,
        "caption": "<b>Video Hazırdır!</b> @ttsaveaze_bot!\n\n<b>AZ</b> : <i>Video boşdursa, yenidən url göndərin!</i>\n<b>TR</b> : <i>Video beyazsa url'yi tekrar gönderin</i>",
        "parse_mode": "html",
        "reply_to_message_id": msgid,
        "reply_markup": json.dumps({
            "inline_keyboard": [
                [
                    {
                        "text": "Adminlə Əlaqə",
                        "url": "https://instagram.com/kenanbabayevofficial"
                    }
                ]
            ]
        })
    }
    res = post(
        tg_url,
        data=data,
        files={
            "video": open("video.mp4", "rb")
        }
    )


def SendMsg(userid, text, msgid):
    tg_url = api + "/sendmessage"
    post(
        tg_url,
        json={
            "chat_id": userid,
            "text": text,
            "parse_mode": "html",
            "reply_to_message_id": msgid
        }
    )


def get_time(tt):
    ttime = datetime.fromtimestamp(tt)
    return f"{ttime.hour}-{ttime.minute}-{ttime.second}-{ttime.day}-{ttime.month}-{ttime.year}"


def Bot(update):
    try:
        global last_use
        userid = update['message']['chat']['id']
        meseg = update['message']['text']
        msgid = update['message']['message_id']
        timee = update['message']['date']
        dl = downloader.tiktok_downloader()
        if update['message']['chat']['type'] != "private":
            SendMsg(
                userid,
                "Bot only work in private chat !",
                msgid
            )
            return
        first_name = update['message']['chat']['first_name']
        print(f"{get_time(timee)}-> {userid} - {first_name} -> {meseg}")
        if meseg.startswith('/start'):
            SendMsg(
                userid,
                "<b>Xoş Gəldiniz TikTok Video Yükləmə Botuna !</b>\n\n<b>Necə istifadə olunur? </b>:\n<i>sadəcə bu bota tiktok url videosunu göndərin və ya yapışdırın </i>!!\n",
                msgid
            )
        elif "tiktok.com" in meseg and "https://" in meseg:
            getvid = dl.musicaldown(url=meseg, output_name="video.mp4")
            if getvid == False:
                SendMsg(
                    userid,
                    "<i>Videonu endirmək alınmadı</i>\n\n<i>Try again later</i>",
                    msgid
                )
                return
            elif getvid == "private/remove":
                SendMsg(
                    userid,
                    "<i>Videonu endirmək alınmadı</i>\n\n<i>Video was private or removed</i>",
                    msgid
                )
            elif int(len(open('video.mp4', 'rb').read()) / 1024) > 51200:
                SendMsg(
                    userid,
                    "<i>Videonu endirmək alınmadı</i>\n\n<i>Video size to large</i>",
                    msgid
                )
            elif getvid == 'url-invalid':
                SendMsg(
                    userid,
                    "<i>URL is invalid, send again !</i>",
                    msgid)
            else:
                SendVideo(
                    userid,
                    msgid
                )
                os.remove('video.mp4')
        elif "/help" in meseg:
            SendMsg(
                userid,
                "Bu botdan necə istifadə etməli :\nsadəcə url tiktok videosunu bu bota göndərin və ya yapışdırın !\n\n/donation - donation bot\n/status - status botunu göstərin",
                msgid
            )
        elif meseg.startswith("/donation"):
            SendMsg(
                userid,
                "Admin: @kenanbabayevofficial",
                msgid
            )
    except KeyError:
        return
