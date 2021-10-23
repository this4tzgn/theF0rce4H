import sqlite3

connector = sqlite3.connect('veri_alani.tzgn')
def sql_update(connector,b_coin,b_time,b_signal,status):

    cursorObj = connector.cursor()
    if status == "buy":
        cursorObj.execute('UPDATE buy SET signal_time = ? , signal = ? where coin = ?',(b_time,b_signal,b_coin))
    elif status == "sell":
        cursorObj.execute('UPDATE sell SET signal_time = ? , signal = ? where coin = ?', (b_time, b_signal, b_coin))
    else:
        print("database'de sorun var ilgilen!!!!")
    connector.commit()

def selectSignal(connector,b_coin,status):
    cursor = connector.cursor()
    if status == "buy":
        res = cursor.execute('SELECT signal FROM buy where coin = "{b_coin}"'.format(b_coin=b_coin))
        temp = res.fetchall()
        for i in temp:
            return i[0]


    if status == "sell":
        res = cursor.execute('SELECT signal FROM sell where coin = "{b_coin}"'.format(b_coin=b_coin))
        temp = res.fetchall()
        for i in temp:
            return i[0]

def selectTime(connector,b_coin,status):
    cursor = connector.cursor()
    if status == "buy":
        res = cursor.execute('SELECT signal_time FROM buy where coin = "{b_coin}"'.format(b_coin=b_coin))
        temp = res.fetchall()
        for i in temp:
            return i[0]

    if status == "sell":
        res = cursor.execute('SELECT signal_time FROM sell where coin = "{b_coin}"'.format(b_coin=b_coin))
        temp = res.fetchall()
        for i in temp:
            return i[0]

#sql_update(connector,2222,"4500","9999","sell")
#print(selectSignal(connector=connector,b_coin="ETH",status="buy"))
