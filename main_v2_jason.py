import csv
import requests
import hmac,hashlib
import json
import collections
import time
from binance.client import Client
from binance.enums import *
import ccxt
ccxt.binance({ 'options': { 'adjustForTimeDifference': True }})
DATEFORMAT='%m-%d'
TIMEFORMAT='%X'

#--------------------------OTC--------------------------------------------------------
api_key_otc = 'XXX'
api_secret_otc = 'XXX'
sig_eth_balance = encrypt('GET|/api/v2/account|access_key='+api_key_otc+'&currency=eth',api_secret_otc)
sig_usdt_balance = encrypt('GET|/api/v2/account|access_key='+api_key_otc+'&currency=usdt',api_secret_otc)
sig_order = encrypt('GET|/api/v2/orders|access_key='+api_key_otc+'&market=ethusdt',api_secret_otc)

otc_dict = collections.defaultdict(dict)
otc_dict['usdt_balance'] = 0
otc_dict['eth_balance'] = 0
otc_dict['buy1_price'] = 0
otc_dict['buy1_quntity'] = 0
otc_dict['sell1_price'] = 0
otc_dict['sell1_quntity'] = 0
otc_dict['buy2_price'] = 0
otc_dict['buy2_quntity'] = 0
otc_dict['sell2_price'] = 0
otc_dict['sell2_quntity'] = 0
otc_dict['order_now'][0] = {'id':0,'buyorsell':'NULL','price':0,'quntity':0}

#--------------------------OTC--------------------------------------------------------

#--------------------------BNC--------------------------------------------------------
api_key_bnc='xFJeufJu5Lm3jWvwDMEnxLbEcaVl8Q4ZGLXeFXhNKrIsLR1rT2HHU1rnn5N1ffM0'
api_secret_bnc='ip8FaoeiMW9PDMJWddfhXkV3jaPxVj69fDlhM1Kra0QtITYALvKZriwRDsRRHUgX'
client = Client(api_key_bnc,api_secret_bnc)

bnc_dict = collections.defaultdict(dict)
bnc_dict['usdt_balance'] = 0
bnc_dict['eth_balance'] = 0
bnc_dict['buy1_price'] = 0
bnc_dict['buy1_quntity'] = 0
bnc_dict['sell1_price'] = 0
bnc_dict['sell1_quntity'] = 0
bnc_dict['buy2_price'] = 0
bnc_dict['buy2_quntity'] = 0
bnc_dict['sell2_price'] = 0
bnc_dict['sell2_quntity'] = 0
bnc_dict['order_now'][0] ={'id':0,'buyorsell':'NULL','price':0,'quntity':0}
#--------------------------HIT--------------------------------------

public_key = "ffc770bc4849f452bf8a761144cac411"
secret = "19a846519affc328d63e93c9a6a8165b"
client_hit = Client_hit("https://api.hitbtc.com", public_key, secret)

hit_dict = collections.defaultdict(dict)
hit_dict['usdt_balance'] = 0
hit_dict['eth_balance'] = 0
hit_dict['buy1_price'] = 0
hit_dict['buy1_quntity'] = 0
hit_dict['sell1_price'] = 0
hit_dict['sell1_quntity'] = 0
hit_dict['buy2_price'] = 0
hit_dict['buy2_quntity'] = 0
hit_dict['sell2_price'] = 0
hit_dict['sell2_quntity'] = 0
hit_dict['order_now'][0] ={'id':0,'buyorsell':'NULL','price':0,'quntity':0}

#--------------------------BNC--------------------------------------------------------

########### function

def encrypt(message,key):
    #message = 'POST|/api/v2/orders|access_key=xxx&market=otbeth&price=0.002&side=sell&volume=100'
    digester = hmac.new(key, message, hashlib.sha256)
    return digester.digest().encode('hex') 

    
def order(exchange,market,buy_sell,volume,price):
    if exchange=='otc':
        sig = encrypt('POST|/api/v2/orders|access_key='+api_key_otc+'&market='+market+'&price='+price+'&side='+buy_sell+'&volume='+volume,api_secret_otc)
        payload = {
        'market':market,
        "side": buy_sell,
        "volume": volume,
        "price": price,
        'access_key':'glLuC0hqU258TxxMQbtukbK0SnlOOG5d3s0BUcLW',
        'signature':sig,
        }

        order_dict = dict()
        order_dict['id']=0
        try:
            res = requests.post('https://bb.otcbtc.com/api/v2/orders',params=payload)
            order_dict = json.loads(res.text)
        except:
            print('loads error')
            return 1
        return order_dict['id']
    if exchange=='hit':
        client_order_id = uuid.uuid4().hex
        try:
            order = client_hit.new_order(client_order_id=client_order_id,symbol_code='ETHUSD', side=buy_sell, quantity=volume, price=price)
        except:
            print 'order hit fail'
            return 1
        return order['clientOrderId']

            

