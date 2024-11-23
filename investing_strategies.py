import yfinance as yf
import pandas as pd

TIMEFRAMES = {'1d': 1 / 365, '5d': 1 / 73, '1mo': 1 / 12, '3mo': 1 / 4, '6mo': 1 / 2, '1y': 1, '2y': 2, '5y': 5, '10y': 10, 'ytd': None, 'max': None}


class InvestStrategies:
    def __init__(self, time_frame: str = '10y') -> None:
        if time_frame not in ['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max']:
            raise Exception("Invalid time frame, must be one of ['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max']")

        self.time_frame = time_frame
        self.safe = yf.download("ZN=F", group_by="Ticker", period=time_frame)       # safe strategy     10-Year T-Note Futures,Dec-2024 https://finance.yahoo.com/quote/ZN%3DF/
        self.medium = yf.download("^SPX", group_by="Ticker", period=time_frame)     # medium strategy   S&P 500 index,                  https://finance.yahoo.com/quote/%5ESPX/
        self.risky = yf.download("TSLA", group_by="Ticker", period=time_frame)      # risky strategy    TESLA                           https://finance.yahoo.com/quote/TSLA/

    def interest_rates(self) -> tuple[float, float, float]:
        return (self.calc_interest_rate(self.safe), self.calc_interest_rate(self.medium), self.calc_interest_rate(self.risky))

    def calc_interest_rate(self, data: pd.DataFrame) -> float:
        actual_years = TIMEFRAMES[self.time_frame]
        if self.time_frame == "ytd" or self.time_frame == "max":
            actual_years = data.len() / 12
        start_val = float(data.iloc[3][4])
        end_val = float(data.iloc[-1][4])
        return (pow(end_val / start_val, 1 / actual_years) - 1) * 100


'''
def main() -> None:
    invs = InvestStrategies()
    print(invs.interest_rates())


if __name__ == "__main__":
    main()
'''
