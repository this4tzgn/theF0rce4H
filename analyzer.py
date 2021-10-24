test_timer = 0
timer = 0

#!/usr/bin/env python
# coding: utf-8
#Kütüphaneler
import os
import warnings
warnings.simplefilter("ignore")
import pandas as pd
import numpy 
import requests # veri çekme
from datetime import datetime #tarih değişkenleri
import time
import talib # teknik analiz indikatörleri için 
import matplotlib.pyplot as plt
#import plotly.graph_objects as go
#import plotly.express as pexp
import inspect
import databaseFile

API_KEY = "2012983454:AAFXcFFZs5oY6nUkhKOPUu8k02ZdqRHJA-Q"
import telebot
bot = telebot.TeleBot(API_KEY)
chat_id = -634899812
bot.config["api_key"] = API_KEY
print("program is running")



i=0
last_buy_signal = {"BTC":0,"ETH":0,"CAKE":0,"NEO":0,"BNB":0,"BAKE":0,"DOT":0,"EOS":0,"ETC":0,"ADA":0,"BCH":0,"LTC":0,"XRP":0,"DOGE":0,"SOL":0,"LUNA":0}
last_sell_signal = {"BTC":0,"ETH":0,"CAKE":0,"NEO":0,"BNB":0,"BAKE":0,"DOT":0,"EOS":0,"ETC":0,"ADA":0,"BCH":0,"LTC":0,"XRP":0,"DOGE":0,"SOL":0,"LUNA":0}
buy_signal = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
signal_time = []
sell_signal = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
last_buy_signal_4h = {"BTC":0,"ETH":0,"CAKE":0,"NEO":0,"BNB":0,"BAKE":0,"DOT":0,"EOS":0,"ETC":0,"ADA":0,"BCH":0,"LTC":0,"XRP":0,"DOGE":0,"SOL":0,"LUNA":0}
last_sell_signal_4h = {"BTC":0,"ETH":0,"CAKE":0,"NEO":0,"BNB":0,"BAKE":0,"DOT":0,"EOS":0,"ETC":0,"ADA":0,"BCH":0,"LTC":0,"XRP":0,"DOGE":0,"SOL":0,"LUNA":0}
buy_signal_4h = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
signal_time_4h = []
sell_signal_4h = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

symbols = ["BTC","ETH","CAKE","NEO","BNB","BAKE","DOT","EOS","ETC","ADA","BCH","LTC","XRP","DOGE","SOL","LUNA"]
yenicoin = ["avax","uni","algo","link","atom","icp","matic","one","rose","xlm","trx","xtz","theta","egld","xmr","aave","iota","btt","dash","chz","mana","enj","bat","rvn","ont","kava","sxp","dent","sun"]
yenicoin1 = [stri.upper() for stri in yenicoin] 
[last_buy_signal.__setitem__(strii,0) for strii in yenicoin1]
[last_sell_signal.__setitem__(strii,0) for strii in yenicoin1]
buy_signal.extend(list(numpy.zeros(len(yenicoin))))
sell_signal.extend(list(numpy.zeros(len(yenicoin))))
symbols.extend(yenicoin1)



def lastReader():
    for i in range(0,len(symbols)):
        item = symbols[i]
        last_buy_signal[item] = databaseFile.selectSignal(databaseFile.connector,item,"buy")
    for i in range(0,len(symbols)):
        item = symbols[i]
        last_sell_signal[item] = databaseFile.selectSignal(databaseFile.connector,item,"sell")
