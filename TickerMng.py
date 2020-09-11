import pandas as pd
import pandas_datareader as pdr
import csv


class TickerMng:
    def __init__(self):
        # 그룹별 종목 이름 리스트
        self.offenseNames = []
        self.defenseNames = []
        self.canaryNames = []

        # 그룹별 종목 DataFrame 배열
        self.offense_dfs = {}
        self.defense_dfs = {}
        self.canary_dfs = {}

        # 집합 그룹
        self.groupsNames = {'offense': self.offenseNames, 'defense': self.defenseNames, 'canary': self.canaryNames}
        self.groups_dfs = {'offense': self.offense_dfs, 'defense': self.defense_dfs, 'canary': self.canary_dfs}

    def make_ticker2dataframe(self, group_name, ticker_name):
        mon = pd.read_csv('data/M_%s.csv' % ticker_name , sep='\t' )
        mon = mon.set_index('Date', drop=True)

        score_df = mon.pct_change(periods=1) * 12 + mon.pct_change(periods=3) * 4 + \
                   mon.pct_change(periods=6) * 2 + mon.pct_change(periods=12)

        score_df.columns = ['Score']

        profit_df = mon.pct_change(periods=1)
        profit_df.columns = ['Profit']

        mon = pd.concat([mon, score_df['Score']] , axis=1 )
        mon = pd.concat([mon, profit_df['Profit']], axis=1)

        self.groups_dfs[group_name][ticker_name] = mon


    def load_type_list(self):
        for key, val in self.groupsNames.items():
            val.clear()
            fd_list = open('data/Z_%s_list.csv' % key, 'r', encoding='utf-8')
            rdlist = csv.reader(fd_list)
            for line in rdlist:
                ticker_name = line[0]
                val.append(ticker_name)
            fd_list.close()

    def download_stooq(self):
        for key, val in self.groupsNames.items():
            for ticker_name in val:
                df = pdr.get_data_stooq(ticker_name)
                df.to_csv('data/O_%s.csv' % ticker_name, sep='\t' )
                mon_df = df['Close'].resample('M').first().to_frame('Close')
                mon_df.to_csv('data/M_%s.csv' % ticker_name, sep='\t' )

    def load_dataframe(self):
        for key, val in self.groupsNames.items():
            for ticker_name in val:
                self.make_ticker2dataframe(key, ticker_name)

    def is_risky_canary(self, date_idx):
        for key, val in self.canary_dfs.items():
            if val['Score'].iloc[date_idx] <= 0:
                return True
        return False

    def select_defense(self, date_idx):
        names = self.sort_dfs(self.defense_dfs, date_idx, 1)

        print('[%s]   defense : [%s] -> [%lf]' % (
            self.defense_dfs[names[0]].index[date_idx],
            names[0],
            self.defense_dfs[names[0]]['Profit'].iloc[date_idx+1] )  )


        #print(self.defense_dfs[names[0]].iloc[date_idx])

    def select_offense(self, date_idx):
        names = self.sort_dfs(self.offense_dfs, date_idx, 2)

        print('[%s]   offense : [%s %s] -> [%lf %lf]' % (
            self.offense_dfs[names[0]].index[date_idx],
            names[0], names[1],
            self.offense_dfs[names[0]]['Profit'].iloc[date_idx+1] , self.offense_dfs[names[1]]['Profit'].iloc[date_idx+1] )  )

    def sort_dfs(self, dfs, date_idx, count):
        oneday_df = pd.DataFrame()

        for key, val in dfs.items():
            my_data = list(val.iloc[date_idx]) + [key]
            my_col = list(val.iloc[date_idx].index) + ['ticker_name']

            tmp = pd.DataFrame(data=[my_data], columns=my_col)
            oneday_df = oneday_df.append(tmp)

        oneday_df = oneday_df.set_index('ticker_name', drop=False)
        oneday_df = oneday_df.sort_values(by='Score', ascending=False)

        result = []
        for idx in range(0, count):
            result.append(oneday_df.iloc[idx]['ticker_name'])

        return result

    def save_type_list(self):
        for key, val in self.groupsNames.items():
            f = open('data/Z_%s_list.csv' % key, 'w', encoding='utf-8', newline='')
            wr = csv.writer(f)
            for name in val:
                wr.writerow([name])
            f.close()
