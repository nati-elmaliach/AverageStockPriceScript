import pandas as pd
import numpy as np
import colorama
import re
import random
import math
from datetime import datetime, timedelta
from operator import itemgetter

from Stock import Stocks
from calculatePositionSizing import calculate_position_sizing
from Api import http_get_request

# If using Windows, init() will cause anything sent to stdout or stderr
# will have ANSI color codes converted to the Windows versions. Hooray!
# If you are already using an ANSI compliant shell, it won't do anything
colorama.init()
stocks_list = Stocks()

# Now regular ANSI codes should work, even in Windows
CLEAR_SCREEN = '\033[2J'
RED = '\033[31m'   # mode 31 = red forground
GREEN = '\033[32m'   # mode 31 = red forground
BLUE = '\033[34m'   # mode 31 = red forground
YELLOW = '\033[93m'   # mode 31 = red forground
MAGENTA = '\033[35m'   # mode 31 = red forground
CYAN = '\033[36m'   # mode 31 = red forground
RESET = '\033[0m'  # mode 0  = reset

bcolors = [GREEN, BLUE, YELLOW, CYAN, MAGENTA]

RED = '\033[31m'   # mode 31 = red forground
RESET = '\033[0m'  # mode 0  = reset


def format_output(stock_symbol, last_price, average, stocks, percent_move):
    print(RED + "---------------------------------" + RESET)
    print(random.choice(bcolors) + stock_symbol + ":" + RESET)
    print('closed price: ' + last_price)
    print('average: ' + average)
    print(GREEN + 'stocks: ' + stocks + RESET)
    print(BLUE + 'percent move: ' + percent_move + " %" + RESET)

    print(RED + "---------------------------------" + RESET)


def format_positinal_sizing_output(last, high, low, ticker, positinal_sizing):
    print(RED + "---------------------------------" + RESET)
    print(random.choice(bcolors) + ticker +
          ": POSITINAL SIZING CALCULATION" + RESET)
    print('HIGH: ' + str(high))
    print('LOW: ' + str(low))
    print(GREEN + 'LAST PRICE: ' + str(last) + RESET)
    print(BLUE + 'POSITIONAL SIZING: ' + str(positinal_sizing) + RESET)

    print(RED + "---------------------------------" + RESET)


def format_error(message):
    print(RED + "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" + RESET)
    print(message)
    print(RED + "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" + RESET)


def get_data_length(data):
    return len(data)


# Validate the user input is correct
def validate_input(user_input):
    if user_input == 'exit':
        return True


def calculate_average(data):
    current_sum = 0
    data_length = get_data_length(data)

    for day_trade in data:
        day_diff = day_trade['high'] - day_trade['low']
        current_sum += day_diff

    return current_sum / data_length


def get_last_closing_price(data):
    return data[-1]["close"]

# Get the stock data


def stock_average_closed(data, current_avg):

    current_sum = 0
    data_length = get_data_length(data)
    for day in data:
        current_sum += day["close"]

    return current_sum / data_length


def calc_precent(result, stock_price_average):
    return (result / stock_price_average) * 100


def get_stock_data(stock_symbol, start_date, end_date):

    base_url = "https://api.tiingo.com/tiingo/daily/" + stock_symbol + '/prices?'
    payload = {
        'startDate': start_date,
        'endDate': end_date,
        'columns': ['close,low,high']
    }

    response = http_get_request(base_url, payload)

    if not response:
        format_error(f"{stock_symbol} is not a valid stock symbol")
        return

    result = calculate_average(response)
    stocks = round(1000/result)
    last_price = get_last_closing_price(response)
    stock_price_average = stock_average_closed(response, result)
    percent_move = calc_precent(result, stock_price_average)

    # Add the stock to the stocks list in the Stocks class
    stocks_list.add(stock_symbol, last_price=str(last_price), average=str(
        result), stocks=str(stocks), precent_move=str(percent_move))

    format_output(stock_symbol, str(last_price), str(
        result), str(stocks), str(percent_move))


# calculate the date 10 days ago
def calculate_start_and_end():
    today = datetime.today()
    delta = timedelta(days=20)
    result = today - delta
    return result.strftime('%Y-%m-%d'), today.strftime('%Y-%m-%d')


def search_stocks(stock_symbol):
    current_stock = stocks_list.search_stock(stock_symbol)

    # if the stock exists
    if current_stock:
        last_price, average, stocks, precent_move = itemgetter(
            'last_price', 'average', 'stocks', 'precent_move')(current_stock)

        format_output(stock_symbol, last_price, average, stocks, precent_move)
        return True

    return None


def check_for_digits(input_string):
    return any(char.isdigit() for char in input_string)


def request_router(value, start_date, end_date):
    if type(value) is list:
        data = calculate_position_sizing(value[0], value[1])

        if not data:
            format_error(f"{value[0]} is not a valid stock symbol")
            return

        format_positinal_sizing_output(**data)

    else:
        get_stock_data(value, start_date, end_date)

# Program entry point


def main():
    exit_flag = False
    start_date, end_date = calculate_start_and_end()
    while True:
        value = input("Enter stock tick here: ")
        exit_flag = validate_input(value)

        if exit_flag:
            break

        value = value.upper().strip()

        if check_for_digits(value):
            input_args = value.split()
            request_router(input_args, start_date, end_date)

        elif not search_stocks(value):
            print("searching web")
            request_router(value, start_date, end_date)


main()
