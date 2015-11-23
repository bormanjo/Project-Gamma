import json, sys
sys.path.append(r'/Users/jzmanrulz/anaconda/lib/python3.4/site-packages')
import yahoo_finance as yf

DATA_FILE = "portfolios.txt"

class Equity(object):
    def __init__(self, symbol):
        self.equity = yf.Share(symbol)
        self.data = {
            "high_52":self.equity.get_year_high,
            "low_52":self.equity.get_year_low,
            "high_day":self.equity.get_days_high,
            "low_day":self.equity.get_days_low,
            "price":self.equity.get_price,
            "volume":self.equity.get_volume,
            "market_cap":self.equity.get_market_cap,
            "pe":self.equity.get_price_earnings_ratio,
            "peg":self.equity.get_price_earnings_growth_ratio,
            "pb":self.equity.get_price_book,
            "ps":self.equity.get_price_sales,
            "info":self.equity.get_info,
            "open":self.equity.get_open,
            "exchange":self.equity.get_stock_exchange,
            "ebitda":self.equity.get_ebitda,
            "div_yield":self.equity.get_dividend_yield,
            "earnings":self.equity.get_earnings_share,
            "mov_avg_50":self.equity.get_50day_moving_avg,
            "mov_avg_200":self.equity.get_200day_moving_avg,
            "refresh":self.equity.refresh
            }
    def get_data(self, value):
        '''returns the specified data from YahooFinance'''
        return self.data[value]()
        
class Currency(object):
    def __init__(self, symbol):
        self.currency = yf.Currency(symbol)
        self.data = {
            "bid":self.currency.get_bid,
            "ask":self.currency.get_ask,
            "rate":self.currency.get_rate,
            "trade_time":self.currency.get_trade_datetime,
            "refresh":self.currency.refresh
            }
    def get_data(self, value):
        '''returns the specified data from YahooFinance'''
        return self.data[value]()

class DataIO(object):
    def __init__(self):
        self.positionVals = ["Net Liquidity","Quantity", "Trades", "Type"]
        try:
            open(DATA_FILE, 'x')
        except FileExistsError:
            pass       
    def _load(self):
        '''returns data from DATA_FILE'''
        with open(DATA_FILE, 'r') as file:
            data = json.load(file)
        return data
    def _save(self, data):
        '''saves given data to DATA_FILE'''
        with open(DATA_FILE, 'w') as file:
            json.dump(data, file)
            
    def yf_value(self, obj, symbol, value):
        '''Returns specified value for symbol from YahooFinance API'''
        if obj.lower() == "equity":
            A = Equity(symbol)
        elif obj.lower() == "currency":
            A = Currency(symbol)
        else:
            return "Invalid command"
        A.get_data("refresh")
        return A.get_data(value)
    def read_value(self, portfolio, symbol, item):
        '''Returns the item value from a symbol in the portfolio'''
        try:
            data = self._load()
        except ValueError:
            print("RV Val Error")
            data = {}
        try:
            return data[portfolio][symbol][item] 
        except KeyError:
            print("No value exists in ", portfolio, " for the data specified")
            return None
    def write_value(self, portfolio, symbol, item, value):
        '''Writes a value of an item to the symbol in a portfolio'''
        data = self._load()
        if symbol not in data[portfolio]:
            data[portfolio][symbol] = {}        #create new symbol in portfolio
        data[portfolio][symbol][item] = value   #add value to item
        self._save(data)
    def read_symbols(self, portfolio):
        '''Returns a list of all current symbols in portfolio'''
        data = self._load()
        L = []
        try:
            for key, val in data[portfolio].items():
                L.append(key)
        except KeyError:
            pass
        return L
    def write_symbol(self, portfolio, symbol, obj):
        '''Writes data structure skeleton for a symbol'''
        data = self._load()
        if symbol not in data[portfolio]:
            data[portfolio][symbol] = {}
            for val in self.positionVals:
                data[portfolio][symbol] = {"Net Liquidity": 0.00,
                                           "Quantity":0,
                                           "Trades":[],
                                           "Type":obj}
        self._save(data)
    def read_portfolio(self, portfolio):
        '''Returns dictionary all current portfolio data'''
        try:
            data = self._load()
        except (KeyError, ValueError) as e:
            print("RP Val Error")
            data[portfolio] = {}
        return data[portfolio]
    def write_portfolio(self, name):
        '''Writes a new portfolio'''
        try:
            data = self._load()
        except ValueError:
            print("WP Val Error")
            data = {}
        data[name] = {"_info":{"Name":name, "Liquid Cash":10000.00}}
        self._save(data)
        print("Portfolio: '", name, "' created.")
    def portfolios(self):
        '''returns a list of all portfolio names in portfolio.txt'''
        L = []
        try:
            data = self._load()
        except ValueError:
            print("P Val Error")
            data = {}
        for key in data:
            L.append(key)
        return L

