from TechnicalAnalysis import *
import time

class WilliamsIndicatorsTest(WilliamsIndicators):

    def __init__(self):
        BinanceConnect.__init__(self)
        self.WI_test = WilliamsIndicators()
        #self.all_candles = BinanceConnect.get_candles_list(self, self.currency_pair, self.time_interval)
        #self.candles_all_time = self.get_candles_list_all_time(self.currency_pair, self.time_interval)


    def test_check_bull_bar(self):
        print(self.WI_test.check_bull_bar_dataframe(self.get_n_candles_as_dataframe(2)))


    def test_check_bear_bar(self):
        print(self.WI_test.check_bear_bar_dataframe(self.get_n_candles_as_dataframe(2)))


    def test_aligator_plot(self):
        #measure script run time
        start_time = time.time()

        #get last 1000 candles list
        candles = self.WI_test.get_candles_list(self.currency_pair, self.time_interval)
        i = 999
        candles_list = candles[i-70:i]

        self.WI_test.alligator_plot(candles_list)

        #measure script run time
        print('running time', time.time() - start_time, 'sec.')


    def test_smma(self):
        # get last 1000 candles list
        candles = self.WI_test.get_candles_list(self.currency_pair, self.time_interval)
        #candles = pd.read_csv('/Volumes/Data/Dropbox/Dropbox/Coding/BinanceTrade/binance_candles.csv')

        i = 979
        candles_list = candles[i - 20:i]

        #candles_list = [1,2,3,1,2,3,1,2,3,1,2,3,1,2,3,1,2,3,1,2]
        print(self.WI_test.SMMA(candles_list, 5, 3))
        print(len(self.WI_test.SMMA(candles_list, 5, 3)))


    def test_alligator_distance_between_lines(self):
        # get last 1000 candles list and pass part of them to alligator
        candles = self.WI_test.get_candles_list(self.currency_pair, self.time_interval)
        i = 999
        candles_list = candles[i - 70:i]

        print(self.WI_test.alligator_distance_between_lines())


    def test_distance_between_alligator_and_candles(self):
        two_candles_list = self.all_candles[998:]
        two_candles_index = 998
        print(self.WI_test.distance_between_alligator_and_candles(two_candles_list, two_candles_index))


    def test_check_bar_type(self):
        for i in range(300, 515):
            two_candles_list = self.all_candles[i:i+2]
            print(self.WI_test.check_bar_type(two_candles_list))


    def test_trend_direction(self):
        for i in range(300, 515):
            two_candles_list = self.all_candles[i:i+2]
            print(self.WI_test.trend_direction(two_candles_list))


    def test_profitunity_windows(self):
        for i in range(300, 515):
            two_candles_list = self.all_candles[i:i+2]
            print(self.WI_test.profitunity_windows(two_candles_list))


    def test_newbee_strategy(self):
        for i in range(300, 515):
            two_candles_list = self.all_candles[i:i+2]
            trend = self.WI_test.trend_direction(two_candles_list)
            bar_type = self.WI_test.check_bar_type(two_candles_list)
            window = self.WI_test.profitunity_windows(two_candles_list)

            print(trend, bar_type, window)


    def test_angularation(self):
        two_candles_index = len(self.candles_all_time) - 2
        print(self.WI_test.angularation(two_candles_index))
        #print(len(self.WI_test.angularation(two_candles_index)))


# measure script run time
start_time = time.time()


# currency_dict = {'LTC': 0, 'USDT': 1000}
# time_interval = Client.KLINE_INTERVAL_15MINUTE
x = WilliamsIndicatorsTest()
# x.test_check_bull_bar()
# x.test_check_bear_bar()
#x.test_smma()
#x.test_alligator_distance_between_lines()
# x.test_distance_between_alligator_and_candles()
# x.test_aligator_plot()
#x.test_check_bar_type()
#x.test_trend_direction()
#x.test_profitunity_windows()
#x.test_newbee_strategy()
x.test_angularation()


# measure script run time
print('Total running time', time.time() - start_time, 'sec.')
