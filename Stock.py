class Stocks:
    stocks_list = {}

    @classmethod
    def search_stock(cls, stock_symbol):
        return cls.stocks_list[stock_symbol] if stock_symbol in cls.stocks_list else None

    @classmethod
    def add(cls, stock_symbol, **args):
        cls.stocks_list[stock_symbol] = args
