API_KEY = "2016294056:AAFiXSbWZIoAWMckfT5f_emfxM8sm7jPNqE"
import telebot

tb = telebot.TeleBot(API_KEY)
chat_id = -634899812
tb.config["api_key"] = API_KEY

@tb.route('/sinyal')
def sinyalVer(message):
    with open("buy_signals.txt", "r", encoding="utf-8") as file:
        text1 = file.read()
    with open("sell_signals.txt", "r", encoding="utf-8") as file:
        text2 = file.read()
    res = "\n\n!!!BUY SIGNALSS!!!\n\n" + text1 + "\n\n!!!SELL SIGNALSS!!!\n\n" + text2
    tb.send_message(chat_id, res)


tb.poll()
