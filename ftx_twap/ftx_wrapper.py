import hmac, json, requests, time
from requests import Request


def connect_ftx():
    return requests.Session()


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






