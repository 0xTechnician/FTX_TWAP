import hmac, json, requests, time
from requests import Request


def connect_ftx():
    return requests.Session()


def get_positions(FTX_API_KEY, FTX_API_SECRET, SUB_ACC):
    requests_session = connect_ftx()
    positions = []
    ts = int(time.time() * 1000)
    request = Request('GET', 'https://ftx.com/api/positions?showAvgPrice=true')
    prepared = request.prepare()
    signature_payload = f'{ts}{prepared.method}{prepared.path_url}'.encode()
    signature = hmac.new(FTX_API_SECRET.encode(), signature_payload, 'sha256').hexdigest()


    request.headers['FTX-KEY'] = FTX_API_KEY
    request.headers['FTX-SUBACCOUNT'] = SUB_ACC
    request.headers['FTX-SIGN'] = signature
    request.headers['FTX-TS'] = str(ts)
    wallet_positions = json.loads(requests_session.send(request.prepare()).text)
    for position in wallet_positions.get('result'):
        if position['netSize'] != 0:
            positions.append(position)
    return positions
      

def get_interesting_instruments(FTX_API_KEY, FTX_API_SECRET, SUB_ACC):
    requests_session = connect_ftx()
    interesting_futures = []
    ts = int(time.time() * 1000)
    request = Request('GET', 'https://ftx.com/api/futures')
    prepared = request.prepare()
    signature_payload = f'{ts}{prepared.method}{prepared.path_url}'.encode()
    signature = hmac.new(FTX_API_SECRET.encode(), signature_payload, 'sha256').hexdigest()

    request.headers['FTX-KEY'] = FTX_API_KEY
    request.headers['FTX-SUBACCOUNT'] = SUB_ACC
    request.headers['FTX-SIGN'] = signature
    request.headers['FTX-TS'] = str(ts)
    futures = json.loads(requests_session.send(request.prepare()).text)
    for future in futures.get('result'):
        if future['volumeUsd24h'] > 10000000 and not 'BTC' in future['name'] and not 'ETH' in future['name']:
            interesting_futures.append([future['name'], future['volumeUsd24h']])

    return interesting_futures
def get_position(ticker_name, FTX_API_KEY, FTX_API_SECRET, SUB_ACC):
    requests_session = connect_ftx()

    ts = int(time.time() * 1000)
    request = Request('GET', 'https://ftx.com/api/positions')
    prepared = request.prepare()
    signature_payload = f'{ts}{prepared.method}{prepared.path_url}'.encode()
    signature = hmac.new(FTX_API_SECRET.encode(), signature_payload, 'sha256').hexdigest()

    request.headers['FTX-KEY'] = FTX_API_KEY
    request.headers['FTX-SUBACCOUNT'] = SUB_ACC
    request.headers['FTX-SIGN'] = signature
    request.headers['FTX-TS'] = str(ts)
    wallet_positions = json.loads(requests_session.send(request.prepare()).text)
    for position in wallet_positions.get('result'):
        if position.get('future') == ticker_name:
            return position

'''
wallet related

'''
def get_wallet_balance(FTX_API_KEY, FTX_API_SECRET, SUB_ACC):
    requests_session = connect_ftx()

    ts = int(time.time() * 1000)
    request = Request('GET', 'https://ftx.com/api/wallet/balances')
    prepared = request.prepare()
    signature_payload = f'{ts}{prepared.method}{prepared.path_url}'.encode()
    signature = hmac.new(FTX_API_SECRET.encode(), signature_payload, 'sha256').hexdigest()

    request.headers['FTX-KEY'] = FTX_API_KEY
    request.headers['FTX-SUBACCOUNT'] = SUB_ACC
    request.headers['FTX-SIGN'] = signature
    request.headers['FTX-TS'] = str(ts)
    wallet_info = json.loads(requests_session.send(request.prepare()).text)
    wallet_balance = 0
    for coin_balance in wallet_info['result']:
        if coin_balance['usdValue']:
            wallet_balance += coin_balance['usdValue']
    return wallet_balance
'''
end walletrelated
'''


def place_market_order(ticker_name, nb_contracts, trade_side, FTX_API_KEY, FTX_API_SECRET, SUB_ACC):
    requests_session = connect_ftx()
    ts = int(time.time() * 1000)
    '''
    market  string  XRP-PERP    e.g. "BTC/USD" for spot, "XRP-PERP" for futures
    side    string  sell    "buy" or "sell"
    price   number  0.306525    Send null for market orders.
    type    string  limit   "limit" or "market"
    '''
    requests_session = connect_ftx()
    body = {
    "market": ticker_name,
    "side": trade_side,
    "price": None,
    "size": nb_contracts,
    "type": "market",
    "reduceOnly": False,
    "ioc": False,
    "postOnly": False,
    "clientId": None
    }
    request = Request('POST', 'https://ftx.com/api/orders', json = body)

    prepared = request.prepare()
    signature_payload = f'{ts}{prepared.method}{prepared.path_url}'.encode()
    if prepared.body:
        signature_payload += prepared.body

    signature_payload = signature_payload
    signature = hmac.new(FTX_API_SECRET.encode(), signature_payload, 'sha256').hexdigest()

    request.headers['FTX-KEY'] = FTX_API_KEY
    request.headers['FTX-SUBACCOUNT'] = SUB_ACC
    request.headers['FTX-SIGN'] = signature
    request.headers['FTX-TS'] = str(ts)


    place_order = requests_session.send(request.prepare()).text


    print(place_order)

