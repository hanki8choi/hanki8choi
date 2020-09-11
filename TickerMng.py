import pandas as pd
import pandas_datareader as pdr
import operator
import csv

class TickerMng:
    def __init__(self):
        self.mode = 0  #
        self.offense = []
        self.defense = []
        self.canary = []
        #self.typeName = ['offense', 'defense', 'canary']
        self.typeDic = {'offense':self.offense, 'defense':self.defense, 'canary':self.canary}

    def load_ticker_file(self, ticker_name):
        pd.read_csv('data/M_%s.csv' % (ticker_name))

                
                #df = pdr.get_data_stooq(ticker_name)
                #df.to_csv( 'data/O_%s.csv'%(ticker_name) )
                #mon_df = df['Close'].resample('M').first()
                #mon_df.to_csv('data/M_%s.csv'%(ticker_name) )


            fd_list.close()
        
    def load(self):
        for key, val in self.typeDic.items():
            val.clear()
            fd_list = open('data/Z_%s_list.csv' % (key), 'r', encoding='utf-8')
            rdlist = csv.reader(fd_list)
            for line in rdlist:
                ticker_name = line[0]
                val.append(ticker_name)

                
                #df = pdr.get_data_stooq(ticker_name)
                #df.to_csv( 'data/O_%s.csv'%(ticker_name) )
                #mon_df = df['Close'].resample('M').first()
                #mon_df.to_csv('data/M_%s.csv'%(ticker_name) )


            fd_list.close()



        for key, val in self.typeDic.items():
            for ticker_name in val:
                df = pdr.get_data_stooq(ticker_name)
                df.to_csv( 'data/O_%s.csv'%(ticker_name) )
                mon_df = df['Close'].resample('M').first()
                mon_df.to_csv('data/M_%s.csv'%(ticker_name) )


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



