import re
from finviz.screener import Screener


# Global Variabels
MIN_SHARES_FLOAT = 450000000


# Convert '490.56M' to 450000000
def parse_float(shares_float):
    # check if the number i above billion
    if 'B' in shares_float:
        return MIN_SHARES_FLOAT

    match_obj = re.match(r'([0-9]*)\.([0-9]*)', shares_float)
    match_number = float(match_obj.group()) * 1000000
    return match_number


def filter_data(data):
    result = []

    for index, stock in enumerate(data):
        shares_float = stock["Float"]
        shares_float = parse_float(shares_float)
        if shares_float >= MIN_SHARES_FLOAT:
            result.append(data[index])

    return result


def main():
    filters = ['sh_avgvol_o2000', 'sh_instown_o60', 'ta_volatility_wo8']
    stock_list = Screener(filters=filters, table='Ownership')
    filter_results = filter_data(stock_list.data)
    stock_list.data = filter_results
    stock_list.to_csv('./Stocks.csv')


main()

# data = [{'No.': '1', 'Ticker': 'ADNT', 'Market Cap': '1.10B', 'Outstanding': '490.43M', 'Float': '40.97B', 'Insider Own': '0.70%', 'Insider Trans': '1.35%', 'Inst Own': '98.40%',
#          'Inst Trans': '-0.05%', 'Float Short': '6.67%', 'Short Ratio': '3.04', 'Avg Volume': '2.04M', 'Price': '11.56', 'Change': '7.53%', 'Volume': '2,121,812'}]
