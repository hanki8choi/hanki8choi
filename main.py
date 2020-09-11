# import os
import pandas_datareader as pdr
import operator
from TickerMng import TickerMng

tickers = TickerMng()

#mng.offense = ['SPY.US', 'IWM.US', 'QQQ.US', 'VGK.US', 'EWJ.US', 'VWO.US', 'VNQ.US', 'GSG.US', 'GLD.US', 'TLT.US', 'HYG.US', 'LQD.US']
#mng.defense = ['SHV.US', 'IEF.US', 'UST.US']
#mng.canary = ['BND.US', 'VWO.US']

tickers.load_type_list()
#tickers.download_stooq()
#tickers.download_fdr()
tickers.load_dataframe()

for date_idx in range(0,10):
    if tickers.is_risky_canary(date_idx) :
        tickers.select_defense(date_idx)
    else :
        tickers.select_offense(date_idx)
        
exit(0)
# Download후에 저장하는방식
# 값을 파일별로 분리
# SPY등을 인자로 찾는다.

def get_daa_score(ticker):
    mon = pdr.get_data_stooq(ticker)
    #mon.to_csv(ticker)

    mon = mon['Close'].resample('M').first()
    #mon.to_csv(ticker+"1")
    #val = (mon[-1] - mon[-2])*12 + (mon[-1] - mon[-4])*4 + (mon[-1] - mon[-7])*2 + (mon[-1] - mon[-13])

    #print(mon.pct_change(periods=1)[-1] )
    #print("-------------")
    #print(mon.pct_change(periods=6) )
    val = mon.pct_change(periods=1)[-1] * 12 + mon.pct_change(periods=3)[-1] * 4 + mon.pct_change(periods=6)[-1] * 2 + mon.pct_change(periods=12)[-1]
    print( "%s :  %lf " % (ticker , val) )
    return val
    #return val

#aaa = pdr.get_data_stooq('SPY.US', chunksize='20')
#print( aaa )
#def get_daa_score(ticker):
#    mon = pdr.StooqDailyReader(symbols=ticker,  )

#offense = ['SPY', 'IWM', 'QQQ', 'VGK', 'EWJ', 'VWO', 'VNQ', 'GSG', 'GLD', 'TLT', 'HYG', 'LQD']
#defense = ['SHV', 'IEF', 'UST']
#canaria = ['BND', 'VWO']

offense = ['SPY.US', 'IWM.US', 'QQQ.US', 'VGK.US', 'EWJ.US', 'VWO.US', 'VNQ.US', 'GSG.US', 'GLD.US', 'TLT.US', 'HYG.US', 'LQD.US']
defense = ['SHV.US', 'IEF.US', 'UST.US']
canaria = ['BND.US', 'VWO.US']

#get_daa_score('SPY.US')
#exit(0)

offense_score = {}
defense_score = {}
canaria_score = {}

for t in offense:
    offense_score[t] = get_daa_score(t)
offense_list = sorted(offense_score.items(), key=operator.itemgetter(1), reverse=True)

for t in defense:
    defense_score[t] = get_daa_score(t)

defense_list = sorted(defense_score.items(), key=operator.itemgetter(1), reverse=True)

for t in canaria:
    canaria_score[t] = get_daa_score(t)

level = 0

for score in canaria_score.values():
    if score > 0:
        level += 1

if level == 0:
    print('수비 100%')
    i = list(defense_list[0])
    print('수비 : ', i[0], '  스코어 :', i[1])
elif level == 1:
    print('수비 50%, 공격 50%(6종목)')
    print('수비 :', defense_list[0])
    for i in offense_list[:6]:
        print('공격 :', i[0], '  스코어 :', i[1])
else:
    print('공격 100%(6종목)')
    for i in offense_list[:6]:
        print('공격 : ', i[0], ' 스코어 :', i[1])
