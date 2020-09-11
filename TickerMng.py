import pandas as pd
import pandas_datareader as pdr
import operator
import csv
import FinanceDataReader as fdr

class TickerMng:
    def __init__(self):
        self.mode = 0  #
        self.offenseNames = []
        self.defenseNames = []
        self.canaryNames = []
        self.offense_dfs = [pd.DataFrame()]
        self.defense_dfs = [pd.DataFrame()]
        self.canary_dfs = [pd.DataFrame()]
        
        self.namesGroup = {'offense':self.offenseNames, 'defense':self.defenseNames, 'canary':self.canaryNames}
        self.dfsGroup = {'offense':self.offense_dfs, 'defense':self.defense_dfs, 'canary':self.canary_dfs}

    def make_ticker2dataframe(self, type, ticker_name):
        mon = pd.read_csv('data/M_%s.csv' % (ticker_name))
        #for idx in range( 12, len(mon)): 
        for idx in range( 0, len(mon) ): 
            score = mon.pct_change(periods=1)[idx] * 12 + mon.pct_change(periods=3)[idx] * 4 + mon.pct_change(periods=6)[idx] * 2 + mon.pct_change(periods=12)[idx]
            mon['score'] = score
            
        for idx in range( 0, len(mon)-1 ): 
            profit = mon['Close'][idx+1] - mon['Close'][idx]
            mon['profit'] = profit
            
        dfs = self.dfsGroup[type]
        dfs[ticker_name] = mon
        
        
    def load_type_list(self):
        for key, val in self.namesGrouop.items():
            val.clear()
            fd_list = open('data/Z_%s_list.csv' % (key), 'r', encoding='utf-8')
            rdlist = csv.reader(fd_list)
            for line in rdlist:
                ticker_name = line[0]
                val.append(ticker_name)                
            fd_list.close()

    def download_stooq(self):
        for key, val in self.namesGroup.items():
            for ticker_name in val:
                df = pdr.get_data_stooq(ticker_name)
                df.to_csv( 'data/O_%s.csv'%(ticker_name) )
                mon_df = df['Close'].resample('M').first()
                mon_df.to_csv('data/M_%s.csv'%(ticker_name) )


    def download_fdr(self):
        for key, val in self.namesGroup.items():
            for ticker_name in val:
                #2019년에서 현재까지
                fdr = fdr.DataReader(ticker_name, '2019' )
                df.to_csv( 'data/O_%s.csv'%(ticker_name) )
                mon_df = df['Close'].resample('M').first()
                mon_df.to_csv('data/M_%s.csv'%(ticker_name) )


    def load_dataframe(self):
        for key, val in self.namesGroup.items():
            for ticker_name in val:
                make_ticker2dataframe(key, ticker_name)

    def is_risky_canary(self, date_idx )
        for val in self.canary_dfs:
            if val['score'].iloc[date_idx] <= 0 :
                return True
        return False
        
    def select_defense(self, date_idx )
        names = sort_dfs( self.defense_dfs, 1 )
        
        print( self.defens_dfs[ names[0] ].iloc[date_idx] )
    
    def select_offense(self, date_idx )
        names = sort_dfs( self.offense_cfs, 2 )
        
        print("-----------")
        print( self.offense_dfs[ names[0] ].iloc[date_idx] )
        print("-----------")
        print( self.offense_dfs[ names[1] ].iloc[date_idx] )
        
        
    def sort_dfs(self, dfs, date_idx, count )
        oneday_df = pd.DataFrame()
        
        for key, val in dfs.items()
            my_data = list(val.iloc[date_idx]) + [key] 
            my_col = list(val.iloc[date_idx].index) + ['ticker_name']
            
            tmp = pd.DataFrame( data=[my_data], columns=my_col )
            oneday_df = oneday_df.append( tmp )
        
        oneday_df = oneday_df.set_index('ticker_name', drop=False )
        oneday_df = oneday_df.sort_values(by='score', ascending=False)
        
        result = []
        for idx in range(0,count)
            result.append( oneday_df.iloc[idx]['ticker_name'] )
         
        return result

    def save_type_list(self):
        for key, val in self.namesGrouop.items():
            f = open( 'data/Z_%s_list.csv'%(key) , 'w', encoding='utf-8', newline='')
            wr = csv.writer(f)
            for name in val:
                wr.writerow( [name] )
            f.close()

