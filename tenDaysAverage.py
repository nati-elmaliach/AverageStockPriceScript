import requests as req
import pandas as pd
import numpy as np
import colorama
import random
import math
from datetime import datetime, timedelta

# If using Windows, init() will cause anything sent to stdout or stderr
# will have ANSI color codes converted to the Windows versions. Hooray!
# If you are already using an ANSI compliant shell, it won't do anything
colorama.init()

# Now regular ANSI codes should work, even in Windows
CLEAR_SCREEN = '\033[2J'
RED = '\033[31m'   # mode 31 = red forground
GREEN = '\033[32m'   # mode 31 = red forground
BLUE = '\033[34m'   # mode 31 = red forground
YELLOW = '\033[93m'   # mode 31 = red forground
MAGENTA = '\033[35m'   # mode 31 = red forground
CYAN = '\033[36m'   # mode 31 = red forground
RESET = '\033[0m'  # mode 0  = reset

bcolors = [GREEN,BLUE,YELLOW,CYAN,MAGENTA]

RED = '\033[31m'   # mode 31 = red forground
RESET = '\033[0m'  # mode 0  = reset

def format_output(stock_symbol, last_price, average, stocks , percent_move):
    print(RED + "---------------------------------" + RESET)
    print(random.choice(bcolors) + stock_symbol + ":" + RESET)
    print('closed price: ' + last_price)
    print('average: ' + average)
    print(GREEN + 'stocks: ' + stocks + RESET)
    print(BLUE + 'percent move: ' + percent_move + " %" + RESET)

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

# def color_output(stock_symbol, result):
#     color_list = ["RED", "GREEN", "YELLOW", "BLUE", "MAGENTA", "CYAN"]
#     random_color = random.choice(color_list)

def get_last_closing_price(data):
    return data[-1]["close"]

# Get the stock data
def stock_average_closed(data, current_avg):

	current_sum = 0
	data_length = get_data_length(data)
	for day in data:
		current_sum += day["close"]

	return current_sum / data_length



def calc_precent(result ,stock_price_average):
	return (result / stock_price_average) * 100

def get_stock_data(stock_symbol, start_date, end_date):

    headers = {'Content-Type': 'application/json'}
    base_url = "https://api.tiingo.com/tiingo/daily/" + stock_symbol + '/prices?'
    api_key = 'bb62373b5df86ade9348afa490d689242b473c70'
    payload = {
        'startDate': start_date,
        'endDate': end_date,
        'token': api_key,
        'columns': ['close,low,high']
    }

    response = req.get(base_url, params=payload, headers=headers)

    if response.status_code == 404:
        format_error(f"{stock_symbol} is not a valid stock symbol")
        return

    data = response.json()
    result = calculate_average(data)
    stocks = round(1000/result)
    last_price = get_last_closing_price(data)
    stock_price_average = stock_average_closed(data,result)
    print(stock_price_average)
    percent_move = calc_precent(result ,stock_price_average )
    format_output(stock_symbol, str(last_price), str(result), str(stocks) , str(percent_move))


# calculate the date 10 days ago
def calculate_start_and_end():
    today = datetime.today()
    delta = timedelta(days=20)
    result = today - delta
    return result.strftime('%Y-%m-%d'), today.strftime('%Y-%m-%d')

# Program entry point


def main():
    exit_flag = False
    start_date, end_date = calculate_start_and_end()
    while True:
        value = input("Enter stock tick here: ")
        exit_flag = validate_input(value)

        if exit_flag:
            break

        get_stock_data(value.upper().strip(), start_date, end_date)


main()

# Change thr ticker to random color
# show error in red
