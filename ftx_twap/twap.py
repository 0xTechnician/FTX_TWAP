import ftx_wrapper

'''
Replace the values surrounded by quotes with your API KEYS 
and the subaccount you want to execute queries on
'''
FTX_API_KEY = 'YOUR_API_KEY'
FTX_API_SECRET = 'YOUR_API_SECRET'
FTX_SUB = 'YOUR_SUBACCOUNT_NAME'


'''
If you want to TWAP a perp, use the following syntax  [YOUR_COIN]-PERP
If you want to TWAP a spot market, use the following syntax [YOUR_COIN]/USD

The quantity following the name of the market is in USD, we'll setup the frequency of execution outside of this script

'''

'''
The following exemple TWAP POLIS-PERP (perp) with 100 USD and ATLAS/USD (spot market) with 100 USD.
'''
FTX_SYMBOLS = {
	"POLIS-PERP":100,
	"ATLAS/USD":100,
}

if __name__ == "__main__":
	for ticker_name, ticker_nb_contracts in FTX_SYMBOLS.items():
		candle_array = ftx_wrapper.get_ticker_info(ticker_name, '1m', 1, FTX_API_KEY, FTX_API_SECRET, FTX_SUB)
		nb_contracts = (1 / candle_array[0]['close']) * ticker_nb_contracts
		ftx_wrapper.place_market_order(ticker_name, nb_contracts, 'buy', FTX_API_KEY, FTX_API_SECRET, FTX_SUB)
