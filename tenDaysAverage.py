import requests as req
import pandas as pd
import numpy as np
import colorama
import random
from datetime import datetime, timedelta


def format_output(message):
    print("---------------------------------")
    print(message)
    print("---------------------------------")


# Validate the user input is correct
def validate_input(user_input):
    if user_input == 'exit':
        return True


def calculate_average(data):
    current_sum = 0
    data_length = len(data)

    for day_trade in data:
        day_diff = day_trade['high'] - day_trade['low']
        current_sum += day_diff

    return current_sum / data_length


# def color_output(stock_symbol, result):
#     color_list = ["RED", "GREEN", "YELLOW", "BLUE", "MAGENTA", "CYAN"]
#     random_color = random.choice(color_list)


# Get the stock data
def get_stock_data(stock_symbol, start_date, end_date):

    headers = {'Content-Type': 'application/json'}
    base_url = "https://api.tiingo.com/tiingo/daily/" + stock_symbol + '/prices?'
    api_key = 'Your API key here'
    payload = {
        'startDate': start_date,
        'endDate': end_date,
        'token': api_key,
        'columns': ['low,high']
    }

    response = req.get(base_url, params=payload, headers=headers)

    if response.status_code == 404:
        format_output(f"{stock_symbol} is not a valid stock symbol")
        return

    data = response.json()
    result = calculate_average(data)
    format_output(f"{stock_symbol} -> {result}")


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
