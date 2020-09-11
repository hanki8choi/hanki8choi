from TickerMng import TickerMng

tickers = TickerMng()
tickers.load_type_list()
# tickers.download_stooq()
tickers.load_dataframe()

for date_idx in range( 12, len(tickers.offense_dfs['SPY.US'].index)-1  ) :
    if tickers.is_risky_canary(date_idx) :
        tickers.select_defense(date_idx)
    else :
        tickers.select_offense(date_idx)
        
exit(0)
