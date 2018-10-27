sig_eth_balance = encrypt('GET|/api/v2/account|access_key='+api_key_otc+'&currency=eth',api_secret_otc)
sig_usdt_balance = encrypt('GET|/api/v2/account|access_key='+api_key_otc+'&currency=usdt',api_secret_otc)
sig_order = encrypt('GET|/api/v2/orders|access_key='+api_key_otc+'&market=ethusdt',api_secret_otc)
def get_price(exchange):
    if exchange=='otc':
        payload = {
            'market':'ethusdt',
            'limit' : 1
         }
        eth_usdt_depth = dict()
        try:
            res = requests.get('https://bb.otcbtc.com/api/v2/depth',params=payload)
            eth_usdt_depth = json.loads(res.text)
        except:
            print('loads error')
            return 1
        if 'bids' in eth_usdt_depth:
            data_dict['otc']['buy1_price'] = eth_usdt_depth['bids'][0][0]
            data_dict['otc']['buy1_quntity'] = eth_usdt_depth['bids'][0][1]
        if 'asks' in eth_usdt_depth:
            data_dict['otc']['sell1_price'] = eth_usdt_depth['asks'][0][0]
            data_dict['otc']['sell1_quntity'] = eth_usdt_depth['asks'][0][1]
    if exchange=='hit':
        try:
            order = client_hit.get_orderbook('ETHUSD')
        except:
            print('hit get price error')
            return 1
        
        data_dict['hit']['buy1_price'] = order['bid'][0]['price']
        data_dict['hit']['buy1_quntity'] = order['bid'][0]['size']
        data_dict['hit']['sell1_price'] = order['ask'][0]['price']
        data_dict['hit']['sell1_quntity'] = order['ask'][0]['size']
    return 0                                                     
           

def get_eth_balance(exchange):
    if exchange=='otc':
        payload= {'access_key':api_key_otc,          
                    'currency':'eth',
                    'signature':sig_eth_balance
                   }
        e_dict = dict()
        try:
            res = requests.get('https://bb.otcbtc.com/api/v2/account',params=payload)
            
            e_dict = json.loads(res.text)
        except:
            print('loads error')
            return 1
        data_dict['otc']['eth_balance'] = e_dict['balance']

    if exchange=='hit':
        eth_balance = 0.0
        try:
            balances = client_hit.get_trading_balance()
        except:
            print('otc error')
            return 1
        for balance in balances:
            if balance['currency'] == 'ETH':
                eth_balance = float(balance['available'])
                data_dict['hit']['eth_balance'] = eth_balance


    return 0 
def get_usdt_balance(exchange):
    if exchange=='otc':
        payload= {'access_key':api_key_otc,          
                    'currency':'usdt',
                    'signature':sig_usdt_balance
                   }
        e_dict = dict()
        try:
            res = requests.get('https://bb.otcbtc.com/api/v2/account',params=payload)
            
            e_dict = json.loads(res.text)
        except:
            print('loads error')
            return 1
        data_dict['otc']['usdt_balance'] = e_dict['balance']
    if exchange=='hit':
        usdt_balance = 0.0
        try:
            balances = client_hit.get_trading_balance()
        except:
            print('otc error')
            return 1
        for balance in balances:
            if balance['currency'] == 'USDT':
                usdt_balance = float(balance['available'])
                data_dict['hit']['usdt_balance'] = usdt_balance


    
    return 0 
def get_order(exchange):
    if exchange=='otc':
        payload = {
            'access_key':api_key_otc,
            'signature':sig_order,
            'market':'ethusdt'
         }
        eth_usdt_dict = dict()

        try:
            res = requests.get('https://bb.otcbtc.com/api/v2/orders',params=payload)
            eth_usdt_dict = json.loads(res.text)
        except:
            print('loads error')
            return 1
        data_dict['otc']['order_now'][0]={'id':0,'buyorsell':'NULL','price':0,'quntity':0}
        for index in range(len(eth_usdt_dict)):
            data_dict['otc']['order_now'][index] = { 'id':eth_usdt_dict[index][u'id'],'buyorsell': eth_usdt_dict[index][u'side'],'price' :eth_usdt_dict[index][u'price'],'quntity' :eth_usdt_dict[index][u'volume'] }
        print data_dict['otc']['order_now'][0]
    if exchange=='hit':
        try:
            o = client_hit.get_active_order('ETHUSD')
        except:
            print 'hit order error'
            return 1
        data_dict['hit']['order_now'][0]={'id':0,'buyorsell':'NULL','price':0,'quntity':0}
        for index in range(len(o)):
            data_dict['hit']['order_now'][index] = {'id':o[index]['clientOrderId'],'buyorsell':o[index]['side'],'price':o[index]['price'],'quntity':o[index]['quantity']}
        print data_dict['hit']['order_now'][0]
    return 0



