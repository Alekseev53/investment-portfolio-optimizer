#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# определение функции
def func(x, a, b):
    return a*np.sqrt(x) + b

import sys
import tqdm
import argparse
import multiprocessing
import functools
import time
from modules.portfolio import Portfolio
from modules.capitalgain import read_capitalgain_csv_data
from modules.plot import draw_portfolios_statistics, draw_portfolios_history
from asset_colors import RGB_COLOR_MAP

MAX_P = 100

def gen_portfolios(assets: list, percentage_step: int, percentages_ret: list):
    if percentages_ret and len(percentages_ret) == len(assets) - 1:
        yield Portfolio(list(zip(assets, percentages_ret + [100 - sum(percentages_ret)])))
        return
    for asset_percent in range(0, MAX_P +1 - sum(percentages_ret), percentage_step):
        added_percentages = percentages_ret + [asset_percent]
        yield from gen_portfolios(assets, percentage_step, added_percentages)


def _simulate_portfolio(market_data, portfolio):
    portfolio.simulate(market_data)
    return portfolio


def _parse_args(argv=None):
    parser = argparse.ArgumentParser(argv)
    parser.add_argument('--debug', action='store_true')
    parser.add_argument('--asset-returns-csv', default='asset_returns.csv', help='path to csv with asset returns')
    parser.add_argument(
        '--precision', type=int, default=1,
        help='simulation precision, values less than 5 require A LOT of ram!')
    return parser.parse_args()
from pprint import pprint

