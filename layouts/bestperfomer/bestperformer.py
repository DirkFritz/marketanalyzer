from dash import (
    dcc,
    html,
)
from db.dbqueries import get_stock_data
import datetime

from algos.bestperformer import BestPerformer


def generate_dataset(stocks_performance, symbols):
    pass


def determ_best_perfomer():

    symbols = ["COIN", "NVDA", "PYPL", "AAPL"]
    end_date = datetime.datetime.today()
    start_date = end_date - datetime.timedelta(days=30)
    stock_groups, stocks_performance = get_stock_data(
        start_date.date(),
        end_date.date(),
        symbols,
    )
    print(stock_groups)
    print(stocks_performance)
    best_performer = BestPerformer()
    # best_performer.find_perfomrer()

    return html.P("Bestperfomer")


best_perfomrer = [determ_best_perfomer()]
