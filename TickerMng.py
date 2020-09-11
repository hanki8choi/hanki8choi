import pandas as pd
import pandas_datareader as pdr
import operator
import csv
import FinanceDataReader as fdr

class TickerMng:
    def __init__(self):
        self.mode = 0  #
        self.offense = []
        self.defense = []
        self.canary = []
        self.offense_df = pd.DataFrame()
        self.defense_df = pd.DataFrame()
        self.canary_df = pd.DataFrame()
        
        #self.typeName = ['offense', 'defense', 'canary']
        self.typeDic = {'offense':self.offense, 'defense':self.defense, 'canary':self.canary}
        self.tickers_df = {'offense':self.offense_df, 'defense':self.defense}, 'canary':self.canary_df}

    def make_ticker2dataframe(self, type, ticker_name):
        mon = pd.read_csv('data/M_%s.csv' % (ticker_name))
        #for idx in range( 12, len(mon)): 
        for idx in range( 0, len(mon) ): 
            score = mon.pct_change(periods=1)[idx] * 12 + mon.pct_change(periods=3)[idx] * 4 + mon.pct_change(periods=6)[idx] * 2 + mon.pct_change(periods=12)[idx]
            mon['score'] = score
            
        for idx in range( 0, len(mon)-1 ): 
            profit = mon['Close'][idx+1] - mon['Close'][idx]
            mon['profit'] = profit
        
        #mon['ticker_name'] = ticker_name
        
        df = self.tickers_df[type]
        df[ticker_name] = mon
        
        
    def load(self):
        for key, val in self.typeDic.items():
            val.clear()
            fd_list = open('data/Z_%s_list.csv' % (key), 'r', encoding='utf-8')
            rdlist = csv.reader(fd_list)
            for line in rdlist:
                ticker_name = line[0]
                val.append(ticker_name)
                make_ticker2dataframe(ticker_name)
                
            fd_list.close()

        for key, val in self.typeDic.items():
            for ticker_name in val:
                df = pdr.get_data_stooq(ticker_name)
                df.to_csv( 'data/O_%s.csv'%(ticker_name) )
                mon_df = df['Close'].resample('M').first()
                mon_df.to_csv('data/M_%s.csv'%(ticker_name) )

    def select_tickers(self, day, number )
        oneday_df = pd.DataFrame()
        
        for key, val in self.offense_df.items()
            my_data = list(val.iloc[0]) + [key] 
            my_col = list(val.iloc[0].index) + ['ticker_name']
            
            tmp = pd.DataFrame( data=[my_data], columns=my_col )
            oneday_df = oneday_df.append( tmp )
        
        oneday_df = oneday_df.set_index('ticker_name', drop=False )
        oneday_df = oneday_df.sort_values(by='score', ascending=False)
        
        result = []
        for idx in range(0,number)
            result.append( oneday_df.iloc[idx]['ticker_name'] )
         
        return result

    def save(self):
        for key, val in self.typeDic.items():
            f = open( 'data/Z_%s_list.csv'%(key) , 'w', encoding='utf-8', newline='')
            wr = csv.writer(f)
            for name in val:
                wr.writerow( [name] )
            f.close()

    def download_stooq(self):
        for key, val in self.typeDic.items():
            for ticker_name in val:
                df = pdr.get_data_stooq(ticker_name)
                df.to_csv( 'data/O_%s.csv'%(ticker_name) )
                mon_df = df['Close'].resample('M').first()
                mon_df.to_csv('data/M_%s.csv'%(ticker_name) )


    def download_fdr(self):
        for key, val in self.typeDic.items():
            for ticker_name in val:
                #2019년에서 현재까지
                fdr = fdr.DataReader(ticker_name, '2019' )
                df.to_csv( 'data/O_%s.csv'%(ticker_name) )
                mon_df = df['Close'].resample('M').first()
                mon_df.to_csv('data/M_%s.csv'%(ticker_name) )