def reshaper():
    symbols_infunc = ["BTC: ","ETH: ","CAKE: ","NEO: ","BNB: ","BAKE: ","DOT: ","EOS: ","ETC: ","ADA: ","BCH: ","LTC: ","XRP: ","DOGE: ","SOL: ","LUNA: ","AVAX: ","UNI: ","ALGO: ","LINK: ","ATOM: ","ICP: ","MATIC: ","ONE: ","ROSE: ","XLM: ","TRX: ","XTZ: ","THETA: ","EGLD: ","XMR: ","AAVE: ","MIOTA: ","BTT: ","DASH: ","CHZ: ","MANA: ","ENJ: ","BAT: ","RVN: ","ONT: ","KAVA: ","SXP: ","DENT: ","SUN: "]
    for i in range(0,len(symbols)):
        buy_signal[i] = str(databaseFile.selectTime(databaseFile.connector,symbols[i],"sell"))+"---->"+symbols_infunc[i] + str(databaseFile.selectSignal(databaseFile.connector,symbols[i],"buy"))
    with open("buy_signals.txt", "w", encoding="utf-8") as file:
                for item in buy_signal:
                    file.write(str(item))
                    file.write("\n")        
    for i in range(0,len(symbols)):
        sell_signal[i] = str(databaseFile.selectTime(databaseFile.connector,symbols[i],"sell"))+"---->"+symbols_infunc[i] + str(databaseFile.selectSignal(databaseFile.connector,symbols[i],"sell"))
    with open("sell_signals.txt", "w", encoding="utf-8") as file:
                for item in sell_signal:
                    file.write(str(item))
                    file.write("\n")
def get_data(coin,money="USDT",api = "114982364c3cb0a2410f7a8871ce4dff8af75a024ae9ca5500e413c11d9ed843",day_hour = "hour"):
   # print(coin,end=": ")
    #api = input("Enter your api adress : ")
    #day_hour = input('Choose your time interval(day/hour) : ')
    frame = inspect.currentframe()
    global valuess
    args, _, _, valuess = inspect.getargvalues(frame)
    
    if day_hour == "day": 
        url_day = "https://min-api.cryptocompare.com/data/histoday"
        load = {"api_key":api,"fsym":coin,"tsym":money,"limit":672}
        result = requests.get(url = url_day,params = load).json()
        global data_day
        data_day = pd.DataFrame(result["Data"])
        #return data_day.iloc[:6,]
    if day_hour =="hour":
        url_hour = "https://min-api.cryptocompare.com/data/histohour"
        load = {"api_key":api,"fsym":coin,"tsym":money,"limit":672}
        result = requests.get(url = url_hour,params = load).json()
        global data_hour
        data_hour = pd.DataFrame(result["Data"])
        #return data_hour.iloc[:6,]

        
def date_transform(time):
    datetime1 = datetime.fromtimestamp(time);datetime1 = str(datetime1)
    datetime_son = datetime.strptime(datetime1,'%Y-%m-%d %H:%M:%S')
    return datetime_son




def get_volume(coin,money = "USDT",api = "1989798748:AAHRBAP34mVJ1bIvCpRfgs17XTr_SegAtnU",day_hour = "hour"):
    url_vol = "https://min-api.cryptocompare.com/data/exchange/histohour"

    api = "114982364c3cb0a2410f7a8871ce4dff8af75a024ae9ca5500e413c11d9ed843"
    load = {
            "api_key":api,
            "fsym":coin,
            "tsym":money,
            "limit":672}

    result = requests.get(url = url_vol,params= load).json()
    global volume
    volume = pd.DataFrame(result["Data"])
##################
#### 4H Data #####
##################
class one_four():
    def one_to_four_volume(data):
        data["time"] = pd.to_datetime(data["time"])
        hours = [3,7,11,15,19,23]
        global new_data_volume
        new_data_volume = pd.DataFrame()
        for i in hours:
            index = data[(data["time"].dt.hour == i)].index
            new_data = new_data.append(data.iloc[index])
        
        new_data = new_data.sort_values(by = "time")
    
    def one_to_four(data):
        data["time"] = pd.to_datetime(data["time"])
        hours = [3,7,11,15,19,23]
        global new_data
        new_data = pd.DataFrame()
        for i in hours:
            index = data[(data["time"].dt.hour == i)].index
            new_data = new_data.append(data.iloc[index])
        
        new_data = new_data.sort_values(by = "time")
