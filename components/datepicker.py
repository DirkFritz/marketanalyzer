from dash import (
    dcc,
)

from datetime import datetime, timedelta


def generateDatePicker(min, max, delta_days):
    start_date = datetime.today() - timedelta(days=delta_days)
    return dcc.DatePickerRange(
        id="my-date-picker-range",
        min_date_allowed=min,
        max_date_allowed=max,
        start_date=start_date.date(),
        initial_visible_month=max,
        end_date=max,
        style={"zIndex": 10},
        persistence=True,
    )
