class WilliamsIndicators(object):

    def __init__(self, candles):
        self.candles_all_time = candles


    def check_bull_bar_dataframe(self, candles_2rows_dataframe):
        '''
        checks if current bar is bull divergent bar
        :return True if current bar is bull divergent bar, else False
        :param candles_2rows_dataframe: dataframe that consists of two rows of candles in chronological order, created by get_num_rows(self, n)
        '''

        # check if current bar is bull divergent bar.
        if float(candles_2rows_dataframe['Low'][0]) > float(candles_2rows_dataframe['Low'][1]) and \
                float(candles_2rows_dataframe['Close'][1]) > \
                (float(candles_2rows_dataframe['High'][1]) + float(candles_2rows_dataframe['Low'][1])) / 2:
                    return True
        else:
            return False

    def check_bull_bar(self, candles_2rows_list):
        '''
        checks if current bar is bull divergent bar
        :return True if current bar is bull divergent bar, else False
        :param candles_2rows_dataframe: dataframe that consists of two rows of candles in chronological order, created by get_num_rows(self, n)
        candles indicies: 0 - Open time, 1 - Open, 2 - High, 3 - Low, 4 - Close, 5 - Volume, 6 - Close time
        '''

        # check if current bar is bull divergent bar.
        if float(candles_2rows_list[0][3]) > float(candles_2rows_list[1][3]) and \
                float(candles_2rows_list[1][4]) > \
                (float(candles_2rows_list[1][2]) + float(candles_2rows_list[1][3])) / 2:
                    return True
        else:
            return False


    def check_bear_bar(self, candles_2rows_list):
        '''
        checks if current bar is bear divergent bar
        :return True if current bar is bear divergent bar, else False
        :param candles_2rows_dataframe: dataframe that consists of two rows of candles in chronological order, created by get_num_rows(self, n)
        candles indicies: 0 - Open time, 1 - Open, 2 - High, 3 - Low, 4 - Close, 5 - Volume, 6 - Close time
        '''

        if float(candles_2rows_list[0][2]) < float(candles_2rows_list[1][2]) and \
                float(candles_2rows_list[1][4]) < \
                (float(candles_2rows_list[1][2]) + float(candles_2rows_list[1][3])) / 2:
            return True
        else:
            return False


    def check_bear_bar_dataframe(self, candles_2rows_dataframe):
        '''
        checks if current bar is bear divergent bar
        :return True if current bar is bear divergent bar, else False
        :param candles_2rows_dataframe: dataframe that consists of two rows of candles in chronological order, created by get_num_rows(self, n)
        '''

        if float(candles_2rows_dataframe['High'][0]) < float(candles_2rows_dataframe['High'][1]) and \
                float(candles_2rows_dataframe['Close'][1]) < \
                (float(candles_2rows_dataframe['High'][1]) + float(candles_2rows_dataframe['Low'][1])) / 2:
            return True
        else:
            return False


    def SMMA(self, candles_list, n_smoothing_periods, future_shift):
        '''
        :param candles_list: list with candles to get median prices
                candles indicies: 0 - Open time, 1 - Open, 2 - High, 3 - Low, 4 - Close, 5 - Volume, 6 - Close time
                candles_list is at least as long as future_shift

        :param n_smoothing_periods: amount of periods for calculating moving average
        :return: list of SMMAs from n_smoothing_periods position to the (end of list + future_shift)
                elements 0-5 are sma of previouse periods, 6 - SMA for current periods - the rest - future_shift
        '''

        if len(candles_list) < n_smoothing_periods:
            print('too short')
            return

        #create a list of median prices
        self.median_prices_list = []
        for i in range(len(candles_list)):
            median_price = (float(candles_list[i][2]) + float(candles_list[i][3])) / 2  # (high + low) / 2
            self.median_prices_list.append(median_price)

        #print(len('median prices list', self.median_prices_list))

        self.start_len = len(self.median_prices_list)

        for i in range(n_smoothing_periods, len(candles_list) + future_shift):
            #print(self.median_prices_list[-n_smoothing_periods:-1])
            sum_prices = sum(self.median_prices_list[i-n_smoothing_periods:i])
            smma = sum_prices / n_smoothing_periods
            self.median_prices_list.append(smma)

        #print('median_prices_list after smma add', len(self.median_prices_list))
        return self.median_prices_list[-(self.start_len + n_smoothing_periods): -1]

    def alligator_plot(self, candles_list):
        #plot alligator lines for candles_list

        jaw = self.SMMA(candles_list, 13, 8)
        teeth = self.SMMA(candles_list, 8, 5)
        lips = self.SMMA(candles_list, 5, 3)


        # plot
        plt.figure('Alligator')
        plt.clf()
        plt.plot(jaw, color='blue')
        plt.plot(teeth, color='red')
        plt.plot(lips, color = 'green')
        plt.plot(self.median_prices_list[13:len(candles_list)], color ='black')
        plt.show()


    def alligator_calculate(self):
        '''
        Calculates alligator jaw, teeth and lips and returns them as self.jaw etc.
        :return: self.jaw, self.teeth, self.lips
        '''

        # обрахунок алігатора за весь період
        jaw = self.SMMA(self.candles_all_time, 13, 8)
        teeth = self.SMMA(self.candles_all_time, 8, 5)
        lips = self.SMMA(self.candles_all_time, 5, 3)


    def alligator_distance_between_lines(self):
        '''

        :return: info if alligator sleeps or awake, if return is bigger than 1, distance between alligator lines is more tha average
        '''

        #distance between max and min alligator values
        self.distance_list = []
        for i in range(14):
            distance = max(self.jaw[i], self.teeth[i], self.lips[i]) - min(self.jaw[i], self.teeth[i], self.lips[i])
            self.distance_list.append(distance)

        # середнє відхилення між лініями алігатора
        average_distance = sum(self.distance_list) / len(self.distance_list)

        jaw_last_candles_trend = []
        teeth_last_candles_trend = []
        lips_last_candles_trend = []

        for i in range(1, 6):
            last_jaw_diff = self.jaw[-i] - self.jaw[-i-1]
            last_teeth_diff = self.teeth[-i] - self.teeth[-i-1]
            last_lips_diff = self.lips[-i] - self.lips[-i-1]

            jaw_last_candles_trend.append(last_jaw_diff)
            teeth_last_candles_trend.append(last_teeth_diff)
            lips_last_candles_trend.append(last_lips_diff)

        alligator_distances_dict = {}
        alligator_distances_dict['CurrentTrendValue'] = sum(self.distance_list[-6:-1]) / (average_distance * 5)
        alligator_distances_dict['jaw_last_candles_trend(13/8)'] = jaw_last_candles_trend
        alligator_distances_dict['teeth_last_candles_trend(8/5)'] = teeth_last_candles_trend
        alligator_distances_dict['lips_last_candles_trend(5/3)'] = lips_last_candles_trend

        return alligator_distances_dict


    def distance_between_alligator_and_candles(self, two_candles_list, two_candles_index):
        '''
        :param two_candles_list: list of two candles
        :param two_candles_index: index of the first of two candles in self.all_candles
        :return: True if alligator lines are outside given candles
        candles indicies: 0 - Open time, 1 - Open, 2 - High, 3 - Low, 4 - Close, 5 - Volume, 6 - Close time
        '''

        #get alligator lines data
        if two_candles_index < 18:
            return False

        jaw_candles = self.candles_all_time[two_candles_index - 18: two_candles_index + 2]
        teeth_candles = self.candles_all_time[two_candles_index - 16: two_candles_index + 2]
        lips_candles = self.candles_all_time[two_candles_index - 15: two_candles_index + 2]
        last_2_jaw_values = self.SMMA(jaw_candles, 13, 8)
        last_2_teeth_values = self.SMMA(teeth_candles, 8, 5)
        last_2_lips_values = self.SMMA(lips_candles, 5, 3)

        min_alligator_value = min(last_2_jaw_values[-1], last_2_teeth_values[-1], last_2_lips_values[-1])
        max_alligator_value = max(last_2_jaw_values[-1], last_2_teeth_values[-1], last_2_lips_values[-1])


        #if alligator min or max values do not cross the last candle - indicator is valid
        if  float(two_candles_list[-1][3]) < min_alligator_value or \
            max_alligator_value > float(two_candles_list[-1][2]):
            return True
        else:
            return False


    def check_bar_type(self, two_candles_list):
        '''
        :param two_candles_list:
        :return: a bar type like 13, 23, 11 etc.
        candles indicies: 0 - Open time, 1 - Open, 2 - High, 3 - Low, 4 - Close, 5 - Volume, 6 - Close time
        Logic: first number - 1 if open is in upper 1/3 of high-low, range, 3 - in lower
        '''

        bar_type = ''

        one_third = (float(two_candles_list[1][2]) - float(two_candles_list[1][3])) / 3

        #compare open price
        if float(two_candles_list[1][1]) < float(two_candles_list[1][3]) + one_third:
            bar_type += '1'
        elif float(two_candles_list[1][3]) + 2 * one_third < float(two_candles_list[1][1]) < float(two_candles_list[1][3]) + 3 * one_third:
            bar_type += '3'
        else:
            bar_type += '2'

        #compare close price
        if float(two_candles_list[1][4]) < float(two_candles_list[1][3]) + one_third:
            bar_type += '1'
        elif float(two_candles_list[1][3]) + 2 * one_third < float(two_candles_list[1][4]) < float(two_candles_list[1][3]) + 3 * one_third:
            bar_type += '3'
        else:
            bar_type += '2'


        return bar_type


    def trend_direction(self, two_candles_list):
        '''
        :param two_candles_list:
        :return: + if trend goes up, - if trend goes down and 0 if no change
        candles indicies: 0 - Open time, 1 - Open, 2 - High, 3 - Low, 4 - Close, 5 - Volume, 6 - Close time
        '''

        if (float(two_candles_list[1][2]) + float(two_candles_list[1][3])) / 2 > float(two_candles_list[0][2]):
            return '+'
        elif (float(two_candles_list[1][2]) + float(two_candles_list[1][3])) / 2 < float(two_candles_list[0][3]):
            return '-'
        else:
            return '0'


    def profitunity_windows(self, two_candles_list):
        '''
        :param two_candles_list:
        :return: one of four window types: green, squat, fake, fade
        candles indicies: 0 - Open time, 1 - Open, 2 - High, 3 - Low, 4 - Close, 5 - Volume, 6 - Close time
        '''
        if float(two_candles_list[0][5]) == 0 or float(two_candles_list[1][5]) == 0:
            return

        MFI_0 = (float(two_candles_list[0][2]) - float(two_candles_list[0][3])) / float(two_candles_list[0][5])
        MFI_1 = (float(two_candles_list[1][2]) - float(two_candles_list[1][3])) / float(two_candles_list[1][5])

        if MFI_1 > MFI_0 and float(two_candles_list[1][5]) > float(two_candles_list[0][5]):
            return 'green'
        elif MFI_1 > MFI_0 and float(two_candles_list[1][5]) < float(two_candles_list[0][5]):
            return 'squat'
        elif MFI_1 < MFI_0 and float(two_candles_list[1][5]) < float(two_candles_list[0][5]):
            return 'fade'
        elif MFI_1 < MFI_0 and float(two_candles_list[1][5]) > float(two_candles_list[0][5]):
            return 'fake'


    def angularation(self, two_candles_index):
        '''
        :param two_candles_indes: index of next-to-last candle
        :return:True if there is a significant angularation, else False
        candles indicies: 0 - Open time, 1 - Open, 2 - High, 3 - Low, 4 - Close, 5 - Volume, 6 - Close time

        We measure distance between last bar mid price and alligator jaw and same distance -10 indexes from this point.
        It should be greater than 2.5
        '''
        #print(len(self.candles_all_time))
        jaw_candles = self.candles_all_time[two_candles_index - 11: two_candles_index + 2]
        jaw_values = self.SMMA(jaw_candles, 13, 8)

        dist1 = abs(float(jaw_candles[-1][2]) + float(jaw_candles[-1][3]) - jaw_values[-1])
        dist2 = abs(float(jaw_candles[-10][2]) + float(jaw_candles[-10][3]) / 2 - jaw_values[-1])

        # print('dist1', dist1)
        # print('dist2', dist2)
        # print(dist1 / dist2)

        if dist1 / dist2 > 1.012 or dist1/dist2 < 0.9:
            #print('True')
            return True

        return False