###################
###################
###################
lastReader()
while True:
    start = datetime.now()
    if time.localtime().tm_min==timer or time.localtime().tm_min==test_timer:
        print("*****************************************")
        print("REQUESTING.......")
        print("*****************************************")
        for items in symbols:
            get_data(items)
            get_volume(items)
            #hacim datasının ana veriye eklenmesi
            data_hour["volume"] = volume["volume"]
            #VWMA
            data_hour["V*P"] = data_hour["volume"]*data_hour["close"]
            data_hour["VWMA30"]=data_hour["V*P"].rolling(window = 30).sum()/data_hour["volume"].rolling(window = 30).sum()
            #gereksiz kolonları şutlake
            data_hour.drop(["volumefrom","volumeto","conversionType","conversionSymbol","V*P"],axis = 1,inplace = True)

            data_hour["time"] = data_hour["time"].apply(lambda x: date_transform(x))
            short_ema9 = talib.EMA(data_hour["close"],9)
            ema_vwma_dict = {"EMA9":short_ema9,"VWMA30":data_hour["VWMA30"]}
            ema_vwma = pd.DataFrame(ema_vwma_dict)
            buy = []
            sell = []
            flag = 42

            for i in range(0, numpy.shape(ema_vwma)[0]):
                if ema_vwma["EMA9"].iloc[i] < ema_vwma["VWMA30"].iloc[i]:
                    buy.append(numpy.nan)
                    if flag != 1:
                        sell.append(ema_vwma["EMA9"].iloc[i])
                        flag = 1
                    else:
                        sell.append(numpy.nan)

                elif ema_vwma["EMA9"].iloc[i] > ema_vwma["VWMA30"].iloc[i]:
                    sell.append(numpy.nan)
                    if flag != 0:
                        buy.append(ema_vwma["EMA9"].iloc[i])
                        flag = 0
                    else:
                        buy.append(numpy.nan)
                else:
                    buy.append(numpy.nan)
                    sell.append(numpy.nan)
            
            
            
            # Buy-Sell datası oluşturma 1H
            buysell_data = {"Time": data_hour["time"], "Buy": buy, "Sell": sell}
            result = pd.DataFrame(buysell_data)
            index = result.iloc[:, 1:].dropna(how="all").index
            result = result.iloc[index,]
            if result["Buy"][0:1].isna().bool() == True:
                result = result.drop([min(index)])

            if numpy.isnan(result.iloc[result.shape[0] - 1,]["Buy"]) == False:
                databaseFile.sql_update(databaseFile.connector,items,str(result["Time"].iloc[-1]),str(round((result.iloc[result.shape[0] - 1,]["Buy"]),3)),status="buy")
                databaseFile.sql_update(databaseFile.connector,items,str(result["Time"].iloc[-1]),"nosignal",status="sell")
                print(items+": buy at ----> "+str(round((result.iloc[result.shape[0] - 1,]["Buy"]),3)))
                if str(round(result.iloc[result.shape[0] - 1,]["Buy"], 3)) != str(last_buy_signal[items]):
                    print("bot tetiklendi")
                    bot.send_message(chat_id,items+": buy at ----> "+str(round((result.iloc[result.shape[0] - 1,]["Buy"]),3)))
                    last_buy_signal[items] = round((result.iloc[result.shape[0] - 1,]["Buy"]),3)
            else:
                databaseFile.sql_update(databaseFile.connector, items, str(result["Time"].iloc[-1]),str(round((result.iloc[result.shape[0] - 1,]["Buy"]), 3)), status="sell")
                databaseFile.sql_update(databaseFile.connector, items, str(result["Time"].iloc[-1]), "nosignal", status="buy")
                print(items+": sell at ---->:"+str(round((result.iloc[result.shape[0] - 1,]["Sell"]),3)))
                if str(round(result.iloc[result.shape[0] - 1,]["Sell"], 3)) != str(last_sell_signal[items]):
                    print("bot tetiklendi")
                    bot.send_message(chat_id, items + ": sell at ----> " + str(round((result.iloc[result.shape[0] - 1,]["Sell"]), 3)))
                    last_sell_signal[items] = round((result.iloc[result.shape[0] - 1,]["Sell"]),3)
            
            
            #Get4H
            one_four.one_to_four(data_hour.drop(["VWMA30"],axis = 1))
            short_ema9_4h = talib.EMA(new_data["close"],9)
            new_data["V*P"] = new_data["volume"]*new_data["close"]
            new_data["VWMA30"]=new_data["V*P"].rolling(window = 30).sum()/new_data["volume"].rolling(window = 30).sum()
            ema_vwma_dict_4h = {"EMA9":short_ema9_4h,"VWMA30":new_data["VWMA30"]}
            ema_vwma_4h = pd.DataFrame(ema_vwma_dict_4h)
            buy = []
            sell = []
            flag = 42

            for i in range(0, numpy.shape(ema_vwma_4h)[0]):
                if ema_vwma_4h["EMA9"].iloc[i] < ema_vwma_4h["VWMA30"].iloc[i]:
                    buy.append(numpy.nan)
                    if flag != 1:
                        sell.append(ema_vwma_4h["EMA9"].iloc[i])
                        flag = 1
                    else:
                        sell.append(numpy.nan)

                elif ema_vwma_4h["EMA9"].iloc[i] > ema_vwma_4h["VWMA30"].iloc[i]:
                    sell.append(numpy.nan)
                    if flag != 0:
                        buy.append(ema_vwma_4h["EMA9"].iloc[i])
                        flag = 0
                    else:
                        buy.append(numpy.nan)
                else:
                    buy.append(numpy.nan)
                    sell.append(numpy.nan)
            
            # Buy-Sell datası oluşturma 4H
            buysell_data_4h = {"Time": new_data["time"], "Buy": buy, "Sell": sell}
            result_4h = pd.DataFrame(buysell_data_4h)
            index_4h = result_4h.iloc[:, 1:].dropna(how="all").index
            result_4h = result_4h.iloc[index_4h,]
            if result_4h["Buy"][0:1].isna().bool() == True:
                result_4h = result_4h.drop([min(index_4h)])

            if numpy.isnan(result_4h.iloc[result_4h.shape[0] - 1,]["Buy"]) == False:
                databaseFile.sql_update(databaseFile.connector,items,str(result_4h["Time"].iloc[-1]),str(round((result_4h.iloc[result_4h.shape[0] - 1,]["Buy"]),3)),status="buy")
                databaseFile.sql_update(databaseFile.connector,items,str(result_4h["Time"].iloc[-1]),"No signal",status="sell")
                print(items+": buy at ----> "+str(round((result_4h.iloc[result_4h.shape[0] - 1,]["Buy"]),3)))
                if str(round(result_4h.iloc[result_4h.shape[0] - 1,]["Buy"], 3)) != str(last_buy_signal_4h[items]):
                    print("bot tetiklendi")
                    #telegramBotAfgan.bot.send_message(telegramBotAfgan.chat_id,items+": buy at ----> "+str(round((result.iloc[result.shape[0] - 1,]["Buy"]),3)))
                    last_buy_signal_4h[items] = round((result_4h.iloc[result_4h.shape[0] - 1,]["Buy"]),3)
            else:
                databaseFile.sql_update(databaseFile.connector, items, str(result_4h["Time"].iloc[-1]),str(round((result_4h.iloc[result_4h.shape[0] - 1,]["Buy"]), 3)), status="sell")
                databaseFile.sql_update(databaseFile.connector, items, str(result_4h["Time"].iloc[-1]), "No signal", status="buy")
                print(items+": sell at ---->:"+str(round((result_4h.iloc[result_4h.shape[0] - 1,]["Sell"]),3)))
                if str(round(result_4h.iloc[result_4h.shape[0] - 1,]["Sell"], 3)) != str(last_sell_signal_4h[items]):
                    print("bot tetiklendi")
                    #telegramBotAfgan.bot.send_message(telegramBotAfgan.chat_id, items + ": sell at ----> " + str(round((result.iloc[result.shape[0] - 1,]["Sell"]), 3)))
                    last_sell_signal_4h[items] = round((result_4h.iloc[result_4h.shape[0] - 1,]["Sell"]),3)
    finish = datetime.now()
    sure = finish-start
    print("İşlem ",sure.seconds," saniyede tamamlandı..." )
    reshaper()
    time.sleep(80)
        
