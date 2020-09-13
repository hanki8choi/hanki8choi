from TickerMng import TickerMng

tickers = TickerMng()
tickers.load_type_list()
# tickers.download_stooq()
tickers.load_dataframe()

tickers.show_daa_profit()