def otc_cancel_order(exchange,id):
    if exchange=='otc':
        sig = encrypt('POST|/api/v2/order/delete|access_key='+api_key_otc+'&id='+id,api_secret_otc)
        payload5 = {

        'access_key':'glLuC0hqU258TxxMQbtukbK0SnlOOG5d3s0BUcLW',
        'signature':sig,
        'id':id

        }
        suc = dict()
        try:
            res = requests.post('https://bb.otcbtc.com/api/v2/order/delete',params=payload5)
            suc = res.json()
        except:
            print('otc cancel order fail')
        return suc
    if exchange=='hit':
        try:
            a = client_hit.cancel_order(id)
        except:
            print ' hit cancel order fail '
            return 1
        return a


def refresh():
    try:
        bnc_dict['usdt_balance']=client.get_asset_balance(asset='USDT')[u'free'] #USDT餘額
    except:
        print('loads error')
        return 1
    try:
        bnc_dict['eth_balance']=client.get_asset_balance(asset='ETH')[u'free'] #ETH餘額
    except:
        print('loads error')
        return 1
    try:
        deepth=client.get_order_book(symbol='ETHUSDT')
    except:
        print('loads error')
        return 1
    bnc_dict['buy1_price']=deepth[u'bids'][0][0]
    bnc_dict['buy1_quntity']=deepth[u'bids'][0][1]
    bnc_dict['buy2_price']=deepth[u'bids'][1][0]
    bnc_dict['buy2_quntity']=deepth[u'bids'][1][1]
    bnc_dict['sell1_price']=deepth[u'asks'][0][0]
    bnc_dict['sell1_quntity']=deepth[u'asks'][0][1]
    bnc_dict['sell2_price']=deepth[u'asks'][1][0]
    bnc_dict['sell2_quntity']=deepth[u'asks'][1][1]
    try:
        orders=client.get_open_orders(symbol='ETHUSDT')
    except:
        print('loads error')
        return 1
    if orders==[]:
        bnc_dict['order_now'][0]={'id':0,'buyorsell':'NULL','price':0,'quntity':0}
    else:
        bnc_dict['order_now'][0]={'id':orders[0][u'orderId'],'buyorsell':orders[0][u'side'],'price':orders[0][u'price'],'quntity':orders[0][u'origQty']}
    
    
    payload1= {'access_key':api_key_otc,                
                'currency':'eth',
                'signature':'bf879bd64f84ff804d1f76b8b2ca65878360333aca13716ada7959cf647ae7dd'
               }
    eth_dict = dict()
    eth_dict['balance']=0 
    try:
        res = requests.get('https://bb.otcbtc.com/api/v2/account',params=payload1)
        eth_dict = json.loads(res.text)
    except:
        print('loads error')
        return 1
    balance = dict()
    balance['eth'] = eth_dict['balance']
    payload2 = {'access_key':api_key_otc,               
                'currency':'usdt',
                'signature':'20a7f20dc2f9864f8a127746bbff4545580eb21af8f2734c57cacf16d9f4ec52'
               }
    usdt_dict = dict()
    usdt_dict['balance']=0
    try:
        res = requests.get('https://bb.otcbtc.com/api/v2/account',params=payload2)
        usdt_dict = json.loads(res.text)
    except:
        print('loads error')
        return 1
    balance['usdt'] = usdt_dict['balance']
    otc_dict['usdt_balance'] = balance['usdt']
    otc_dict['eth_balance'] = balance['eth']
    payload3 = {
        'access_key':'glLuC0hqU258TxxMQbtukbK0SnlOOG5d3s0BUcLW',
        'signature':'d28883765df222b6a4322db4f03c8264aacf6695edf81f17209beb6b090ac930',
        'market':'ethusdt'
     }
    eth_usdt_dict = dict()
    
    try:
        res = requests.get('https://bb.otcbtc.com/api/v2/orders',params=payload3)
        eth_usdt_dict = json.loads(res.text)
    except:
        print('loads error')
        return 1
    otc_dict['order_now'][0]={'id':0,'buyorsell':'NULL','price':0,'quntity':0}
    for index in range(len(eth_usdt_dict)):
        otc_dict['order_now'][index] = { 'id':eth_usdt_dict[index][u'id'],'buyorsell': eth_usdt_dict[index][u'side'],'price' :eth_usdt_dict[index][u'price'],'quntity' :eth_usdt_dict[index][u'volume'] }
    payload4 = {
        'market':'ethusdt',
        'limit' : 2
     }
    eth_usdt_depth = dict()
    try:
        res = requests.get('https://bb.otcbtc.com/api/v2/depth',params=payload4)
        eth_usdt_depth = json.loads(res.text)
    except:
        print('loads error')
        return 1
    if u'bids' in eth_usdt_depth:
        otc_dict['buy1_price'] = eth_usdt_depth[u'bids'][0][0]
        otc_dict['buy1_quntity'] = eth_usdt_depth[u'bids'][0][1]
        otc_dict['buy2_price'] = eth_usdt_depth[u'bids'][1][0]
        otc_dict['buy2_quntity'] = eth_usdt_depth[u'bids'][1][1]
    if u'asks' in eth_usdt_depth:
        otc_dict['sell1_price'] = eth_usdt_depth[u'asks'][0][0]
        otc_dict['sell1_quntity'] = eth_usdt_depth[u'asks'][0][1]
        otc_dict['sell2_price'] = eth_usdt_depth[u'asks'][1][0]
        otc_dict['sell2_quntity'] = eth_usdt_depth[u'asks'][1][1]
    return 0