def place_limit_order(price, ticker_name, nb_contracts, trade_side, FTX_API_KEY, FTX_API_SECRET, SUB_ACC):
    requests_session = connect_ftx()
    ts = int(time.time() * 1000)
    '''
    market  string  XRP-PERP    e.g. "BTC/USD" for spot, "XRP-PERP" for futures
    side    string  sell    "buy" or "sell"
    price   number  0.306525    Send null for market orders.
    type    string  limit   "limit" or "market"
    '''
    body = {
    "market": ticker_name,
    "side": trade_side,
    "price": price,
    "size": nb_contracts,
    "type": "limit",
    "reduceOnly": False,
    "ioc": False,
    "postOnly": False,
    "clientId": None
    }
    request = Request('POST', 'https://ftx.com/api/orders', json = body)

    prepared = request.prepare()
    signature_payload = f'{ts}{prepared.method}{prepared.path_url}'.encode()
    if prepared.body:
        signature_payload += prepared.body

    signature_payload = signature_payload
    signature = hmac.new(FTX_API_SECRET.encode(), signature_payload, 'sha256').hexdigest()

    request.headers['FTX-KEY'] = FTX_API_KEY
    request.headers['FTX-SUBACCOUNT'] = SUB_ACC
    request.headers['FTX-SIGN'] = signature
    request.headers['FTX-TS'] = str(ts)


    place_order = requests_session.send(request.prepare()).text
    print(place_order)

def get_nb_contracts(wallet_balance, price, leverage):
    try:
        return ((wallet_balance / price) * float(leverage))
    except Exception as e:
        print(e)

def cancel_all_orders(ticker_name, FTX_API_KEY, FTX_API_SECRET, FTX_SUBACCOUNT):
    requests_session = connect_ftx()
    ts = int(time.time() * 1000)

    body = {
    "market": ticker_name
    }
    request = Request('DELETE', 'https://ftx.com/api/orders', json = body)

    prepared = request.prepare()
    signature_payload = f'{ts}{prepared.method}{prepared.path_url}'.encode()
    if prepared.body:
        signature_payload += prepared.body

    signature_payload = signature_payload
    signature = hmac.new(FTX_API_SECRET.encode(), signature_payload, 'sha256').hexdigest()

    request.headers['FTX-KEY'] = FTX_API_KEY
    request.headers['FTX-SIGN'] = signature
    request.headers['FTX-TS'] = str(ts)
    request.headers['FTX-SUBACCOUNT'] = FTX_SUBACCOUNT
    requests_session.send(request.prepare()).text

def cancel_all_orders_for_exch(FTX_API_KEY, FTX_API_SECRET, FTX_SUBACCOUNT):
    requests_session = connect_ftx()
    ts = int(time.time() * 1000)

    request = Request('DELETE', 'https://ftx.com/api/orders')

    prepared = request.prepare()
    signature_payload = f'{ts}{prepared.method}{prepared.path_url}'.encode()
    if prepared.body:
        signature_payload += prepared.body

    signature_payload = signature_payload
    signature = hmac.new(FTX_API_SECRET.encode(), signature_payload, 'sha256').hexdigest()

    request.headers['FTX-KEY'] = FTX_API_KEY
    request.headers['FTX-SIGN'] = signature
    request.headers['FTX-TS'] = str(ts)
    request.headers['FTX-SUBACCOUNT'] = FTX_SUBACCOUNT
    requests_session.send(request.prepare()).text


def get_ticker_info(symbol_id, timeframe_id, length, FTX_API_KEY, FTX_API_SECRET, SUB_ACC):
    requests_session = connect_ftx()

    if timeframe_id == "1m":
        tf_sec = 60
    elif timeframe_id == "5m":
        tf_sec = 60 * 5 
    elif timeframe_id == "15m":
        tf_sec = 15 * 60
    elif timeframe_id == "1h":
        tf_sec = 60 * 60
    elif timeframe_id == "4h":
        tf_sec = 60 * 60 * 4
    elif timeframe_id == "1d":
        tf_sec = 60 * 60 * 24


    ts = int(time.time() * 1000)
    request = Request('GET', 'https://ftx.com/api/markets/' + symbol_id + '/candles?resolution=' + str(tf_sec)  + '&limit=' + str(length))
    prepared = request.prepare()
    signature_payload = f'{ts}{prepared.method}{prepared.path_url}'.encode()
    signature = hmac.new(FTX_API_SECRET.encode(), signature_payload, 'sha256').hexdigest()

    request.headers['FTX-KEY'] = FTX_API_KEY
    request.headers['FTX-SUBACCOUNT'] = SUB_ACC
    request.headers['FTX-SIGN'] = signature
    request.headers['FTX-TS'] = str(ts)

    last_candles = json.loads(requests_session.send(request.prepare()).text)
    candles_array = []
    for candle_item in last_candles.get('result'):
        candle_dict = {}
        candle_dict["symbol"] = symbol_id
        candle_dict["timestamp"] = float(candle_item["time"])
        candle_dict["high"] = float(candle_item["high"])
        candle_dict["low"] = float(candle_item["low"])
        candle_dict["close"] = float(candle_item["close"])
        candle_dict["volume"] = float(candle_item["volume"])

        candles_array.append(candle_dict)
    candles_array = candles_array[::-1]
    return candles_array






