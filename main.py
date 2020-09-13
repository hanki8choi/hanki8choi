from DAABackTest import DAABackTest

daa = DAABackTest()
daa.load_type_list()
daa.download_stooq()
daa.load_dataframe()

daa.show_profit()