def main(argv):
    cmdline_args = _parse_args(argv)
    #tickers_to_test, yearly_revenue_multiplier = read_capitalgain_csv_data("asset_returns - Copy of asset_returns.csv (2).csv")#cmdline_args.asset_returns_csv
    #tickers_to_test, yearly_revenue_multiplier = read_capitalgain_csv_data("without_gol.csv.csv")#cmdline_args.asset_returns_csv
    #tickers_to_test, yearly_revenue_multiplier = read_capitalgain_csv_data("small_corr.csv")
    
    tickers_to_test, yearly_revenue_multiplier = read_capitalgain_csv_data("my - asset_returns_original.csv")
    
    #tickers_to_test, yearly_revenue_multiplier = read_capitalgain_csv_data("asset_returns_original.csv")#cmdline_args.asset_returns_csv
    #print(tickers_to_test)
    #pprint(yearly_revenue_multiplier)

    time_start = time.time()
    portfolios = []
    for portfolio in gen_portfolios(tickers_to_test, cmdline_args.precision, []):
        portfolios.append(portfolio)
    print(portfolios[0].weights)
    # Bitcon	17.13149
    # Акции РФ	8.11619
    # Золото	3.56040
    # Вклады	64.46515
    # Доллар$	6.72677
    #17.13149+8.11619+3.56040+64.46515+6.72678
        
    # Bitcon	48.21028
    # Акции РФ	22.84003
    # Золото	10.01943
    # Вклады	0.00000
    # $	18.93026
    Active_1 = [
        Portfolio([('Акции РФ', 8.11619), ('Депозиты в рублях (до года)', 64.46515), ('Доллар США', 6.72677), ('Золото', 3.56040), ('Bytcoin', 17.13149)]),
        Portfolio([('Акции РФ', 22.84003), ('Депозиты в рублях (до года)', 0), ('Доллар США', 18.93026), ('Золото', 10.01943), ('Bytcoin', 48.21028)]),
        Portfolio([('Акции РФ',  11.57), ('Депозиты в рублях (до года)', 65.31), ('Доллар США', 4.15), ('Золото', 4.33), ('Bytcoin', 14.64)]),
        ]
    portfolios.extend(Active_1)
    #Active_1=[]
    
    time_prepare = time.time()
    with multiprocessing.Pool() as pool:
        pool_func = functools.partial(_simulate_portfolio, yearly_revenue_multiplier)
        # Use tqdm to monitor progress
        portfolios_simulated = list(tqdm.tqdm(pool.imap(pool_func, portfolios), total=len(portfolios)))

    time_simulate = time.time()

    #print(portfolios_simulated)
    print(len(portfolios_simulated))
    CONST_N=3
    new_portfolios_simulated = []
    for stat_values in portfolios_simulated:
        if stat_values.stat_stdev<=CONST_N:#stat_values.stat_cagr > 0.04:
                    new_portfolios_simulated.append(stat_values)
    portfolios_simulated=new_portfolios_simulated
    

    print(len(portfolios_simulated))
    # # Применяем алгоритм
    portfolios_simulated = sorted(portfolios_simulated, key=lambda x: x.stat_stdev)
    new_result_array = []
    max_gain = -1
    last_stat =0
    for stat_values in portfolios_simulated:
        if (stat_values.stat_gain > max_gain  and stat_values.stat_stdev-last_stat>0.001) or stat_values.weights in [x.weights for x in Active_1]:
            new_result_array.append(stat_values)
            max_gain = max(max_gain, stat_values.stat_gain)
            last_stat = stat_values.stat_stdev
    
    portfolios_simulated = new_result_array


    portfolios_simulated = sorted(portfolios_simulated, key=lambda x: -x.stat_stdev)

    # new_result_array = []
    # max_sharp = 0
    # for stat_values in portfolios_simulated:
    #     if stat_values.stat_sharpe > max_sharp or stat_values.weights in [x.weights for x in Active_1]:
    #         new_result_array.append(stat_values)
    #         max_sharp = max(max_sharp, stat_values.stat_sharpe)
    
    # portfolios_simulated = new_result_array
    # print(len(portfolios_simulated))

    print(f'DONE :: {len(portfolios_simulated)} portfolios tested')
    print(f'times: prepare = {time_prepare-time_start:.2f}s, simulate = {time_simulate-time_prepare:.2f}s')
    print(' --- Edge Cases --- ')
    portfolios_for_history = set()
    portfolios_simulated.sort(key=lambda x: x.stat_cagr)
    portfolios_for_history.add(portfolios_simulated[0])
    portfolios_for_history.add(portfolios_simulated[-1])
    print(f'MAX PROFIT: {portfolios_simulated[-1]}')
    print(f'MAX LOSS  : {portfolios_simulated[0]}')
    portfolios_simulated.sort(key=lambda x: x.stat_var)
    portfolios_for_history.add(portfolios_simulated[0])
    portfolios_for_history.add(portfolios_simulated[-1])
    print(f'  VOLATILE: {portfolios_simulated[-1]}')
    print(f'    STABLE: {portfolios_simulated[0]}')
    portfolios_simulated.sort(key=lambda x: x.stat_sharpe)
    portfolios_for_history.add(portfolios_simulated[0])
    portfolios_for_history.add(portfolios_simulated[-1])
    print(f'MAX SHARPE: {portfolios_simulated[-1]}')
    print(f'MIN SHARPE: {portfolios_simulated[0]}')

    for portfolio in portfolios_simulated:
        if portfolio.number_of_assets() == 1:
            portfolios_for_history.add(portfolio)







    # draw_portfolios_history(
    #     portfolios_for_history,
    #     title='Capital gain history for edge cases portfolios',
    #     xlabel='Year', ylabel='Total capital gain %', color_map=RGB_COLOR_MAP)

    title = ', '.join(
        [
            f'{min(yearly_revenue_multiplier.keys())}-{max(yearly_revenue_multiplier.keys())}',
            'rebalance every row',
            f'{cmdline_args.precision}% step',
        ]
    )
    draw_portfolios_statistics(
        portfolios_list=portfolios_simulated,
        f_x=lambda x: x.stat_var, f_y=lambda y: y.stat_cagr * 100,
        title=title, xlabel='Variance', ylabel='CAGR %', color_map=RGB_COLOR_MAP)
    draw_portfolios_statistics(
        portfolios_list=portfolios_simulated,
        f_x=lambda x: x.stat_var, f_y=lambda y: y.stat_sharpe,
        title=title, xlabel='Variance', ylabel='Sharpe', color_map=RGB_COLOR_MAP)
    draw_portfolios_statistics(
        portfolios_list=portfolios_simulated,
        f_x=lambda x: x.stat_stdev, f_y=lambda y: y.stat_cagr * 100,
        title=title, xlabel='Stdev', ylabel='CAGR %', color_map=RGB_COLOR_MAP)
    draw_portfolios_statistics(
        portfolios_list=portfolios_simulated,
        f_x=lambda x: x.stat_stdev, f_y=lambda y: y.stat_sharpe,
        title=title, xlabel='Stdev', ylabel='Sharpe', color_map=RGB_COLOR_MAP)
    draw_portfolios_statistics(
        portfolios_list=portfolios_simulated,
        f_x=lambda x: x.stat_sharpe, f_y=lambda y: y.stat_cagr * 100,
        title=title, xlabel='Sharpe', ylabel='CAGR %', color_map=RGB_COLOR_MAP)

    # xdata = [x.stat_stdev for x in portfolios_simulated]
    # ydata = [x.stat_cagr for x in portfolios_simulated]

    # # поиск параметров
    # popt, pcov = curve_fit(func, xdata, ydata)

    # # вывод параметров
    # a, b = popt
    # print(f"a = {a}, b = {b}")
    
    
    # # создание последовательности для визуализации
    # x = np.linspace(xdata[0], CONST_N, 400)
    # y = func(x, *popt)
    # # Clear the plot before visualizing
    # plt.clf()

    # # визуализация
    # plt.figure(figsize=(10,6))
    # plt.plot(xdata, ydata, 'bo', label='данные')
    # plt.plot(x, y, 'r', label='подгонка: a=%.3f, b=%.3f' % tuple(popt))
    # plt.xlabel('x')
    # plt.ylabel('y')
    # plt.legend()
    # plt.show()

if __name__ == '__main__':
    main(sys.argv)
