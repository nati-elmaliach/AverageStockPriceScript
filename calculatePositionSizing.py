from Api import http_get_request

# Global variables
base_url = "https://api.tiingo.com/iex/"
account_balance = 2000
precentage = 0.07


def calculate_trade_limit():
    return precentage * account_balance


# Get the last live data about the stocks
def get_last_price(stock_symbol):

    base_url_symbol = base_url + stock_symbol
    return http_get_request(base_url_symbol)


def validate_response(stock_data):
    if stock_data is None:
        return None
    elif type(stock_data) is list:
        if not len(stock_data):
            return None
    return True


# Add positinal sizing to the dictonary
def add_positinal_sizing(result_dict, trade_limit, stop_loss):
    last_price = result_dict["last"]
    pos_sizing = last_price
    result_dict["positinal_sizing"] = trade_limit / (last_price - stop_loss)


def calculate_position_sizing(stock_symbol, stop_loss):
    stop_loss = float(stop_loss)
    trade_limit = calculate_trade_limit()
    stock_data = get_last_price(stock_symbol)

    # validte the data exists
    if not validate_response(stock_data):
        return None

    result = {k: stock_data[0].get(k, None)
              for k in ("last", "high", "low", "ticker")}

    add_positinal_sizing(result, trade_limit, stop_loss)
    return result
